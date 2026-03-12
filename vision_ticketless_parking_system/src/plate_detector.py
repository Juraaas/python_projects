from ultralytics import YOLO

class PlateDetector:
    def __init__(self,
                 model_path="models/plate_detector/best.pt",
                 conf_threshold=0.4):
        self.model = YOLO(model_path, task="detect")
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        plates = []

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                plates.append({
                    "bbox": (x1, y1, x2, y2),
                    "label": "plate",
                    "confidence": conf,
                })
        return plates
        