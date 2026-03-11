from ultralytics import YOLO

class VehicleDetector:
    def __init__(self, model_path="models/yolov8n.pt", conf_threshold=0.4):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

        self.vehicle_classes = {
            "car",
            "bus",
            "truck",
            "motorcycle",
        }

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        vehicles = []
        
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    continue

                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]

                if label in self.vehicle_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    vehicles.append({
                        "bbox": (x1, y1, x2, y2),
                        "label": label,
                        "confidence": conf,
                    })
        return vehicles
