import pandas as pd

class ShelfEvaluator:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)

        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

    def basic_stats(self):
        stats = {
            "frames_logged": len(self.df),
            "avg_count": self.df["current_count"].mean(),
            "std_count": self.df["current_count"].std(),
            "min_count": self.df["current_count"].min(),
            "max_count": self.df["current_count"].max(),
        }
        return stats
    
    def fps_stats(self):
        return {
            "avg_fps": self.df["fps"].mean(),
            "std_fps": self.df["fps"].std(),
            "min_fps": self.df["fps"].min(),
            "max_fps": self.df["fps"].max(),
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
        diffs = self.df["current_count"].diff().abs()

        return {
            "avg_count_change": diffs.mean(),
            "max_count_jump": diffs.max(),
        }
    
    def generate_report(self):
        report = {
            "basic": self.basic_stats(),
            "fps": self.fps_stats(),
            "alerts": self.alert_stats(),
            "stability": self.stability_metrics(),
        }
        return report