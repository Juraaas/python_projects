import cv2
import time
from src.detector import YOLODetector
from src.video_stream import VideoStream

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


def main():
    detector = YOLODetector()
    stream = VideoStream(source=0)

    prev_time = time.time()

    while True:
        ret, frame = stream.read()
        if not ret:
            break

        detections = detector.detect(frame)

        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        prev_time = curr_time

        draw_detections(frame, detections)
        draw_fps(frame, fps)

        cv2.imshow("Smart Retail - Detection MVP", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

