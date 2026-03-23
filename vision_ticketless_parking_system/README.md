# Vision Ticketless Parking System

End-to-end computer vision pipeline for automated vehicle entry and exit monitoring in parking lots, without the need for physical tickets. 
The system detects vehicles, identifies license plates, performs OCR recognition, tracks plates across frames and generates structured parking events ready to integrate with automated parking management systems.
The goal of the project is to build a **modular, production-oriented ANPR system, similar to real-world applications used in modern parking infrastructure.

---

## Project Motivation

Manual parking management with tickets or attendants is:
- labor-intensive
- error-prone
- difficult to scale for busy locations
- hard to integrate with automated payment systems

A vision-based ticketless system can:
- detect vehicles automatically at entry/exit
- read and log license plates reliably
- timestamp and track parking duration
- integrate with payment verification
- provide structured data for analytics and operational optimization

The goal is not just detection, but building a complete system architecture.

---

## Implemented Features

### Phase 1 – Vehicle Detection
- Real-time video stream (camera / video)
- YOLOv8-based vehicle detection
- Multi-class vehicle support
- Confidence filtering
- FPS monitoring

### Phase 2 – License Plate Recognition Pipeline

#### Plate Detection
- Detection inside vehicle ROI
- Fine-tuned YOLO model for plates
- Global coordinate reconstruction

#### OCR Recognition
- EasyOCR integration
- Text normalization (A-Z, 0-9)
- Best-confidence selection

#### Temporal OCR Stabilization
OCR predictions vary due to:
- motion blur
- lighting conditions
- viewing angle
- occlusion

Solution: **PlateTextStabilizer**
- sliding window history
- character-level voting
- minimum vote threshold
- length consistency filtering

#### OCR Optimization
- OCR executed every N frames
- reduced compute cost
- improved real-time performance

### Phase 3 – Plate Tracking (ByteTrack)

System upgraded from frame-based to object-based processing:

- ByteTrack integration
- persistent `track_id` per plate
- robust tracking across frames
- reduced OCR redundancy
- improved stability of predictions

---

### Phase 4 – Parking Event System (Entry Logic)

Module: `PlateRegistry`
Responsibilities:
- detect new vehicles entering the scene
- prevent duplicate events
- maintain active tracks
- convert detections → structured events

Example event output:
```
[EVENT] vehicle_entered -> GD1234A
```

### Phase 5 – Parking Sessions & Billing Engine

Full backend logic implemented:

#### Session Manager (State Machine)

Parking lifecycle:
```
ENTRY_DETECTED → SESSION_ACTIVE → PAYMENT_PENDING → PAYMENT_CONFIRMED → EXIT_ALLOWED → SESSION_ENDED
```

Each session stores:
- plate number
- entry time
- payment status
- session ID
- amount due

#### Billing Engine

- billing per **30-minute intervals**
- automatic fee calculation
- support for additional charges after grace period

#### Payment Logic

- payment confirmation handling
- prevention of duplicate payments
- grace period after payment (10 min)
- re-billing if grace period exceeded

#### Gate Controller

Decision system:
- `OPEN_GATE` → valid payment + within grace period
- `DENY` → unpaid or expired payment

### Phase 6 – Event Logging System

Logging implementation:
- JSON structured logs
- ISO timestamps
- rotating log files (size-based)
- multiple backups
Example log:
```json
{
  "event": "vehicle_entered",
  "plate": "WPR74821",
  "timestamp": "2026-03-20T15:12:01",
  "camera": "entry_cam_1"
}
```
---

## High-level system pipeline:
```
VideoStream
     ↓
FrameProcessor
     ↓
Vehicle Detector (YOLOv8)
     ↓
Vehicle ROI Extraction
     ↓
Plate Detector (fine-tuned YOLOv8)
     ↓
Global Coordinate Reconstruction
     ↓
ByteTrack (Plate Tracking)
     ↓
Plate Crop Extraction
     ↓
OCR (EasyOCR)
     ↓
PlateTextStabilizer
     ↓
PlateRegistry (Entry Events)
     ↓
SessionManager
     ↓
BillingEngine
     ↓
GateController
     ↓
EventLogger
     ↓
System Output / Visualization
```
---

## Project Structure
```
vision_ticketless_parking_system/
├── data/
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

#### Phase 6 – Exit Camera Integration
- second video stream
- exit detection logic
- linking entry <-> exit
  
#### Phase 7 Api Layer and Production Readiness
- REST API
- Docker deployment
- GPU acceleration
- database integration
- experiments metadata
- monitoring & evaluation metrics

---

## Future Goal

Build a fully functional production-ready parking system:
- multi-camera vehicle tracking
- real-time payment validation
- large-scale parking analytics
- automated gate control

---
