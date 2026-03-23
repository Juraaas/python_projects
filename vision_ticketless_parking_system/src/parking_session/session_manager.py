import uuid
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from src.parking_session.billing_engine import BillingEngine


@dataclass
class ParkingSession:
    session_id: str
    plate: str
    entry_time: float
    state: str
    payment_status: str = "unpaid"
    exit_time: float = None
    amount_due: float = 0.0


class SessionManager:
    def __init__(self):
        self.active_sessions = {}
        self.session_history = []
        self.billing = BillingEngine()
        self.grace_period_sec = 30

    def _normalize(self, plate):
        if not plate:
            return plate
        return (
            plate.upper()
            .replace("O", "0")
            .replace("I", "1")
            .replace("B", "8")
            .replace("S", "5")
        )

    def _similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def _find_matching_plate(self, plate, threshold=0.8):
        plate_norm = self._normalize(plate)
        best_match = None
        best_score = 0.0

        for existing_plate in self.active_sessions.keys():
            existing_norm = self._normalize(existing_plate)
            score = self._similarity(plate_norm, existing_norm)

            if score > best_score:
                best_score = score
                best_match = existing_plate
        
        if best_score >= threshold:
            return best_match
        
        return None

    def handle_event(self, event):
        event_type = event["type"]
        plate = event["plate"]

        if event_type == "vehicle_entered":
            return self._handle_entry(plate, event["time"])
        
        elif event_type == "vehicle_exit_detected":
            return self._handle_exit(plate, event["time"])
        
        elif event_type == "payment_confirmed":
            return self._handle_payment(plate)
        
    def _handle_entry(self, plate, timestamp):
        if plate in self.active_sessions:
            return None
        
        session = ParkingSession(
            session_id=str(uuid.uuid4()),
            plate=plate,
            entry_time=timestamp,
            state="SESSION_ACTIVE",
        )
        self.active_sessions[plate] = session

        return {
            "type": "session_started",
            "plate": plate,
            "session_id": session.session_id,
        }
    
    def _handle_payment(self, plate):
        matched_plate = self._find_matching_plate(plate)

        if matched_plate:
            plate = matched_plate

        session = self.active_sessions.get(plate)
        if not session:
            return None
        
        if session.payment_status == "paid":
            return {
                "type": "payment_ignored",
                "plate": plate,
                "reason": "already_paid",
            }
        
        session.payment_status = "paid"
        session.payment_time = time.time()
        session.state = "PAYMENT_CONFIRMED"
        session.amount_due = 0.0

        return {
            "type": "payment_confirmed",
            "plate": plate
        }
    
    def _handle_exit(self, plate, timestamp):
        matched_plate = self._find_matching_plate(plate)

        if matched_plate:
            plate = matched_plate
            
        session = self.active_sessions.get(plate)
        if not session:
            return None
        
        if session.payment_status != "paid":
            session_state = "PAYMENT_PENDING"

            session.amount_due = self.billing.calculate_fee(
                session.entry_time,
                timestamp,
            )

            return {
                "type": "exit_blocked",
                "plate": plate,
                "amount_due": session.amount_due,
            }
        
        if timestamp - session.payment_time > self.grace_period_sec:
            session.payment_status = "unpaid"

            additional_fee = self.billing.calculate_additional_fee(
                session.payment_time,
                timestamp,
            )
            session.amount_due = additional_fee

            return {
                "type": "exit_blocked",
                "plate": plate,
                "reason": "grace_expired",
                "amount_due": additional_fee,
            }

        session_state = "SESSION_ENDED"
        session.exit_time = timestamp

        self.session_history.append(session)
        del self.active_sessions[plate]

        return {
            "type": "session_ended",
            "plate": plate,
            "session_id": session.session_id,
        }
            