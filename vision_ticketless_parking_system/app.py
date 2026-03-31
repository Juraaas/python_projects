import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.system_state import system_state
from typing import Dict

app = FastAPI(title="Parking API")

session_manager = system_state.session_manager
gate_controller = system_state.gate_controller

class PaymentRequest(BaseModel):
    plate: str


class ExitRequest(BaseModel):
    plate: str


@app.get("/sessions/active")
def get_sessions():
    return list(session_manager.active_sessions.keys())


@app.get("/sessions/{plate}")
def get_session(plate: str):
    session = session_manager.active_sessions.get(plate)
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

    if event["type"] == "vehicle_exit_detected":
        matched_plate = None

        if result and "plate" in result:
            matched_plate = result["plate"]
        else:
            matched_plate = event["plate"]

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