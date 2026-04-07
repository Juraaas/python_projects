import uuid
import time
from dataclasses import dataclass
from difflib import SequenceMatcher
from src.parking_session.billing_engine import BillingEngine
from src.db.database import SessionLocal, get_db
from src.db.models import ParkingSessionDB


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
        self.billing = BillingEngine()
        self.grace_period_sec = 60
        self.entry_cooldown_sec = 10

    def _normalize(self, plate):
        if not plate:
            return plate
        return (
            plate.upper()
            .replace("O", "0")
            .replace("I", "1")
        )

    def _similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def _find_matching_plate(self, plate, threshold=0.9):
        best_match = None
        best_score = 0.0

        with get_db() as db:
            sessions = db.query(ParkingSessionDB).filter_by(status="ACTIVE").all()

            for s in sessions:
                norm_input = self._normalize(plate)
                norm_existing = self._normalize(s.plate)

                score = self._similarity(norm_input, norm_existing)

                if norm_input in norm_existing or norm_existing in norm_input:
                    score = max(score, 0.95)
            
                if score > best_score:
                    best_score = score
                    best_match = s.plate

        if best_score >= threshold:
            return best_match
        return None

    def handle_event(self, event):
        plate = event["plate"]

        if not plate or len(plate) < 5:
            return None
        
        event_type = event["type"]

        if event_type == "vehicle_entered":
            return self._handle_entry(plate, event["time"])
        
        elif event_type == "vehicle_exit_detected":
            return self._handle_exit(plate, event["time"])
        
        elif event_type == "payment_confirmed":
            return self._handle_payment(plate)
        
    def _handle_entry(self, plate, timestamp):
        matched = self._find_matching_plate(plate)
        if matched:
            with get_db() as db:
                session = db.query(ParkingSessionDB).filter_by(plate=matched, status="ACTIVE").first()

                if session:
                    if timestamp - session.entry_time < self.entry_cooldown_sec:
                        return None
                    
        session_id = str(uuid.uuid4())

        with get_db() as db:

            db_session = ParkingSessionDB(
                session_id = session_id,
                plate = plate,
                entry_time = timestamp,
                payment_status = "unpaid",
                amount_due = 0.0,
                status = "ACTIVE",
            )
            db.add(db_session)
            db.commit()

        return {
            "type": "session_started",
            "plate": plate,
            "session_id": session_id,
        }
    
    def _handle_payment(self, plate):
        matched_plate = self._find_matching_plate(plate) or plate

        if matched_plate:
            plate = matched_plate

        with get_db() as db:
            session = (db.query(ParkingSessionDB).filter_by(plate=plate, status="ACTIVE").first())

            if not session:
                return None
            
            if session.payment_status == "paid":
                if time.time() - session.payment_time <= self.grace_period_sec:
                    return {
                        "type": "payment_ignored",
                        "plate": plate,
                        "reason": "already_paid",
                    }
            
            session.payment_status = "paid"
            session.payment_time = time.time()
            session.amount_due = 0.0

            db.commit()

        return {
            "type": "payment_confirmed",
            "plate": plate,
        }
    
    def _handle_exit(self, plate, timestamp):
        plate = self._find_matching_plate(plate) or plate
        
        with get_db() as db:
            session = (db.query(ParkingSessionDB).filter_by(plate=plate, status="ACTIVE").first())

            if not session:
                return None
            
            if session.payment_status != "paid":
                fee = self.billing.calculate_fee(session.entry_time, timestamp)
                session.amount_due = fee
                db.commit()

                return {
                    "type": "exit_blocked",
                    "plate": plate,
                    "amount_due": fee,
                }
        
            if session.payment_time and timestamp - session.payment_time > self.grace_period_sec:
                additional_fee = self.billing.calculate_additional_fee(
                    session.payment_time,
                    timestamp,
                )
                session.payment_status = "unpaid"
                session.amount_due = additional_fee
                db.commit()

                return {
                    "type": "exit_blocked",
                    "plate": plate,
                    "reason": "grace_expired",
                    "amount_due": additional_fee,
                }
            session_id = session.session_id,
            session.exit_time = timestamp
            session.status = "ENDED"
            db.commit()

        return {
            "type": "session_ended",
            "plate": plate,
            "session_id": session_id,
        }
            