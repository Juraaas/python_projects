# Vision Ticketless Parking System

A **real-time ANPR (Automatic Number Plate Recognition) system** for automated parking management — no physical tickets, no attendants. Built end-to-end with computer vision, object tracking, temporal OCR stabilization, and an event-driven backend.

---

## The Problem

Manual parking management is labor-intensive, error-prone, and hard to scale. Physical tickets get lost, OCR readings flicker under motion blur, and tracking IDs drift across frames — making it difficult to reliably associate a vehicle with its session.

This project addresses all of that: a fully automated pipeline from camera frame to gate decision, with robust identity resolution at its core.

---

## How It Works

```
Video Stream → Detection + Tracking → Async OCR → Temporal Stabilization
     → Event Generation → Session Management → Billing → Gate Decision → API
```

Two main layers work together: a **computer vision pipeline** responsible for detecting vehicles, recognizing plates, and generating structured events — and a **backend logic layer** that manages session lifecycle, calculates fees, and controls gate decisions.

---

## Key Design Decisions

**Plate identity abstraction** — instead of relying on unstable `track_id` values (which drift due to tracking fragmentation), the system assigns persistent `identity_id` based on stabilized OCR output. This eliminates duplicate session creation caused by ID switches mid-session.

**Temporal OCR stabilization** — a custom `PlateTextStabilizer` module aggregates plate readings over a sliding window using character-level majority voting, dramatically reducing noise from motion blur and partial occlusions. Stable text — not raw frame output — is used as the primary input for identity resolution.

**Async OCR pipeline** — OCR is offloaded from the frame processing loop to a Redis-backed worker system. This keeps the video pipeline non-blocking, stabilizes FPS, and makes OCR compute independently scalable.

**Stateless gate controller** — gate decisions (`OPEN_GATE` / `DENY`) are derived purely from `SessionManager` output, keeping the controller decoupled from business logic and easy to test.

---

## System Architecture

### Computer Vision Pipeline
- YOLOv8 vehicle detection with ROI-based plate localization inside each vehicle bounding box
- Fine-tuned YOLO model for license plate detection
- ByteTrack object tracking with track-level temporal association
- EasyOCR with alphanumeric normalization and confidence scoring
- Frame skipping for OCR performance without affecting detection

### Parking Event System (`PlateRegistry`)
Converts stabilized detections into structured events, deduplicates entries, and maintains active track state:

```json
{
  "type": "vehicle_entered",
  "plate": "GD1234A",
  "camera": "entry"
}
```

### Session Lifecycle
```
ENTRY → ACTIVE → PAID → EXIT → ENDED
```

Each session stores: license plate, entry/exit timestamps, payment status, billing amount, and session ID.

Edge cases handled: duplicate entries (cooldown logic), OCR mismatches (fuzzy matching), expired payments (grace period), re-payment after expiration.

### REST API (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/sessions/active` | List all active sessions |
| `GET` | `/sessions/{plate}` | Get session by plate |
| `POST` | `/payment` | Register payment |
| `POST` | `/exit` | Process vehicle exit |

### Async OCR Queue

```
FrameProcessor → enqueue crop → Redis Queue → OCR Worker → Redis Stream → Stabilizer
```

OCR results are streamed back asynchronously and aggregated in the stabilizer for temporal consistency, completely decoupled from the video processing loop.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Vehicle & plate detection | YOLOv8 (fine-tuned) |
| OCR | EasyOCR |
| Object tracking | ByteTrack |
| Async queue | Redis |
| Backend / API | FastAPI |
| Database | SQLite |
| Event logging | JSON structured logs (rotating) |

---

## Performance (CPU, lightweight models)

| Component | Performance |
|---|---|
| Vehicle Detection | ~40–60 FPS |
| Plate Detection | Real-time |
| OCR | Optimized via frame skipping |
| Tracking | Negligible overhead |

---

## Project Structure

```
vision_ticketless_parking_system/
│
├── db/
│   ├── database.py
│   └── models.py
│
├── src/
│   ├── video_stream.py
│   ├── vehicle_detector.py
│   ├── plate_detector.py
│   ├── plate_ocr.py
│   ├── plate_registry.py
│   ├── plate_text_stabilizer.py
│   │
│   ├── utils/
│   │   ├── drawing.py
│   │   ├── plate_format.py
│   │   └── fps_counter.py
│   │
│   ├── pipeline/
│   │   ├── event_enricher.py
│   │   └── frame_processor.py
│   │
│   ├── queue/
│   │   ├── ocr_queue.py
│   │   └── redis_client.py
│   │
│   ├── workers/
│   │   └── ocr_worker.py
│   │
│   ├── logging/
│   │   └── event_logger.py
│   │
│   └── parking_session/
│       ├── session_manager.py
│       ├── billing_engine.py
│       └── gate_controller.py
│
├── app.py
├── main.py
├── requirements.txt
├── train_plate_detector.py
└── parking.db
```

---

## Current Limitations

- Single-process architecture (no horizontal scaling)
- SQLite (not suitable for concurrent writes at scale)
- Synchronous API
- No authentication layer

---

## Roadmap

- PostgreSQL migration
- Full async event pipeline
- Microservice architecture
- Admin dashboard
- Scalable worker-based OCR processing
