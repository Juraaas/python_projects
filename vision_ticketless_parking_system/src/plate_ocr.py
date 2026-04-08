import cv2
import easyocr
import re

class PlateOCR:
    def __init__(self, use_gpu=True):
        self.reader = easyocr.Reader(
            ['en'],
            gpu=use_gpu
        )

    def _is_valid_plate(self, text):
        pattern = r'^[A-Z]{2,3}[A-Z0-9]{4,5}$'
        return re.match(pattern, text) is not None
    
    def _preprocess(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 17, 17)
        thresh = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
        return thresh
    
    def _pick_best(self, results):
        best_text = None
        best_conf = 0.0

        for _, text, conf in results:
            text = text.replace(" ", "").upper()
            if not self._is_valid_plate(text):
                continue
            
            if conf > best_conf:
                best_text = text
                best_conf = conf

        return best_text, best_conf

    
    def read(self, plate_image):
        if plate_image is None or plate_image.size == 0:
            return None
        
        cv2.imshow("OCR_RAW_PLATE", plate_image)
        
        raw_results = self.reader.readtext(plate_image)
        raw_text, raw_conf = self._pick_best(raw_results)

        processed = self._preprocess(plate_image)
        cv2.imshow("OCR_PREPROCESSED", processed)

        proc_results = self.reader.readtext(processed)
        proc_text, proc_conf = self._pick_best(proc_results)

        if raw_conf >= proc_conf:
            best_text = raw_text
            best_conf = raw_conf
            source = "RAW"
        else:
            best_text = proc_text
            best_conf = proc_conf
            source = "PREPROCESSED"

        if not best_text:
            return None

        print(f"[OCR] {best_text} ({best_conf:.2f}) from {source}")
        
        return {
            "text": best_text,
            "confidence": float(best_conf),
        }
