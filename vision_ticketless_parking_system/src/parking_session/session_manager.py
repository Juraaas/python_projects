from dataclasses import dataclass
import uuid
import time
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
        session = self.active_sessions.get(plate)
        if not session:
            return None
        
        session.payment_status = "paid"
        session.payment_time = time.time()
        session.state = "PAYMENT_CONFIRMED"

        return {
            "type": "payment_confirmed",
            "plate": plate
        }
    
    def _handle_exit(self, plate, timestamp):
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

            return {
                "type": "exit_blocked",
                "plate": plate,
                "reason": "grace_expired",
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
            