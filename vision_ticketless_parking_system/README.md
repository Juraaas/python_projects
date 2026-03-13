# Vision Ticketless Parking System

End-to-end computer vision pipeline for automated vehicle entry and exit monitoring in parking lots, without the need for physical tickets. 
The system detects vehicles, identifies license plates, performs OCR recognition, and prepares structured events for automated parking management systems.
The goal of the project is to build a modular, production-oriented vision pipeline, similar to real-world ANPR (Automatic Number Plate Recognition) systems used in modern parking infrastructure.

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

The goal is not just detection, but building a robust, reproducible, production-oriented pipeline.

---

## Implemented Features

### Phase 1 – Vehicle Detection

- Real-time video capture from webcam or video
- Vehicle detection for car, bus, truck, motorcycle using YOLOv8
- Confidence thresholding for stable detections
- Bounding box visualization with class and confidence
- FPS measurement to evaluate real-time performance

### Phase 2 – License Plate Recognition Pipeline

##### License Plate Detection
- Plate detection inside vehicle ROI
- Dedicated, fine-tuned YOLO plate detection model
- Global coordinate reconstruction
#### OCR Recognition
- EasyOCR based plate recognition
- Text normalization and filtering
- Best-confidence text selection
#### OCR Stabilization
OCR predictions fluctuate across frames. To ensure consistent results the system includes: **PlateTextStabilizer**
- sliding window text aggregation
- consensus-based plate output
- stable plate prediction across frames
#### OCR Performance Optimization
To reduce redundant OCR calls, OCR is executed only every N frames by configurable parameter, which provides significant reduction in compute cost.

---

## High-level system pipeline:
```
VideoStream
     ↓
Vehicle Detector (YOLO)
     ↓
Vehicle ROI Extraction
     ↓
Plate Detector (YOLO)
     ↓
Plate Crop
     ↓
OCR (EasyOCR)
     ↓
Plate Text Stabilizer
     ↓
Visualization / Event Output
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
│   ├── plate_text_stabilizer.py
│   ├── visualizer.py
│   └── utils/
│       └── drawing.py
├── main.py
├── requirements.txt
└── README.md
```
---

## Next Steps

#### Phase 3 – Vehicle & Plate Tracking
Add object tracking to improve system efficiency. Planned features:
- ByteTrack integration
- persistent track_id for vehicles
- OCR executed once per tracked plate
- elimination of duplicate OCR calls
This will transform the system from a frame-based pipeline to an object-based pipeline.

#### Phase 4 – Parking Event System
Parking system logic:
- entry detection
- exit detection
- parking duration calculation
- structured event logging

Example event:
```
vehicle_entered
plate: GD1234A
timestamp: 2026-03-13 12:01:34
```

#### Phase 5 – Production Readiness
- pipeline profiling
- GPU inference support
- Docker deployment
- REST API for parking system integration
- database logging

--- 

## Performance
Approximate CPU performance with lightweight models:
- Vehicle detection: ~40–60 FPS
- Plate detection + OCR pipeline: real-time capable
- OCR execution optimized using frame skipping