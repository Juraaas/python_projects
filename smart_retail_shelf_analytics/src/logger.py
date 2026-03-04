import csv
import os
import time
import json
from datetime import datetime

class EventLogger:
    def __init__(self,
                 output_dir="logs",
                 log_interval_sec=1.0,
                 experiment_config=None):
        self.log_interval_sec = log_interval_sec
        self.last_log_time = 0.0
        self.last_alert_state = None
        self.run_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_path = os.path.join(
            output_dir,
            f"experiment_{self.run_id}.csv"
        )
        self.experiment_config = experiment_config or {}
        self._ensure_dir_exists()
        self._init_csv()

        print(f"[LOGGER] Experiment started: {self.run_id}")
        print(f"[LOGGER] Logging to: {self.output_path}")

    
    def _ensure_dir_exists(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
    
    def _init_csv(self):
        if not os.path.exists(self.output_path):
            with open(self.output_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "frame_id",
                    "raw_detection_count",
                    "occupied_slots",
                    "total_slots",
                    "occupancy_ratio",
                    "avg_count",
                    "low_stock_alert",
                    "low_stock_counter",
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
    
    def log(self, frame_id, shelf_state, fps, raw_count):

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
                raw_count,
                shelf_state["current_count"],
                shelf_state["total_slots"],
                round(shelf_state["occupancy_ratio"], 3),
                round(shelf_state["avg_count"], 2),
                int(shelf_state["low_stock_alert"]),
                round(fps, 2),
                event_type,
            ])
            
        self.last_log_time = now
        self.last_alert_state = shelf_state["low_stock_alert"]

    def save_metadata(self):
        metadata_path = self.output_path.replace(".csv", "_metadata.json")

        metadata = {
            "run_id": self.run_id,
            "created_at": datetime.utcnow().isoformat(),
            "log_interval_sec": self.log_interval_sec,
            "experiment_config": self.experiment_config,
        }

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

        print(f"[LOGGER] Metadata saved: {metadata_path}")
