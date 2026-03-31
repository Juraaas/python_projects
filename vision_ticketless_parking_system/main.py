import cv2
import time
import requests

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
from src.pipeline.event_enricher import enrich_event
from src.db.database import Base, engine
from src.db import models

def resize_for_display(frame, width=1200):

    h, w = frame.shape[:2]

    scale = width / w

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(frame, (new_w, new_h))

def main():
    CONF_THRESHOLD = 0.4
    mode = "entry"

    cv2.namedWindow("Vision Parking System", cv2.WINDOW_NORMAL)

    stream = VideoStream(source=0)

    vehicle_detector = VehicleDetector(conf_threshold=CONF_THRESHOLD)
    plate_detector = PlateDetector(conf_threshold=0.2)
    entry_tracker = PlateTracker(conf_threshold=CONF_THRESHOLD, max_age=120)
    exit_tracker = PlateTracker(conf_threshold=CONF_THRESHOLD, max_age=120)
    plate_ocr = PlateOCR(use_gpu=True)
    entry_stabilizer = PlateTextStabilizer(window_size=15, min_votes=3)
    exit_stabilizer = PlateTextStabilizer(window_size=15, min_votes=3)
    entry_registry = PlateRegistry(exit_timeout=20, min_stable_frames=20)
    exit_registry = PlateRegistry(exit_timeout=20, min_stable_frames=20)
    event_logger = EventLogger("logging/logs")
    fps_counter = FPSCounter(window_size=30)

    entry_processor = FrameProcessor(
        vehicle_detector,
        plate_detector,
        entry_tracker,
        plate_ocr,
        entry_stabilizer,
        entry_registry,
    )

    exit_processor = FrameProcessor(
        vehicle_detector,
        plate_detector,
        exit_tracker,
        plate_ocr,
        exit_stabilizer,
        exit_registry,
    )

    Base.metadata.create_all(bind=engine)

    while True:

        ret, frame = stream.read()

        if not ret:
            break

        processor = entry_processor if mode == "entry" else exit_processor
        vehicles, plates, events = processor.process(frame)

        fps = fps_counter.update()

        for event in events:
            event = enrich_event(event, mode)

            print(f"[EVENT] {event['type']} -> {event['plate']}")

            event_logger.log_event(event)

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/event",
                    json=event,
                    timeout=0.5,
                )
                print(f"[API STATUS] {response.status_code}")
                if response.headers.get("content-type", "").startswith("application/json"):
                    print(f"[API RESPONSE] {response.json()}")
                else:
                    print(f"[API RAW] {response.text}")
            except Exception as e:
                print(f"[API ERROR] {e}")


        draw_detections(frame, vehicles)
        draw_plates_with_text(frame, plates)
        draw_fps(frame, fps)

        cv2.imshow(f"{mode.upper()} STREAM", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if key == ord("1"):
            mode = "entry"
            print(">>> SWITCHED TO ENTRY CAMERA")

        if key == ord("2"):
            mode = "exit"
            print(">>> SWITCHED TO EXIT CAMERA")

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

