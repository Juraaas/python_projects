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
from src.config_loader import load_config

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
        "--config",
        type=str,
        default="configs/default.yaml",
        help="Path to configuration file"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    config = load_config(args.config)

    detector_config = config["detector"]
    tracker_config = config["tracker"]
    stabilizer_config = config["stabilizer"]
    monitor_config = config["monitor"]
    shelf_model_config = config["shelf_model"]
    logging_config = config["logging"]

    mode = config["mode"]
    ALLOWED_LABELS = detector_config["allowed_labels"]
    CONF_THRESHOLD = detector_config["confidence_threshold"]


    detector = YOLODetector()
    tracker = ObjectTracker(**tracker_config)
    stabilizer = TrackStabilizer(**stabilizer_config)
    monitor = ShelfMonitor(**monitor_config)
    shelf_state_manager = ShelfStateManager(**shelf_model_config)
    logger = EventLogger(log_interval_sec=logging_config["log_interval_sec"],
                         experiment_config=config)

    atexit.register(logger.save_metadata)

    if mode == "live":
        print("Running in Live Mode")
        stream = VideoStream(source=0)
    elif mode == "offline":
        video_path = config.get("video")
        if video_path is None:
            raise ValueError("Offline mode requires --video path")
        print(f"Running Offline Mode: {video_path}")
        stream = VideoStream(source=video_path)

    frame_id = 0
    prev_time = time.time()

    bbox = tuple(shelf_model_config["shelf_bbox"])
    rows = shelf_model_config["grid_rows"]
    cols = shelf_model_config["grid_cols"]

    while True:
        ret, frame = stream.read()
        pipeline_start = time.time()
        if not ret:
            break

        if mode == "offline":
            time.sleep(1 / 30)
        t0 = time.time()
        detections = detector.detect(frame)
        t1 = time.time()
        detection_time = t1 - t0
        filtered_detections = [
            d for d in detections
            if d["confidence"] >= CONF_THRESHOLD
            and d["label"] in ALLOWED_LABELS
        ]
        t0 = time.time()
        tracked_objects = tracker.update(filtered_detections)
        t1 = time.time()
        tracker_time = t1 - t0
        
        t0 = time.time()
        objects = stabilizer.update(tracked_objects, frame_id)
        t1 = time.time()
        stabilization_time = t1 - t0

        t0 = time.time()
        spatial_state = shelf_state_manager.update(objects)
        t1 = time.time()
        spatial_time = t1 - t0

        t0 = time.time()
        shelf_state = monitor.update(spatial_state)
        t1 = time.time()
        decision_time = t1 - t0

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time

        raw_count = len(objects)
        pipeline_time = time.time() - pipeline_start

        timings = {
            "detection_time": detection_time,
            "tracking_time": tracker_time,
            "stabilization_time": stabilization_time,
            "spatial_time": spatial_time,
            "decision_time": decision_time,
            "pipeline_time": pipeline_time,
        }
        if logger.should_log(shelf_state):
            logger.log(frame_id, shelf_state, fps, raw_count, timings)
            
        frame_id += 1

        draw_detections(frame, objects)
        draw_fps(frame, fps)
        draw_shelf_status(frame, shelf_state)
        draw_shelf_grid(frame,
                        bbox,
                        rows,
                        cols,
                        spatial_state)

        cv2.imshow("Smart Retail Shelf Analytics", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

