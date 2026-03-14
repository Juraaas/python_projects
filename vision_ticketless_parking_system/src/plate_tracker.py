import supervision as sv
import numpy as np

class PlateTracker:
    def __init__(self,
                 conf_threshold=0.4,
                 max_age=30):
        self.conf_threshold = conf_threshold
        self.max_age = max_age
        self.tracker = sv.ByteTrack(
            track_activation_threshold=conf_threshold,
            lost_track_buffer=max_age,
            frame_rate=30,
        )
        self.last_tracks = []
    
    def update(self, plates):
        if plates is None or len(plates) == 0:
            return self.last_tracks
        
        xyxy = []
        confidences = []

        for plate in plates:
            bbox = plate.get("bbox")
            conf = plate.get("confidence")

            if bbox is None or len(bbox) != 4:
                continue

            xyxy.append(bbox)
            confidences.append(conf)

        if len(xyxy) == 0:
            return self.last_tracks
        
        xyxy = np.array(xyxy, dtype=np.float32)
        confidences = np.array(confidences, dtype=np.float32)

        detections = sv.Detections(
            xyxy=xyxy,
            confidence=confidences,
            class_id=np.zeros(len(xyxy))
        )

        tracked = self.tracker.update_with_detections(detections)
        tracked_plates = []

        for plate, track_id in zip(plates, tracked.tracker_id):
            plate["track_id"] = int(track_id)
            tracked_plates.append(plate)
        self.last_tracks = tracked_plates

        return tracked_plates
