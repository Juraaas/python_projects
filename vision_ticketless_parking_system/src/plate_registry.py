import time

class PlateRegistry:
    def __init__(self, exit_timeout=10, min_stable_frames=5):
        self.exit_timeout = exit_timeout
        self.min_stable_frames = min_stable_frames
        self.active_tracks = {}
        self.parking_sessions = {}
    
    def update(self, plates):
        current_time = time.time()
        events = []
        for plate in plates:
            track_id = plate.get("track_id")
            text = plate.get("text")

            if track_id is None or text is None:
                continue

            if track_id not in self.active_tracks:
                if text in self.parking_sessions:
                    continue

                self.active_tracks[track_id] = {
                    "plate": text,
                    "first_seen": current_time,
                    "last_seen": current_time,
                    "stable_count": 1,
                    "emitted": False,
                }
                continue

            track = self.active_tracks[track_id]
            track["last_seen"] = current_time

            if track["plate"] == text:
                track["stable_count"] += 1
            else:
                continue
            
            if (
                track["stable_count"] >= self.min_stable_frames
                and not track["emitted"]
                and text not in self.parking_sessions
            ):
                self.parking_sessions[text] = {
                    "entry_time": current_time,
                    "track_id": track_id,
                }

                events.append({
                    "type": "vehicle_entered",
                    "plate": text,
                    "time": current_time,
                    "camera": "entry",
                })
            
                track["emitted"] = True
        
        self._cleanup_tracks(current_time)

        return events
    
    def _cleanup_tracks(self, current_time):
        tracks_to_remove = []

        for track_id, data in self.active_tracks.items():
            if current_time - data["last_seen"] > self.exit_timeout:
                tracks_to_remove.append(track_id)
        for track_id in tracks_to_remove:
            del self.active_tracks[track_id]
    

    def get_active_vehicles(self):
        return list(self.parking_sessions.keys())

