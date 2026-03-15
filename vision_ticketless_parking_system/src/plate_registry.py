import time

class PlateRegistry:
    def __init__(self, exit_timeout=10):
        self.exit_timeout = exit_timeout
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
                self.active_tracks[track_id] = {
                    "plate": text,
                    "first_seen": current_time,
                    "last_seen": current_time,
                }

                self.parking_sessions[text] = {
                    "entry_time": current_time,
                    "track_id": track_id,
                }

                events.append({
                    "type": "vehicle_entered",
                    "plate": text,
                    "time": current_time,
                })
            else:
                self.active_tracks[track_id]["last_seen"] = current_time
        
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

