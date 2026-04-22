import numpy as np
from collections import defaultdict, Counter

class PlateTextStabilizer:
    def __init__(
            self, 
            window_size=10, 
            min_votes=3,
            min_confidence=0.6,
            stable_threshold=0.7,
            ):
        self.window_size = window_size
        self.min_votes = min_votes
        self.min_confidence = min_confidence
        self.stable_threshold = stable_threshold
        self.history = defaultdict(list)

    def update(self, track_id, text, confidence=None):
        if track_id is None:
            return None
        
        if text is None or text == "":
            return None
        
        text = text.replace(" ", "").upper()

        if confidence is None:
            confidence = 0.5

        if confidence < self.min_confidence:
            return None

        self.history[track_id].append((text, confidence))

        if len(self.history[track_id]) > self.window_size:
            self.history[track_id].pop(0)

        if len(self.history[track_id]) < self.min_votes:
            return None

        stable_text, score = self._vote(self.history[track_id])

        if score >= self.stable_threshold:
            return stable_text
        return None
    
    def _vote(self, items):
        texts = [t for t, _ in items]
        confs = [c for _, c in items]
        
        length_counter = Counter(len(t) for t in texts)
        target_len, _ = length_counter.most_common(1)[0]

        filtered = [(t, c) for t, c in items if len(t) == target_len]

        if len(filtered) == 0:
            return None, 0
        
        result = []
        scores = []

        for i in range(target_len):
            char_votes = {}
            for t, c in filtered:
                ch = t[i]
                char_votes[ch] = char_votes.get(ch, 0) + c

            best_char = max(char_votes.items(), key=lambda x: x[1])
            result.append(best_char[0])

            total = sum(char_votes.values())
            scores.append(best_char[1] / total if total > 0 else 0)

        final_text = "".join(result)
        final_score = np.mean(scores)
        
        return final_text, final_score