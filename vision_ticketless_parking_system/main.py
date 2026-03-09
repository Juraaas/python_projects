import cv2

from src.video_stream import VideoStream
from src.vehicle_detector import VehicleDetector
from src.utils.drawing import draw_detections

def main():
    stream = VideoStream(source="data/test_car.mp4")
    detector = VehicleDetector(conf_threshold=0.4)

    while True:
        ret, frame = stream.read()

        if not ret:
            break

        vehicles = detector.detect(frame)

        draw_detections(frame, vehicles)

        cv2.imshow("Vision parking Entry stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

