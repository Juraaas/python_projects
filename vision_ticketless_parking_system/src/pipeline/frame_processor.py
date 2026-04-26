from src.utils.plate_format import is_valid_plate
from src.queue.redis_client import redis_client
from src.queue.ocr_queue import enqueue_ocr
from src.pipeline.plate_identity_manager import PlateIdentityManager
import time

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
        self.MAX_MISSING_FRAMES = 30
        self.identity_manager = PlateIdentityManager()

    def get_ocr_events(self, track_id):
        key = f"ocr_stream:{track_id}"

        events = redis_client.lrange(key, 0, -1)

        if events:
            redis_client.delete(key)

        parsed = []

        for e in events:
            try:
                text, conf = e.split("|")
                parsed.append({
                    "text": text,
                    "confidence": float(conf)
                })
            except Exception as ex:
                print(f"[PARSE ERROR] {e} {ex}")

        return parsed

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

            memory = self.track_memory.get(track_id)
            if memory is None:
                memory = {
                    "stable_text": None,
                    "last_ocr_frame": 0,
                    "last_seen_frame": self.frame_count,
                }

            memory["last_seen_frame"] = self.frame_count

            ocr_events = self.get_ocr_events(track_id)

            for ocr_result in ocr_events:
                print(f"[OCR EVENT] track={track_id} -> {ocr_result}")
                stable = self.stabilizer.update(
                    track_id,
                    ocr_result["text"],
                    ocr_result["confidence"],
                )

                if stable and is_valid_plate(stable):
                    memory["stable_text"] = stable
            
            if self.frame_count - memory["last_ocr_frame"] >= self.OCR_EVERY_N:
                enqueue_ocr(track_id, crop)
                memory["last_ocr_frame"] = self.frame_count
                
            if memory.get("stable_text"):
                plate["text"] = memory["stable_text"]
            
                identity_id = self.identity_manager.match_or_create(
                    track_id,
                    memory["stable_text"],
                    self.frame_count
                )
                plate["identity_id"] = identity_id

                print(f"[PIPELINE FINAL] track={track_id} text={plate['text']} identity={identity_id}")
            else:
                print(f"[PIPELINE FINAL] track={track_id} text=None")

            self.track_memory[track_id] = memory

        for tid in list(self.track_memory.keys()):
            last_seen = self.track_memory[tid]["last_seen_frame"]

            if self.frame_count - last_seen > self.MAX_MISSING_FRAMES:
                del self.track_memory[tid]
            
        self.identity_manager.cleanup(self.frame_count)

        events = self.registry.update(detected_plates)

        return vehicles, detected_plates, events    