# Vision Ticketless Parking System

End-to-end **real-time ANPR (Automatic Number Plate Recognition) system** for automated parking management without physical tickets.

The system combines **computer vision, tracking, temporal OCR stabilization, and event-driven backend logic** to simulate real-world parking infrastructure.


---

## Project Motivation

Manual parking management with tickets or attendants is:
- labor-intensive
- error-prone
- difficult to scale for busy locations
- hard to integrate with automated payment systems

This project aims to build a **modern, automated parking system** that:
- detects vehicles in real time
- recognizes license plates under noisy conditions
- manages parking lifecycle in a session-bassed manner
- calculates fees dynamically
- exposes system state via API
- simulates real-world gate control decisions


---

## System Overview

The system consists of two main layers:

### 1. Computer Vision Pipeline
Responsible for:
- vehicle detection
- license plate detection
- object tracking
- OCR recognition
- temporal stabilization of plate text
- generating structured events

### 2. Backend Logic (State + API)
Responsible for:
- session lifecycle management
- billing engine
- payment handling
- gate control logic
- API interface
- database connection

---

## Core components

### Vehicle & Plate Detection
- YOLOv8-based detection pipeline
- ROI-based plate detection inside vehicle bbox
- confidence filtering + real-time exe
- fine-tuned YOLO model for plates
- global coordinate reconstruction

### OCR Recognition (EasyOCR)
- alphanumeric normalization
- confidence scoring
- frame skipping for performance

### Temporal OCR Stabilization
Custom module: `PlateTextStabilizer`

- sliding window aggregation
- character-level majority voting
- noise reduction under motion blur / light occlusions
- stable OCR output is used as primary input for identity resolution

### Plate Tracking (ByteTrack)
- ByteTrack-based object tracking
- track-level temporal association
- integration with identity persistence layer

### Parking Event System
Module: `PlateRegistry`
- detect new vehicles entries
- avoid duplicate events
- maintain active tracks
- convert detections → structured events

Example:
```json
{
  "type": "vehicle_entered",
  "plate": "GD1234A",
  "camera": "entry"
}
```

### Session Management System (DB)
Parking lifecycle:
```
ENTRY → ACTIVE → PAID → EXIT → ENDED
```

Each session stored in DB contains:
- license plate
- entry/exit timestamps
- payment status + time
- billing amount
- session ID

Edge cases handled:
- duplicate entries (cooldown logic)
- OCR mismatches (fuzzy matching)
- expired payments (grace period)
- re-payment after expiration

#### Billing Engine

- time-based billing
- automatic fee calculation
- additional charges after grace period

#### Gate Controller (stateless)
Decision logic (interpreting events results of SessionManager):

- `OPEN_GATE` → valid payment
- `DENY` → unpaid / expired / invalid session 

### REST API (FastAPI)
Endpoints:
- `GET /sessions/active`
- `GET /sessions/{plate}`
- `POST /payment`
- `POST /exit`

### Event Logging System
Logging implementation:
- JSON structured logs
- ISO timestamps
- rotating log files (size-based)
- multiple backups
- persistent event tracking

### OCR Processing (Async - Redis + Worker System)

OCR system has been upgraded from synchronous processing to an **asynchronous queue-based architecture**.

Instead of running OCR directly inside the frame processing loop, OCR is now offloaded to a background worker.

#### Flow:
```
FrameProcessor → enqueue crop → Redis Queue → OCR Worker → Redis Stream → FrameProcessor → Stabilizer
```

#### Benefits:
- non-blocking video pipeline
- improved FPS stability
- scalable OCR processing
- separation of concerns
- worker-based compute scaling
OCR results are streamed back asynchronously and aggregated in the stabilizer for temporal consistency.

### Plate Identity Layer (Re-identification System)

The system introduces a **plate identity abstraction layer**, decoupling tracking IDs from actual vehicle identity. Instead of relying on unstable `track_id` (which can change due to tracking drift), the system assigns persistent `identity_id` based on stabilized OCR output.

#### Pipeline:
- ByteTrack → temporary `track_id`
- OCR Stabilizer → stable plate text
- PlateIdentityManager → persistent `identity_id`

#### Benefits:
- robust against tracking ID switches
- consistent vehicle identity across frames
- improved event reliability
- eliminates duplicate session creation caused by track fragmentation

---

## High-level system pipeline:
```
Video Stream
      ↓
FrameProcessor
      ↓
Detection + Tracking
      ↓
Async OCR (worker)
      ↓
Temporal Stabilization
      ↓
Event Generation
      ↓
SessionManager
      ↓
BillingEngine
      ↓
GateController
      ↓
API Response
      ↓
User / External System
```
---

### Current Limitations
- single-process system
- SQLite
- synchronous API
- no authentication layer

---

## Project Structure
```
vision_ticketless_parking_system/
│
├── db/
│   ├── database.py
│   ├── models.py
│ 
├── src/
│   ├── video_stream.py
│   ├── vehicle_detector.py
│   ├── plate_detector.py
│   ├── plate_ocr.py
│   ├── plate_registry.py
│   ├── plate_text_stabilizer.py
|
│   ├── utils/
│   │   ├── drawing.py
│   │   ├── plate_format.py
│   │   └── fps_counter.py
│
│   ├── pipeline/
│   |   ├── event_enricher.py
│   |   └── frame_processor.py
│ 
│   ├── queue/
│   |   ├── ocr_queue.py
│   |   └── redis_client.py
│
│   ├── workers/
│   |   └── ocr_worker.py
│ 
│ 
│   ├── logging/
│   |   └── event_logger.py
│
│   ├── parking_session/
│   |   ├── session_manager.py
│   |   ├── billing_engine.py
│   |   └── gate_controller.py
│ 
├── app.py
├── main.py
├── requirements.txt
├── train_plate_detector.py
├── parking.db
└── README.md
```
--- 

## Performance
Approximate CPU performance with lightweight models:
```
| Component         | Performance                    |
| ----------------- | ------------------------------ |
| Vehicle Detection | ~40–60 FPS                     |
| Plate Detection   | real-time                      |
| OCR               | optimized using frame skipping |
| Tracking          | negligible overhead            |
```

---

## Next Steps
- async event pipeline (Redis)
- microservice architecture
- PostgreSQL migration
- admin dashboard
- scalable worker-based OCR processing

---

## Future Goal
Build a production-ready intelligent parking system with:
- real-time computer vision pipeline
- scalable backend architecture
- event-driven processing
- robust OCR under real-world conditions

---
