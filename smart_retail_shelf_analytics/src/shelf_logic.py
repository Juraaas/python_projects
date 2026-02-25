from collections import deque

class ShelfMonitor:
    def __init__(
        self,
        min_stock: int = 3,
        window_size: int = 10,
        alert_delay: int = 5,
        conf_threshold: float = 0.4,
        allowed_labels: list | None = None,
    ):
        """
        Shelf monitoring logic.

        :param min_stock: minimum acceptable number of products
        :param window_size: number of frames used for rolling average
        :param conf_threshold: confidence threshold for detections
        :param allowed_labels: optional list of allowed object classes
        """
        self.min_stock = min_stock
        self.window_size = window_size
        self.alert_delay = alert_delay
        self.conf_threshold = conf_threshold
        self.allowed_labels = allowed_labels

        self.count_history = deque(maxlen=window_size)
        self.low_stock_counter = 0

    def update(self, objects: list) -> dict:
        """
        Update shelf state based on detections from a single frame.

        Returns:
        dict:
        - current_count
        - avg_count
        - low_stock_alert
        """
        valid_objects = []

        for obj in objects:
            if obj["confidence"] < self.conf_threshold:
                continue

            if self.allowed_labels is not None:
                if "label" in obj and obj["label"] not in self.allowed_labels:
                    continue
            
            valid_objects.append(obj)

        if valid_objects and "track_id" in valid_objects[0]:
            current_count = len({obj["track_id"] for obj in valid_objects})
        else:
            current_count = len(valid_objects)
        
        self.count_history.append(current_count)
        avg_count = sum(self.count_history) / len(self.count_history)

        if avg_count < self.min_stock:
            self.low_stock_counter += 1
        else:
            self.low_stock_counter = 0
        
        low_stock_alert = self.low_stock_counter >= self.alert_delay

        return {
            "current_count": current_count,
            "avg_count": avg_count,
            "low_stock_alert": low_stock_alert,
            "low_stock_counter": self.low_stock_counter,
        }

