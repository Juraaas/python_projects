from collections import deque

class ShelfMonitor:
    def __init__(
        self,
        min_stock: int = 3,
        window_size: int = 10,
        alert_delay: int = 5,
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

        self.count_history = deque(maxlen=window_size)
        self.low_stock_counter = 0

    def update(self, spatial_state: dict) -> dict:
        """
        Update shelf state based on spatial_state (slot-based).

        spatial_state contains:
        - occupied slots
        - total slots
        - occupancy_ratio
        - occupancy_map
        """
        current_count = spatial_state["occupied_slots"]
        
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
            "occupancy_ratio": spatial_state["occupancy_ratio"],
            "occupancy_map": spatial_state["occupancy_map"],
            "total_slots": spatial_state["total_slots"],
        }

