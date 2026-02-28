import cv2

class VideoStream:
    def __init__(self, source=0):
        """
        Unified video source.

        source:
            0          -> webcam
            "file.mp4" -> video file
        """
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {source}")
        
        self.is_file = isinstance(source, str)
    
    def read(self):
        ret, frame = self.cap.read()

        if not ret and self.is_file:
            return False, None
        
        return ret, frame
    
    def release(self):
        self.cap.release()