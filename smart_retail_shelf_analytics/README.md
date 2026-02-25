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
a robust, real-time decision-making system, rather than focusing on raw detection accuracy.

---

## System overview

The system processes video input from a webcam or video file and performs
real-time object detection using a pretrained YOLOv8 model.

High-level pipeline:

Video stream → Frame capture → YOLO detection → Shelf analytics → Decision logic → Visualization & Logging

The project is designed as a modular system, where detection, business logic, logging
and visualization are clearly separated to allow further extensions and experiments.

---

## Implemented features

### Phase 1 – Detection MVP
- real-time video capture from webcam or video file,
- object detection using a pretrained YOLOv8 model,
- visualization of detected objects with bounding boxes and confidence scores,
- FPS measurement to evaluate real-time performance.

### Phase 2 – Shelf Analytics & Decision Logic
- product counting based on filtered detections,
- rolling window averaging to stabilize counts across frames,
- configurable minimum stock threshold,
- delayed alert triggering to reduce false positives caused by transient occlusions,
- real-time visualization of current count, average count and alert status.

The alert logic ensures that low-stock notifications are triggered only when
the condition persists over multiple consecutive frames, making the system
robust to short-term disturbances such as hand occlusions or camera noise.

### Phase 2.5 – Event Logging & Observability
- structured logging of shelf state and system performance to CSV files,
- hybrid logging strategy combining:
  - periodic logging (time-based snapshots),
  - event-based logging (alert state changes),
- recorded fields include timestamps, product counts, alert states and FPS.

This logging approach significantly reduces data volume while preserving
all critical information required for offline evaluation, debugging and
performance analysis.

### Phase 2.5.1 – Object Tracking (Initial Integration)
- integration of a multi-object tracker to assign persistent IDs to detected products,
- improved temporal consistency of product counts across frames,
- groundwork for future extensions such as zone-based counting and shelf-depth analysis.

Tracker parameters are currently being tuned to further improve ID stability
under occlusions and fast object motion.

---

## Performance

The detection pipeline runs in real time on a laptop webcam with stable
performance (approximately 10–15 FPS), demonstrating feasibility under
limited hardware constraints without GPU acceleration.

---

## Project structure

```
smart_retail_shelf_analytics/
├── data/
│ └── groceries_video.mp4
│
├── logs/
│ └── shelf_events.csv
│
├── notebooks/
│
├── src/
│ └── detector.py
│ └── shelf_logic.py
│ └── video_stream.py
│ └── logger.py
│ └── tracker.py
│
├── main.py
├── requirements.txt
└── README.md
└── yolov8n.pt

```

---

## Design considerations 
- The system prioritizes robust behavior and decision stability over perfect frame-level detection accuracy.
- Business logic is intentionally separated from the detection model to allow future extensions without retraining.
- Temporal smoothing and delayed decision-making are used to reflect real-world retail conditions.
- Logging is treated as a first-class component to enable reproducibility and offline analysis.

---

## Next Steps

Planned extensions of the project include:
- further tuning of tracker parameters to improve ID stability,
- offline evaluation on recorded video data using logged events,
- quantitative metrics for counting accuracy and alert precision,
- zone-based shelf analysis (front vs back of shelf),
- advanced visualization and reporting.

---