import json 
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class EventLogger:
    def __init__(
            self, 
            log_dir="src/logging/logs",
            base_filename="parking_events",
            max_bytes=5*1024*1024,
            backup_count=5,
        ):
        os.makedirs(log_dir, exist_ok=True)
        start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        log_file = os.path.join(
            log_dir,
            f"{base_filename}_{start_time}.log"
        )

        self.logger = logging.getLogger("parking_events")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
            )
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_event(self, event):
        log_record = {
            "event": event["type"],
            "plate": event["plate"],
            "timestamp": datetime.fromtimestamp(event["time"]).isoformat(),
            "camera": event["camera"],
        }

        self.logger.info(json.dumps(log_record))