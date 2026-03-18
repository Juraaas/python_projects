class GateController:
    def __init__(self, session_manager):
        self.session_manager = session_manager

    def process_exit(self, plate, timestamp):
        result = self.session_manager._handle_exit(plate, timestamp)

        if not result:
            return None
        
        if result["type"] == "session_ended":
            return {
                "action": "OPEN_GATE",
                "plate": plate,
            }
        
        return {
            "action": "DENY",
            "plate": plate,
            "details": result,
        }