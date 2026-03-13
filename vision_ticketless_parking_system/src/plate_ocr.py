import cv2
import easyocr
import re

class PlateOCR:
    def __init__(self, use_gpu=False):
        self.reader = easyocr.Reader(
            ['en'],
            gpu=use_gpu
        )
    
    def read(self, plate_image):
        if plate_image is None or plate_image.size == 0:
            return None
        
        results = self.reader.readtext(plate_image)

        if len(results) == 0:
            return None
        
        best_text = ""
        best_conf = 0.0

        for bbox, text, conf in results:
            if conf > best_conf:
                best_text = text
                best_conf = conf
        
        best_text = best_text.upper()
        best_text = re.sub(r'[^A-Z0-9]', '', best_text)

        if best_conf < 0.5:
            return None
        
        return {
            "text": best_text,
            "confidence": float(best_conf),
        }
