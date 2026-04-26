from collections import defaultdict

class PlateIdentityManager:
    def __init__(self, similarity_threshold=0.85, ttl=50):
        self.similarity_threshold = similarity_threshold
        self.ttl = ttl

        self.identities = {}
        self.track_to_identity = {}
        self.next_id = 1

    def _similarity(self, a, b):
        if not a or not b:
            return 0.0
        
        if a == b:
            return 1.0
        
        length = max(len(a), len(b))
        diff = sum(1 for x, y in zip(a, b) if x != y)

        return 1 - diff / length
    
    def match_or_create(self, track_id, text, frame_count):
        if track_id in self.track_to_identity:
            identity_id = self.track_to_identity[track_id]
            self.identities[identity_id]["last_seen_frame"] = frame_count
            return identity_id
        
        best_id = None
        best_score = 0

        for identity_id, data in self.identities.items():
            score = self._similarity(text, data["text"])

            if score > best_score and score >= self.similarity_threshold:
                best_score = score
                best_id = identity_id
            
        if best_id is None:
            best_id = self.next_id
            self.next_id += 1

            print(f"[IDENTITY NEW] id={best_id} ({text})")
        else:
            print(f"[IDENTITY MATCH] track={track_id} -> id={best_id} ({text})")

        self.identities[best_id] = {
            "text": text,
            "last_seen_frame": frame_count,
            "track_ids": self.identities.get(best_id, {}).get("track_ids", set())
        }

        self.identities[best_id]["track_ids"].add(track_id)
        self.track_to_identity[track_id] = best_id

        return best_id
        
    def cleanup(self, frame_count):
        to_delete = []

        for identity_id, data in self.identities.items():
            if frame_count - data["last_seen_frame"] > self.ttl:
                to_delete.append(identity_id)

        for identity_id in to_delete:
            print(f"[IDENTITY REMOVED] id={identity_id}")
            del self.identities[identity_id]

        self.track_to_identity = {
            tid: iid for tid, iid in self.track_to_identity.items()
            if iid in self.identities
        }