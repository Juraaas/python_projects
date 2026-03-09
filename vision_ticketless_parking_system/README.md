# Vision Ticketless Parking System

End-to-end computer vision pipeline for automated vehicle entry and exit monitoring in parking lots, without the need for physical tickets. The system detects vehicles, reads license plates, logs timestamps, and can integrate with payment verification for seamless parking management.

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

### Phase 1 – Vehicle Detection MVP

- Real-time video capture from webcam. 
- Vehicle detection for car, bus, truck, motorcycle using YOLOv8
- Confidence thresholding for stable detections
- Bounding box visualization with class and confidence
- FPS measurement to evaluate real-time performance

Note: Tracking and OCR will be added in the next phase.

---

## Project Structure

vision_ticketless_parking_system/
├── data/
│   └── test_car.mp4
│
├── src/
│   ├── video_stream.py
│   ├── vehicle_detector.py
│   ├── plate_ocr.py
│   ├── visualizer.py
│   └── utils/
│       └── drawing.py
├── main.py
├── requirements.txt
├── yolov8n.pt
└── README.md

---

## Next Steps

#### Phase 2 – License Plate Recognition
- License plate detection ROI
- PaddleOCR integration
- Structured plate logging per vehicle
- Entry/exit timestamp matching

#### Phase 3 – Tracking & System Intelligence
- Persistent IDs for vehicles
- Avoid duplicate logging for the same car
- Timestamp-based parking duration calculation
- Optional integration with payment system

#### Phase 4 – Performance & Deployment
- Optimize FPS and inference speed
- Pipeline profiling and diagnostics
- Docker containerization / deployment-ready system

--- 

## Performance
- Real-time vehicle detection (~40–60 FPS effective pipeline on CPU with small YOLO model)
- Modular architecture allows lightweight scaling and incremental improvements