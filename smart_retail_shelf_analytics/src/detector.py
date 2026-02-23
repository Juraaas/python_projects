from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.4):
        self.model = YOLO(model_path)
        self.conf_threshold=conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]

        detections = []
        for box in results.boxes:
            conf = float(box.conf[0])
            if conf < self.conf_threshold:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]

            detections.append({
                "bbox": (x1, y1, x2, y2),
                "label": label,
                "confidence": conf,
            })
        return detections
