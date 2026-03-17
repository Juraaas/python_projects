from collections import defaultdict, Counter

class PlateTextStabilizer:
    def __init__(self, window_size=10, min_votes=3):
        self.window_size = window_size
        self.min_votes = min_votes
        self.history = defaultdict(list)

    def _normalize_char(self, c):

        mapping = {
            '0': 'O', 'O': 'O',
            '1': 'I', 'I': 'I',
            '5': 'S', 'S': 'S',
        }
        return mapping.get(c, c)

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
        
        length_counter = Counter(len(t) for t in texts)
        target_len, _ = length_counter.most_common(1)[0]

        filtered_texts = [t for t in texts if len(t) == target_len]
        result = []

        for i in range(target_len):
            chars = []
            for t in filtered_texts:
                c = t[i]
                #c = self._normalize_char(c)
                chars.append(c)

            counter = Counter(chars)
            best_char, _ = counter.most_common(1)[0]

            result.append(best_char)
        
        return "".join(result)