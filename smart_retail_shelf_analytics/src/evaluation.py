import pandas as pd

class ShelfEvaluator:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)

        if "timestamp" in self.df.columns:
            self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        
        self._validate_schema()

    def _validate_schema(self):
        required_columns = [
            "occupied_slots",
            "total_slots",
            "occupancy_ratio",
            "avg_count",
            "low_stock_alert",
            "fps",
        ]

        missing = [c for c in required_columns if c not in self.df.columns]

        if missing:
            raise ValueError(
                f"Log file missing required columns: {missing}"
            )
        
    def basic_stats(self):
        counts = self.df["occupied_slots"]

        return {
            "frames_logged": len(self.df),
            "avg_count": counts.mean(),
            "std_count": counts.std(),
            "min_count": counts.min(),
            "max_count": counts.max(),
        }
    
    def fps_stats(self):
        fps = self.df["fps"]

        return {
            "avg_fps": fps.mean(),
            "std_fps": fps.std(),
            "min_fps": fps.min(),
            "max_fps": fps.max(),
        }
    
    def alert_stats(self):
        alerts = self.df["low_stock_alert"]
        alert_changes = alerts.diff().fillna(0)

        alert_starts = (alert_changes == 1).sum()
        alert_ends = (alert_changes == -1).sum()

        total_alert_frames = alerts.sum()

        return {
            "alert_activations": int(alert_starts),
            "alert_resolutions": int(alert_ends),
            "total_alert_frames": int(total_alert_frames),
            "alert_ratio": total_alert_frames / float(len(alerts)),
        }
    
    def stability_metrics(self):
        diffs = self.df["occupied_slots"].diff().abs()

        return {
            "avg_count_change": diffs.mean(),
            "max_count_jump": diffs.max(),
        }
    
    def flip_rate_stats(self):
        if "slot_flip_rate" not in self.df.columns:
            return {
                "avg_slot_flip_rate": None,
                "max_slot_flip_rate": None,
            }
        flip = self.df["slot_flip_rate"]
        
        return {
            "avg_slot_flip_rate": flip.mean(),
            "max_slot_flip_rate": flip.max(),
        }
    
    def pipeline_stats(self):
        fields = [
            "detection_time",
            "tracking_time",
            "stabilization_time",
            "spatial_time",
            "decision_time",
            "pipeline_time",
        ]

        stats = {}
        for f in fields:
            if f in self.df.columns:
                col = pd.to_numeric(self.df[f], errors="coerce")
                if col.notna().any():
                    stats[f] = col.mean()
                else:
                    stats[f] = None
        return stats
    
    def generate_report(self):
        report = {
            "basic": self.basic_stats(),
            "fps": self.fps_stats(),
            "alerts": self.alert_stats(),
            "stability": self.stability_metrics(),
            "slot_stability": self.flip_rate_stats(),
            "pipeline": self.pipeline_stats(),
        }
        return report