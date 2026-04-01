import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.parking_session.session_manager import SessionManager
from src.parking_session.gate_controller import GateController
from typing import Dict
from src.db.database import SessionLocal, get_db
from src.db.models import ParkingSessionDB

app = FastAPI(title="Parking API")

session_manager = SessionManager()
gate_controller = GateController()

class PaymentRequest(BaseModel):
    plate: str


class ExitRequest(BaseModel):
    plate: str


@app.get("/sessions/active")
def get_sessions():
    with get_db() as db:
        sessions = db.query(ParkingSessionDB).filter_by(status="ACTIVE").all()
        return [s.plate for s in sessions]


@app.get("/sessions/{plate}")
def get_session(plate: str):
    with get_db() as db:
        session = db.query(ParkingSessionDB).filter_by(plate=plate, status="ACTIVE").first()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        now = time.time()
        
        if session.amount_due > 0:
            fee = session.amount_due
        else:
            fee = session_manager.billing.calculate_fee(
                session.entry_time,
                now,
            )
        return {"plate": plate, "amount_due": fee}


@app.post("/payment")
def make_payment(request: PaymentRequest):
    result = session_manager.handle_event({
        "type": "payment_confirmed",
        "plate": request.plate,
        "time": time.time(),
    })
    if not result:
        raise HTTPException(status_code=404, detail=f"No active session for plate {request.plate}")
    print(f"[API PAYMENT] {result}")
    return result


@app.post("/exit")
def try_exit(request: ExitRequest):
    decision = gate_controller.process_exit(
        request.plate,
        time.time(),
    )
    if not decision:
        raise HTTPException(status_code=404, detail=f"No active session for plate {request.plate}")
    print(f"[API EXIT] {decision}")
    return decision

@app.post("/event")
def ingest_event(event: Dict):
    matched_plate = session_manager._find_matching_plate(event["plate"]) or event["plate"]
    if event["type"] == "vehicle_exit_detected":
        decision = gate_controller.process_exit(
            matched_plate,
            event["time"],
        )
        result = session_manager.handle_event(event)
        return {
            "event_result": result,
            "gate_decision": decision,
        }
    result = session_manager.handle_event(event)
    return {"event_result": result}