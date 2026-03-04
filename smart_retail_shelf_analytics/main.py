import cv2
import time
import argparse
import atexit
from src.detector import YOLODetector
from src.video_stream import VideoStream
from src.shelf_logic import ShelfMonitor
from src.logger import EventLogger
from src.tracker import ObjectTracker
from src.stabilizer import TrackStabilizer
from src.shelf_state import ShelfStateManager

def draw_detections(frame, objects):
    for obj in objects:
        x1, y1, x2, y2 = obj["bbox"]
        conf = obj["confidence"]
        label = obj.get("label", "obj")
        track_id = obj.get("track_id")

        text = f"{label}"
        if track_id is not None:
            text += f" | ID {track_id}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{text} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

def draw_fps(frame, fps):
    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

def draw_shelf_status(frame, shelf_state):
    cv2.putText(
        frame,
        f"Count: {shelf_state['current_count']} | Avg {shelf_state['avg_count']:.1f}",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2,
    )
    if shelf_state["low_stock_alert"]:
        cv2.putText(
        frame,
        "LOW STOCK ALERT",
        (10, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3,
    )
        
def draw_shelf_grid(frame, shelf_bbox, rows, cols, spatial_state=None):
    x1, y1, x2, y2 = shelf_bbox
    slot_width = (x2 - x1) / cols
    slot_height = (y2 - y1) / rows

    for r in range(rows):
        for c in range(cols):
            slot_index = r * cols + c

            sx1 = int(x1 + c * slot_width)
            sy1 = int(y1 + r * slot_height)
            sx2 = int(sx1 + slot_width)
            sy2 = int(sy1 + slot_height)

            occupied = False
            if spatial_state is not None:
                occupied = spatial_state["occupancy_map"][slot_index] == 1

            color = (0, 255, 0) if occupied else (255, 0, 0)

            cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), color, 2)
            cv2.putText(
                frame,
                f"{slot_index}",
                (sx1 + 5, sy1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
            )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Smart Retail Shelf Analytics"
    )
    parser.add_argument(
        "--mode",
        choices=["live", "offline"],
        default="live",
        help="Run mode",
    )
    parser.add_argument(
        "--video",
        type=str,
        default=None,
        help="Path to offline video file",
    )
    return parser.parse_args()

def main():
    args = parse_args()

    tracker_config = {
    "conf_threshold": 0.4,
    "max_age": 30,
    "min_hits": 3,
}

    monitor_config = {
        "min_stock": 3,
        "window_size": 10,
        "alert_delay": 20,
    }

    stabilizer_config = {
        "missing_tolerance": 20,
    }

    experiment_config = {
        "mode": args.mode,
        "tracker": tracker_config,
        "monitor": monitor_config,
        "detector": {
            "model": "YOLOv8",
            "confidence_filter": 0.4,
            "label": "cup"
        }
    }

    detector = YOLODetector()

    if args.mode == "live":
        print("Running in Live Mode")
        stream = VideoStream(source=0)
    elif args.mode == "offline":
        if args.video is None:
            raise ValueError("Offline mode requires --video path")
        print(f"Running Offline Mode: {args.video}")
        stream = VideoStream(source=args.video)

    prev_time = time.time()

    monitor = ShelfMonitor(**monitor_config)

    shelf_bbox = (80, 120, 560, 400)
    grid_rows = 1
    grid_cols = 4
    presence_threshold = 3
    absence_threshold = 5

    shelf_state_manager = ShelfStateManager(
        shelf_bbox=shelf_bbox,
        grid_rows=grid_rows,
        grid_cols=grid_cols,
        presence_threshold=presence_threshold,
        absence_threshold=absence_threshold
    )
    
    frame_id = 0
    ALLOWED_LABELS = ["cup"]

    use_tracker = True
    tracker = ObjectTracker(**tracker_config)
    stabilizer = TrackStabilizer(missing_tolerance=20)

    logger = EventLogger(experiment_config=experiment_config)
    atexit.register(logger.save_metadata)

    while True:
        ret, frame = stream.read()
        if not ret:
            break

        if args.mode == "offline":
            time.sleep(1 / 30)

        detections = detector.detect(frame)

        filtered_detections = [
            d for d in detections
            if d["confidence"] >= 0.4 and d["label"] in ALLOWED_LABELS
        ]

        if use_tracker:
            tracked_objects = tracker.update(filtered_detections)
            objects = stabilizer.update(tracked_objects, frame_id)
        else:
            objects = filtered_detections

        spatial_state = shelf_state_manager.update(objects)
        shelf_state = monitor.update(spatial_state)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time

        if logger.should_log(shelf_state):
            logger.log(frame_id, shelf_state, fps)
            
        frame_id += 1

        draw_detections(frame, objects)
        draw_fps(frame, fps)
        draw_shelf_status(frame, shelf_state)
        draw_shelf_grid(frame, shelf_bbox, grid_rows, grid_cols, spatial_state)

        cv2.imshow("Smart Retail - Detection MVP", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

