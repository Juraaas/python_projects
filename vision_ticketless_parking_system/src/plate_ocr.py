import cv2
import easyocr
import re

class PlateOCR:
    def __init__(self, use_gpu=True):
        self.reader = easyocr.Reader(
            ['en'],
            gpu=use_gpu
        )
    
    def read(self, plate_image):
        if plate_image is None or plate_image.size == 0:
            return None
        
        cv2.imshow("OCR_RAW_PLATE", plate_image)
        
        results = self.reader.readtext(plate_image)

        if len(results) == 0:
            return None
        
        best_text = ""
        best_conf = 0.0

        for bbox, text, conf in results:
            if conf > best_conf:
                best_text = text
                best_conf = conf
        
        return {
            "text": best_text,
            "confidence": float(best_conf),
        }
