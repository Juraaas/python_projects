import cv2
import time
from src.detector import YOLODetector
from src.video_stream import VideoStream
from src.shelf_logic import ShelfMonitor
from src.logger import EventLogger

def draw_detections(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = det["label"]
        conf = det["confidence"]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{label} {conf:.2f}",
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


def main():
    detector = YOLODetector()
    stream = VideoStream(source=0)

    prev_time = time.time()

    monitor = ShelfMonitor(
    min_stock=3,
    window_size=10,
    alert_delay=20,
    conf_threshold=0.4,
    allowed_labels=["cup"]
)
    
    logger = EventLogger(output_path="logs/shelf_events.csv")
    frame_id = 0

    while True:
        ret, frame = stream.read()
        if not ret:
            break

        detections = detector.detect(frame)
        shelf_state = monitor.update(detections)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time

        if logger.should_log(shelf_state):
            logger.log(frame_id, shelf_state, fps)
            
        frame_id += 1

        draw_detections(frame, detections)
        draw_fps(frame, fps)
        draw_shelf_status(frame, shelf_state)

        cv2.imshow("Smart Retail - Detection MVP", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

