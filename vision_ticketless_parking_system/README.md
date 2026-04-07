# Vision Ticketless Parking System

End-to-end computer vision system for automated vehicle entry and exit management in parking lots, without the need for physical tickets. 
The system combines **real-time computer vision**, **event-driven architecture**, and **database-backend session management**
The goal of the project is to build a modular, production-oriented ANPR system, similar to real-world applications used in modern parking infrastructure.

---

## Project Motivation

Manual parking management with tickets or attendants is:
- labor-intensive
- error-prone
- difficult to scale for busy locations
- hard to integrate with automated payment systems

This project aims to build a **modern, automated parking system** that:
- detects vehicles in real time
- recognizes license plates
- manages sessions in a persistent database
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
- OCR recognition
- tracking and stabilization
- generating structured events

### 2. Backend Logic (State + API)
Responsible for:
- session lifecycle management
- billing and payments
- database
- gate decisions
- API communication

---

## Implemented Features

### Vehicle Detection
- YOLOv8-based detection
- multi-class support
- confidence filtering
- real-time performance monitoring (FPS)

### License Plate Recognition Pipeline

#### Plate Detection
- detection inside vehicle ROI
- fine-tuned YOLO model for plates
- global coordinate reconstruction

#### OCR Recognition (EasyOCR)
- alphanumeric normalization
- confidence-based selection

#### Temporal OCR Stabilization
Custom module: `PlateTextStabilizer`

- sliding window aggregation
- character-level voting
- noise reduction
- stable plate output across frames

#### OCR Optimization
- OCR executed every N frames
- reduced compute cost
- improved real-time performance

### Plate Tracking (ByteTrack)

- persistent tracking IDs
- reduced OCR calls
- improved temporal consistency
- object-based instead of frame-based processing

### Plate Matching (OCR Error Handling)
To handle OCR inconsistencies:

- similarity matching using `SequenceMatcher`
- fuzzy matching between entry and exit plates

Significantly improves robustness in real-world scenarios under different light conditions/motion blur.

### Parking Event System
Module: `PlateRegistry`

- detect new vehicles entries
- avoid duplicate events
- maintain active tracks
- convert detections → structured events

Example event output:
```
[EVENT] vehicle_entered -> GD1234A
```
Events are sent to the backend via `POST /event`

### Session Management System (DB)
Parking lifecycle:
```
ENTRY → ACTIVE → PAID → EXIT → ENDED
```

Each session stored in DB contains:
- plate
- entry time
- exit time
- payment status
- payment time
- session ID
- amount due
- session status (ACTIVE / ENDED)

Edge cases handled:
- duplicate entries (cooldown logic)
- OCR mismatches (fuzzy matching)
- expired payments (grace period)
- re-payment after expiration

#### Billing Engine

- time-based billing (30-minute intervals)
- automatic fee calculation
- additional charges after grace period

#### Payment Logic

- API-triggered payments (for now)
- duplicate payment protection
- configurable grace period after payment
- payment timestamp tracking

#### Gate Controller (stateless)
Decision logic (interpreting events results of SessionManager):

- `OPEN_GATE` → valid payment
- `DENY` → unpaid / expired / invalid session 

### REST API (FastAPI)
The system exposes a REST API:

#### Endpoints:
- `GET /sessions/active` → list active vehicles
- `GET /sessions/{plate}` → session details & fee
- `POST /payment` → confirm payment
- `POST /exit` → attempt exit

Example:
```json
{
  "plate": "GD1234A"
}
```

### Phase 6 – Event Logging System
Logging implementation:

- JSON structured logs
- ISO timestamps
- rotating log files (size-based)
- multiple backups
- persistent event tracking

Example log:
```json
{
  "event": "vehicle_entered",
  "plate": "GD1234A",
  "timestamp": "2026-03-25T15:12:01",
  "camera": "entry_cam_1"
}
```

#### Database Layer
Structure based on SQLite, context-managed sessions (get_db())

Benefits:
- clean session handling
- no memory leaks

---

## High-level system pipeline:
```
Camera / Video
      ↓
FrameProcessor
      ↓
Detection + OCR + Tracking
      ↓
Event Generation
      ↓
SessionManager (in-memory)
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
- no auth

---

## Project Structure
```
vision_ticketless_parking_system/
├── data/
│   ├── **video_files_for_testing_purposes.mp4**
│
├── src/
│   ├── video_stream.py
│   ├── vehicle_detector.py
│   ├── plate_detector.py
│   ├── plate_ocr.py
│   ├── plate_registry.py
│   ├── plate_text_stabilizer.py
│   ├── system_state.py
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

- PostgreSQL integration
- async processing
- service separation
- message queue (Kafka)
- admin dashboard

---

## Future Goal

Build a fully functional production-ready parking system:
- fully automated entry/exit
- scalable backend
- robust OCR handling
- real-time monitoring
- seamless payment integration

---
