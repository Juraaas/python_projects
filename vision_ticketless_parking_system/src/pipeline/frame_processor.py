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
        self.track_memory = {}

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
            track_id = plate.get("track_id")

            crop = frame[y1:y2, x1:x2]

            if crop is None or crop.size == 0 or track_id is None:
                continue

            memory = self.track_memory.get(track_id, {
                "text": None,
                "conf": 0.0,
                "frames_seen": 0,
            })

            memory["frames_seen"] += 1
            self.track_memory[track_id] = memory

            if self.frame_count % self.OCR_EVERY_N == 0 and memory["frames_seen"] > 5:
                ocr_result = self.plate_ocr.read(crop)

                if ocr_result:
                    if ocr_result["confidence"] > memory["conf"]:
                        memory["text"] = ocr_result["text"]
                        memory["conf"] = ocr_result["confidence"]
                    
                    self.track_memory[track_id] = memory
            
            if memory["text"]:

                stable = self.stabilizer.update(
                    plate["track_id"],
                    memory["text"],
                )

                if stable:
                    if is_valid_plate(stable):
                        plate["text"] = stable
                        plate["ocr_conf"] = memory["conf"]

        events = self.registry.update(detected_plates)

        return vehicles, detected_plates, events
