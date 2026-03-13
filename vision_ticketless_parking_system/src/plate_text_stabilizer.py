from collections import defaultdict, Counter

class PlateTextStabilizer:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.history = defaultdict(list)

    def update(self, plate_bbox, text):
        key = tuple(plate_bbox)

        if text is None or text == "":
            return None
        self.history[key].append(text)

        if len(self.history[key]) > self.window_size:
            self.history[key].pop(0)

        counter = Counter(self.history[key])
        stable_text, count = counter.most_common(1)[0]

        return stable_text