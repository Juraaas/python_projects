from src.utils.plate_format import is_valid_plate

class FrameProcessor:
    def __init__(self,
                 vehicle_detector,
                 plate_detector,
                 plate_tracker,
                 plate_ocr,
                 stabilizer,
                 registry):
        self.vehicle_detector = vehicle_detector
        self.plate_detector = plate_detector
        self.plate_tracker = plate_tracker
        self.plate_ocr = plate_ocr
        self.stabilizer = stabilizer
        self.registry = registry

        self.frame_count = 0
        self.OCR_EVERY_N = 5

    def process(self, frame):
        self.frame_count += 1

        vehicles = self.vehicle_detector.detect(frame)
        detected_plates = []

        for vehicle in vehicles:
            x1, y1, x2, y2 = vehicle["bbox"]
            vehicle_roi = frame[y1:y2, x1:x2]

            plates = self.plate_detector.detect(vehicle_roi)
            for plate in plates:
                px1, py1, px2, py2 = plate["bbox"]

                gx1 = px1 + x1
                gy1 = py1 + y1
                gx2 = px2 + x1
                gy2 = py2 + y1

                plate["bbox"] = (gx1, gy1, gx2, gy2)
                detected_plates.append(plate)

        detected_plates = self.plate_tracker.update(detected_plates)

        for plate in detected_plates:
            x1, y1, x2, y2 = plate["bbox"]

            crop = frame[y1:y2, x1:x2]

            if crop is None or crop.size == 0:
                continue

            if self.frame_count % self.OCR_EVERY_N != 0:
                continue

            ocr_result = self.plate_ocr.read(crop)

            if not ocr_result:
                continue

            stable = self.stabilizer.update(
                plate["track_id"],
                ocr_result["text"],
            )

            if stable and is_valid_plate(stable):
                plate["text"] = stable
                plate["ocr_conf"] = ocr_result["confidence"]

        events = self.registry.update(detected_plates)

        return vehicles, detected_plates, events
