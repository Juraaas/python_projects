import cv2

from src.video_stream import VideoStream
from src.vehicle_detector import VehicleDetector
from src.plate_detector import PlateDetector
from src.utils.drawing import draw_detections, draw_plates_with_text
from src.plate_ocr import PlateOCR
from src.plate_text_stabilizer import PlateTextStabilizer

def resize_for_display(frame, width=1200):

    h, w = frame.shape[:2]

    scale = width / w

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(frame, (new_w, new_h))

def main():
    CONF_THRESHOLD = 0.4
    frame_count = 0
    OCR_EVERY_N_FRAMES = 5

    cv2.namedWindow("Vision parking Entry stream", cv2.WINDOW_NORMAL)

    stream = VideoStream(source="data/test_2.mp4")

    vehicle_detector = VehicleDetector(conf_threshold=CONF_THRESHOLD)
    plate_detector = PlateDetector(conf_threshold=CONF_THRESHOLD)
    plate_ocr = PlateOCR(use_gpu=False)
    plate_stabilizer = PlateTextStabilizer(window_size=10)

    while True:
        ret, frame = stream.read()

        if not ret:
            break

        frame_count += 1

        vehicles = vehicle_detector.detect(frame)

        detected_plates = []

        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle["bbox"]
            vehicle_roi = frame[y1:y2, x1:x2]
            det_plates = plate_detector.detect(vehicle_roi)
            for plate in det_plates:
                px1, py1, px2, py2 = plate["bbox"]

                gx1 = px1 + x1
                gy1 = py1 + y1
                gx2 = px2 + x1
                gy2 = py2 + y1

                plate["bbox"] = (gx1, gy1, gx2, gy2)

                plate_crop = frame[gy1:gy2, gx1:gx2]
                if plate_crop is not None and plate_crop.size > 0:
                    debug_plate = cv2.resize(plate_crop, (300, 100))
                    cv2.imshow("DEBUG_plate_crop", debug_plate)

                ocr_result = None
                if frame_count % OCR_EVERY_N_FRAMES == 0:
                    ocr_result = plate_ocr.read(plate_crop)
                
                if ocr_result:
                    raw_text = ocr_result["text"]
                    stable_text = plate_stabilizer.update(
                        plate["bbox"],
                        raw_text,
                    )

                    if stable_text:
                        plate["text"] = stable_text
                        plate["ocr_conf"] = ocr_result["confidence"]    

                detected_plates.append(plate)

        draw_detections(frame, vehicles)
        draw_plates_with_text(frame, detected_plates)

        display_frame = resize_for_display(frame)

        cv2.imshow("Vision parking Entry stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

