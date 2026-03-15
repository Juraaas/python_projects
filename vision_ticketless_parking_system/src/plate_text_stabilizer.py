from collections import defaultdict, Counter

class PlateTextStabilizer:
    def __init__(self, window_size=10, min_votes=3):
        self.window_size = window_size
        self.min_votes = min_votes
        self.history = defaultdict(list)

    def update(self, track_id, text):
        if track_id is None:
            return None
        
        if text is None or text == "":
            return None
        
        text = text.replace(" ", "").upper()

        self.history[track_id].append(text)

        if len(self.history[track_id]) > self.window_size:
            self.history[track_id].pop(0)

        if len(self.history[track_id]) < self.min_votes:
            return None

        return self._character_vote(self.history[track_id])
    
    def _character_vote(self, texts):
        if len(texts) == 0:
            return None
        
        max_len = max(len(t) for t in texts)
        result = []

        for i in range(max_len):
            chars = []
            for t in texts:
                if len(t) > i:
                    chars.append(t[i])
            
            if len(chars) == 0:
                continue

            counter = Counter(chars)
            best_char, _ = counter.most_common(1)[0]

            result.append(best_char)
        
        return "".join(result)