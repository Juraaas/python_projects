import cv2

class VideoStream:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open video source")
    
    def read(self):
        ret, frame = self.cap.read()
        return ret, frame
    
    def release(self):
        self.cap.release()