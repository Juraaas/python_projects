from src.db.database import SessionLocal, get_db
from src.db.models import ParkingSessionDB
from src.parking_session.session_manager import SessionManager

class GateController:
    def __init__(self):
        self.grace_period_sec = 60

    def process_exit(self, plate, timestamp):
        with get_db() as db:
            session = db.query(ParkingSessionDB).filter_by(plate=plate, status="ACTIVE").first()

            if not session:
                return None
        
            if session.payment_status != "paid":
                return {
                    "action": "DENY",
                    "plate": plate,
                    "reason": "not_paid",
                }
        
            if timestamp - session.payment_time > self.grace_period_sec:
                return {
                    "action": "DENY",
                    "plate": plate,
                    "reason": "grace_expired",
                }
        
        return {
            "action": "OPEN_GATE",
            "plate": plate,
        }