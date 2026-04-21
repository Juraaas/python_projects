from rq import Queue
from src.queue.redis_client import redis_client
import pickle
import base64

ocr_queue = Queue("ocr", connection=redis_client)

def enqueue_ocr(track_id, crop):
    data = base64.b64encode(pickle.dumps(crop)).decode()

    ocr_queue.enqueue(
        "src.workers.ocr_worker.process_ocr",
        track_id,
        data,
    )