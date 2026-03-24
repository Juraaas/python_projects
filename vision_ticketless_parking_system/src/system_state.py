from src.parking_session.session_manager import SessionManager
from src.parking_session.gate_controller import GateController

class SystemState:
    def __init__(self):
        self.session_manager = SessionManager()
        self.gate_controller = GateController(self.session_manager)

system_state = SystemState()