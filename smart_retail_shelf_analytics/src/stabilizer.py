def bbox_center(bbox):
    x1, y1, x2, y2 = bbox
    return((x1 + x2) / 2, (y1 + y2) / 2)

class TrackStabilizer:
    """
    Stabilizes tracking results by keeping recently lost tracks alive
    for a fixed period of time (missing-frame memory).

    Prevents object count flickering by short occlusions.

    """
    def __init__(self,
                 missing_tolerance=20,
                 reassociation_distance=80):
        """
        missing_tolerance:
            how many frames a track may be missing before being removed permamently

        memory:
            track_id -> {
            "last_seen": frame_id,
            "object": last known object dict
        }
        """
        self.missing_tolerance = missing_tolerance
        self.reassociation_distance = reassociation_distance

        self.memory = {}
        self.lost_tracks = {}
    
    def update(self, tracks, frame_id):
        stabilized_objects = []
        current_ids = set()

        for obj in tracks:
            new_center = bbox_center(obj["bbox"])
            reassigned_id = None

            for lost_id, lost_data in list(self.lost_tracks.items()):
                old_center = bbox_center(lost_data["object"]["bbox"])
                dist = (
                    (new_center[0] - old_center[0]) ** 2 +
                    (new_center[1] - old_center[1]) ** 2
                ) ** 0.5

                if dist < self.reassociation_distance:
                    reassigned_id = lost_id
                    break

            if reassigned_id is not None:
                obj["track_id"] = reassigned_id
                del self.lost_tracks[reassigned_id]

            track_id = obj["track_id"]
            current_ids.add(track_id)

            self.memory[track_id] = {
                "last_seen": frame_id,
                "object": obj.copy(),
            }

            stabilized_objects.append(obj)
        
        for track_id, data in list(self.memory.items()):
            if track_id in current_ids:
                continue
            frames_missing = frame_id - data["last_seen"]

            if frames_missing > self.missing_tolerance:
                self.lost_tracks[track_id] = data
                del self.memory[track_id]

        return stabilized_objects
