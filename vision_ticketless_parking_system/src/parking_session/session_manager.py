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
    
    def _find_matching_plate(self, plate, threshold=0.85):
        best_match = None
        best_score = 0.0

        with get_db() as db:
            sessions = db.query(ParkingSessionDB).filter_by(status="ACTIVE").all()

            for s in sessions:
                score = self._similarity(
                    self._normalize(plate),
                    self._normalize(s.plate),
                )
            
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
        matched_plate = self._find_matching_plate(plate)

        if matched_plate:
            plate = matched_plate

        with get_db() as db:
            session = (db.query(ParkingSessionDB).filter_by(plate=plate, status="ACTIVE").first())

            if not session:
                return None
            
            if session.payment_status == "paid":
                return {
                    "type": "payment_ignored",
                    "plate": plate,
                    "reason": "already_paid",
                }
            
            session.payment_status = "paid"
            session.amount_due = 0.0
            session.payment_time = time.time()

            db.commit()

        return {
            "type": "payment_confirmed",
            "plate": plate,
        }
    
    def _handle_exit(self, plate, timestamp):
        matched_plate = self._find_matching_plate(plate)

        if matched_plate:
            plate = matched_plate
        
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
        
            if timestamp - session.payment_time > self.grace_period_sec:
                session.payment_status = "unpaid"

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

            session.exit_time = timestamp
            session.status = "ENDED"
            db.commit()

        return {
            "type": "session_ended",
            "plate": plate,
            "session_id": session.session_id,
        }
            