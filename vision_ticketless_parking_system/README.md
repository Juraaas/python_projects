# Vision Ticketless Parking System

End-to-end computer vision pipeline for automated vehicle entry and exit monitoring in parking lots, without the need for physical tickets. 
The system detects vehicles, identifies license plates, performs OCR recognition, tracks plates across frames and generates structured parking events ready to integrate with automated parking management systems.
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
#### Temporal OCR Stabilization
OCR predictions fluctuate across frames due to:
- motion blur
- lighting changes
- angle variation
- partial occlusion
To stabilize predictions the system implements **PlateTextStabilizer**:
- sliding window text history
- character-level temporal voting
- configurable minimum number of OCR votes
- stable plate prediction across frames
#### OCR Performance Optimization
To reduce redundant OCR calls, OCR is executed only every N frames by configurable parameter, which provides significant reduction in compute cost.

### Phase 3 – Plate Tracking

To transform the system from frame-based processing to object-based processing, tracking was added,with integration of ByteTrack.
Features:
- persistent track_id for each detected plate
- tracking across frames
- reduced redundant OCR calls
- improved temporal stabilization

### Phase 4 – Parking Event System (Entry Detection)

The system includes a PlateRegistry module that converts detections into structured parking events.
Responsibilities:
- track active plate detections
- detect new vehicle entry
- prevent duplicate event generation
- maintain active vehicle registry

Example event output:
```
[EVENT] vehicle_entered -> GD1234A
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
PlateRegistry
     ↓
Parking Events
     ↓
Visualization
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
│   ├── visualizer.py
│   └── utils/
│   │   └── drawing.py
│   │   └── plate_format.py
│   └── pipeline/
│       └── frame_processor.py
│ 
├── main.py
├── requirements.txt
└── README.md
```
---

## Next Steps

#### Phase 5 – Exit Camera & Parking Sessions

Planned functionality:
- exit camera stream
- vehicle exit detection
- parking session tracking
-parking duration calculation

#### Phase 6 – Production Readiness
- pipeline profiling
- GPU inference support
- Docker deployment
- REST API for parking system integration
- database logging

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

## Future Goal

Transform the project into a complete intelligent parking vision system capable of:
- fully automated ticketless parking
- integration with payment infrastructure
- multi-camera vehicle tracking
- large-scale parking analytics

---