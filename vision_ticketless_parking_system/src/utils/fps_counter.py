import time
from collections import deque


class FPSCounter:
    def __init__(self, window_size=30):
        self.timestamps = deque(maxlen=window_size)

    def update(self):
        now = time.time()
        self.timestamps.append(now)

        if len(self.timestamps) < 2:
            return 0.0
        
        elapsed = self.timestamps[-1] - self.timestamps[0]
        fps = (len(self.timestamps) - 1) / elapsed

        return fps