import cv2
from typing import Union

class VideoStream:
    def __init__(self, source: Union[int, str] = 0):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {self.source}")
        
        print(f"[VideoStream] Source opened: {self.source}")
        
        self.is_file = isinstance(self.source, str)
        
    def read(self):
        ret, frame = self.cap.read()

        if not ret and self.is_file:
            return False, None
        return ret, frame
    
    def release(self):
        self.cap.release()
        