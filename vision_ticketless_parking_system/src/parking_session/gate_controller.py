from src.parking_session.session_manager import SessionManager

class GateController:
    def process_exit(self, event_result):
        if not event_result:
            return None
    
        if event_result["type"] == "session_ended":
            return {
                "action": "OPEN_GATE",
                "plate": event_result["plate"],
            }
    
        return {
            "action": "DENY",
            "plate": event_result["plate"],
            "details": event_result,
        }
    