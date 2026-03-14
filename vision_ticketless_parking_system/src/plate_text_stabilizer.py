from collections import defaultdict, Counter

class PlateTextStabilizer:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.history = defaultdict(list)

    def update(self, track_id, text):
        if track_id is None:
            return None
        if text is None or text == "":
            return None
        self.history[track_id].append(text)

        if len(self.history[track_id]) > self.window_size:
            self.history[track_id].pop(0)

        counter = Counter(self.history[track_id])
        stable_text, count = counter.most_common(1)[0]

        return stable_text