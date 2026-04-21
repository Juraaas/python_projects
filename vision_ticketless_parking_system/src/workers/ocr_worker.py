import pickle
import base64
from src.queue.redis_client import redis_client
from src.plate_ocr import PlateOCR
import numpy as np


ocr = PlateOCR(use_gpu=True)

def process_ocr(track_id, crop_data):
    crop = pickle.loads(base64.b64decode(crop_data))
    crop = np.ascontiguousarray(crop)

    result = ocr.read(crop)

    if result:
        payload = f"{result['text']}|{result['confidence']}"

        key = f"ocr_stream:{track_id}"

        redis_client.rpush(key, payload)
        redis_client.expire(key, 5)

        print(f"[REDIS WRITE] {key} -> {payload}")