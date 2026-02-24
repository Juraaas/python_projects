import csv
import os
import time
from datetime import datetime

class EventLogger:
    def __init__(self,
                 output_path="logs/shelf_events.csv",
                 log_interval_sec=1.0):
        self.output_path = output_path
        self.log_interval_sec = log_interval_sec
        self.last_log_time = 0.0
        self.last_alert_state = None
        self._ensure_dir_exists()
        self._init_csv()
    
    def _ensure_dir_exists(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
    
    def _init_csv(self):
        if not os.path.exists(self.output_path):
            with open(self.output_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "frame_id",
                    "current_count",
                    "avg_count",
                    "low_stock_alert",
                    "fps",
                    "event_type",
                ])

    def should_log(self, shelf_state):
        now = time.time()

        alert_changed = (
            self.last_alert_state is None
            or shelf_state["low_stock_alert"] != self.last_alert_state
        )

        time_elapsed = (now - self.last_log_time) >= self.log_interval_sec

        return alert_changed or time_elapsed
    
    def log(self, frame_id, shelf_state, fps):

        now = time.time()
        event_type = "periodic"
        if (
            self.last_alert_state is None
            or shelf_state["low_stock_alert"] != self.last_alert_state
        ):
            event_type = "alert_change"
        
        with open(self.output_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                frame_id,
                shelf_state["current_count"],
                round(shelf_state["avg_count"], 2),
                int(shelf_state["low_stock_alert"]),
                round(fps, 2),
                event_type,
            ])
            
        self.last_log_time = now
        self.last_alert_state = shelf_state["low_stock_alert"]
