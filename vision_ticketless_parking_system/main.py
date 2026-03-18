import cv2
import time

from src.video_stream import VideoStream
from src.vehicle_detector import VehicleDetector
from src.plate_detector import PlateDetector
from src.utils.drawing import draw_detections, draw_plates_with_text, draw_fps
from src.plate_ocr import PlateOCR
from src.plate_text_stabilizer import PlateTextStabilizer
from src.plate_tracker import PlateTracker
from src.plate_registry import PlateRegistry
from src.pipeline.frame_processor import FrameProcessor
from src.logging.event_logger import EventLogger
from src.utils.fps_counter import FPSCounter
from src.parking_session.session_manager import SessionManager
from src.parking_session.gate_controller import GateController

def resize_for_display(frame, width=1200):

    h, w = frame.shape[:2]

    scale = width / w

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(frame, (new_w, new_h))

def main():
    CONF_THRESHOLD = 0.4

    cv2.namedWindow("Vision parking Entry stream", cv2.WINDOW_NORMAL)

    stream = VideoStream(source=0)

    vehicle_detector = VehicleDetector(conf_threshold=CONF_THRESHOLD)
    plate_detector = PlateDetector(conf_threshold=0.2)
    plate_tracker = PlateTracker(conf_threshold=CONF_THRESHOLD, max_age=120)
    plate_ocr = PlateOCR(use_gpu=True)
    plate_stabilizer = PlateTextStabilizer(window_size=15, min_votes=3)
    plate_registry = PlateRegistry(exit_timeout=20, min_stable_frames=20)
    event_logger = EventLogger("logging/logs/parking_events.log")
    fps_counter = FPSCounter(window_size=30)
    session_manager = SessionManager()
    gate_controller = GateController(session_manager)

    processor = FrameProcessor(
        vehicle_detector,
        plate_detector,
        plate_tracker,
        plate_ocr,
        plate_stabilizer,
        plate_registry,
    )

    while True:
        ret, frame = stream.read()

        if not ret:
            break

        vehicles, plates, events = processor.process(frame)

        fps = fps_counter.update()

        for event in events:
            event["camera"] = "entry_cam_1"

            print(f"[EVENT] {event['type']} -> {event['plate']}")

            event_logger.log_event(event)

            session_event = session_manager.handle_event(event)

            if session_event:
                print(f"[SESSION] {session_event}")

            print(f"[ACTIVE SESSIONS]: {list(session_manager.active_sessions.keys())}")



        draw_detections(frame, vehicles)
        draw_plates_with_text(frame, plates)
        draw_fps(frame, fps)

        # display_frame = resize_for_display(frame)

        cv2.imshow("Vision parking Entry stream", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if key == ord("e"):
            for plate in list(session_manager.active_sessions.keys()):
                decision = gate_controller.process_exit(
                    plate,
                    time.time(),
                )
                print(f"[GATE] {decision}")

        if key == ord("p"):
            for plate in list(session_manager.active_sessions.keys()):
                payment_event = session_manager.handle_event({
                    "type": "payment_confirmed",
                    "plate": plate,
                    "time": time.time(),
                })
                print(f"[PAYMENT] {payment_event}")

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

