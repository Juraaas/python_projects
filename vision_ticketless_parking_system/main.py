import cv2

from src.video_stream import VideoStream
from src.vehicle_detector import VehicleDetector
from src.plate_detector import PlateDetector
from src.utils.drawing import draw_detections, draw_plates_with_text
from src.plate_ocr import PlateOCR

def main():
    CONF_THRESHOLD = 0.4

    stream = VideoStream(source=0)

    vehicle_detector = VehicleDetector(conf_threshold=CONF_THRESHOLD)
    plate_detector = PlateDetector(conf_threshold=CONF_THRESHOLD)
    plate_ocr = PlateOCR(use_gpu=False)

    while True:
        ret, frame = stream.read()

        if not ret:
            break

        vehicles = vehicle_detector.detect(frame)

        detected_plates = []

        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle["bbox"]
            vehicle_roi = frame[y1:y2, x1:x2]
            det_plates = plate_detector.detect(vehicle_roi)
            for plate in det_plates:
                px1, py1, px2, py2 = plate["bbox"]

                plate_crop = vehicle_roi[py1:py2, px1:px2]
                ocr_result = plate_ocr.read(plate_crop)

                if ocr_result:
                    plate["text"] = ocr_result["text"]
                    plate["ocr_conf"] = ocr_result["confidence"]    

                plate["bbox"] = (
                    px1 + x1,
                    py1 + y1,
                    px2 + x1,
                    py2 + y1,
                )
                detected_plates.append(plate)

        draw_detections(frame, vehicles)
        draw_plates_with_text(frame, detected_plates)

        cv2.imshow("Vision parking Entry stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

