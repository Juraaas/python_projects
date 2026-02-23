# Smart Retail Shelf Analytics

This project demonstrates a real-time computer vision system for monitoring
product availability on retail shelves using YOLO-based object detection.

The goal of the system is to support automated shelf monitoring by detecting
products, estimating stock levels and enabling data-driven restocking decisions.

---

## Project motivation

Manual shelf monitoring in retail environments is time-consuming, error-prone
and difficult to scale. An automated vision-based system can help detect
out-of-stock situations early and provide actionable insights for store operations.

This project explores how modern object detection models can be integrated into
a real-time system to support such use cases.

---

## System overview

The system processes video input from a webcam or video file and performs
real-time object detection using a pretrained YOLOv8 model.

High-level pipeline:

Video stream → Frame capture → YOLO detection → Visual output

At this stage, the project focuses on establishing a stable and efficient
detection pipeline, which will be extended with shelf analytics and business
logic in later phases.

---

## Phase 1 – Detection MVP

**Current scope:**
- real-time video capture from webcam or video file,
- object detection using YOLOv8,
- visualization of detected objects with bounding boxes and confidence scores,
- FPS measurement to evaluate real-time performance.

**Out of scope (planned for next phases):**
- product counting and stock estimation,
- alerting and business logic,
- evaluation metrics and reporting.

---

## Performance

The detection pipeline runs in real time on a laptop webcam with stable
performance (approximately 10–15 FPS), demonstrating feasibility under
limited hardware constraints.

---

## Project structure

smart_retail_shelf_analytics/
├── data/
├── notebooks/
│
├── src/
│ └── detector.py
│ └── video_stream.py
│
├── main.py
├── requirements.txt
└── README.md
```

---