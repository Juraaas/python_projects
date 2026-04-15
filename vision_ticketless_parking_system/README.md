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
- stable plate output across frames

### Plate Tracking (ByteTrack)
- persistent tracking IDs
- reduced OCR calls
- improved temporal consistency
- object-based instead of frame-based processing

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

---

## High-level system pipeline:
```
Video Stream
      ↓
FrameProcessor
      ↓
Detection + OCR + Tracking
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
│   |   └── event_enricher.py
│   |   └── frame_processor.py

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
