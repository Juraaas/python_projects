# Smart Retail Shelf Analytics

This project demonstrates a real-time computer vision system for monitoring
product availability on retail shelves using YOLO-based object detection combined with temporal analytics and decision logic.

The goal of the system is to support automated shelf monitoring by detecting
products, estimating stock levels and enabling data-driven restocking decisions in retail environments.

---

## Project motivation

Manual shelf monitoring in retail environments is time-consuming, error-prone and difficult to scale. An automated vision-based system can detect out-of-stock situations early and provide actionable insights for store operations.

Rather than focusing purely on object detection accuracy, this project explores how modern computer vision models can be integrated into a robust temporal decision-making system, where stability, observability and system behavior are treated as first-class design goals.

---

## System overview

The system processes video input from a webcam or video file and performs
real-time object detection using a pretrained YOLOv8 model.

High-level pipeline:

Video stream → Frame capture → YOLO detection → Object tracking → Shelf analytics → Decision logic → Visualization & Logging → Offline evaluation

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
The system implements structured experiment logging designed to support
offline evaluation, debugging and reproducible experimentation.

Key features:
- structured logging of shelf state and system performance to CSV files,
- automatic creation of a new log file for every experiment run,
- hybrid logging strategy combining:
  - periodic logging (time-based snapshots),
  - event-based logging (alert state changes),
- recorded fields include timestamps, product counts, alert states and FPS.

Additionally, each experiment automatically generates a metadata file
(`*_metadata.json`) containing:

- experiment run identifier,
- system configuration (tracker, detector and monitoring parameters),
- logging settings,
- experiment creation timestamp.

This design enables full experiment reproducibility and allows quantitative
comparison between different system configurations without manual bookkeeping.
The logging approach significantly reduces data volume while preserving
all critical information required for performance analysis and system evaluation.

### Phase 2.5.1 – Object Tracking (Initial Integration)
- integration of a multi-object tracker to assign persistent IDs to detected products,
- improved temporal consistency of product counts across frames,
- reduced counting instability caused by frame-to-frame detection vatiance.

The tracker introduces identity persistence across frames, forming the foundation for higher-level analytics such as zone-based counting and long-term shelf state estimation.

Tracker parameters are currently being tuned to further improve ID stability
under occlusions and rapid motion.

### Phase 3 – Offline Evaluation & System Analysis

- offline evaluation pipeline operating on logged system events,
- statistical analysis of shelf behavior and system stability,
- performance diagnostics including: count distribution statistics, FPS performance analysis, alert activation and duration metrics, temporal stability indicators (count changes and jumps).

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
│ └── experiment_2026-03-01_10-57-41.csv
│ └── archive/
│ └── shelf_events.csv


│
├── notebooks/
│
├── src/
│ └── detector.py
│ └── evaluation.py
│ └── shelf_logic.py
│ └── video_stream.py
│ └── logger.py
│ └── tracker.py
│
├── evaluate.py
├── main.py
├── requirements.txt
└── README.md
└── yolov8n.pt

```

---

## Design considerations 

- The system prioritizes decision stability and temporal consistency over perfect frame-level detection accuracy.
- Detection, tracking and business logic are intentionally decoupled to allow independent experimentation.
- Temporal smoothing and delayed decisions reflect real-world retail conditions where short visual disturbances are common.
- Logging and evaluation are treated as core system components enabling reproducibility and iterative improvement.
- The architecture follows a production-oriented vision pipeline rather than a single-model approach.

---

## Next Steps

Planned extensions of the project include:
- further tuning of tracker parameters to improve ID persistence,
- hysteresis-based alert logic for improved decision stability,
- shelf memory mechanisms to handle temporary occlusions,
- quantitative metrics for counting accuracy and alert precision,
- zone-based shelf analysis (front vs back of shelf),
- advanced visualization and reporting.

---