import supervision as sv
import numpy as np

class ObjectTracker:
    def __init__(self,
                 conf_threshold=0.4,
                 max_age=30,
                 min_hits=3,
        ):
        self.conf_threshold = conf_threshold
        self.max_age = max_age
        self.min_hits = min_hits

        self.tracker = sv.ByteTrack(
            track_activation_threshold=conf_threshold,
            lost_track_buffer=max_age,
            minimum_matching_threshold=0.8,
            frame_rate=30,
        )
        self.last_tracks = []
    
    def update(self, detections):
        """
        detections: list of dicts from YOLODetector
        returns: list of tracked objects with IDs
        """
        if detections is None or len(detections) == 0:
            return self.last_tracks
        
        xyxy = []
        confidences = []
        class_ids = []

        for det in detections:
            bbox = det.get("bbox")
            conf = det.get("confidence")
            
            if bbox is None or conf is None:
                continue

            if len(bbox) != 4:
                continue

            xyxy.append(bbox)
            confidences.append(conf)
            class_ids.append(0) # works only with single class
        
        if len(xyxy) == 0:
            return self.last_tracks
        
        xyxy = np.array(xyxy, dtype=np.float32)
        confidences = np.array(confidences, dtype=np.float32)
        class_ids = np.array(class_ids, dtype=np.int32)

        detections_sv = sv.Detections(
            xyxy=xyxy,
            confidence=confidences,
            class_id=class_ids,
        )
        
        tracked = self.tracker.update_with_detections(detections_sv)

        tracks = []
        for i in range(len(tracked)):
            tracks.append({
                "track_id": int(tracked.tracker_id[i]),
                "bbox": tracked.xyxy[i].astype(int).tolist(),
                "confidence": float(tracked.confidence[i]),
                "label": "cup",
            })
        self.last_tracks = tracks

        return tracks
    
    def predict(self):
        """
        Called when detection is skipped. Keeps existing tracks
        alive without new detections.
        """
        return self.last_tracks
    
    def get_config(self):
        return {
            "conf_threshold": self.conf_threshold,
            "max_age": self.max_age,
            "min_hits": self.min_hits,
            "algorithm": "ByteTrack",
        }
