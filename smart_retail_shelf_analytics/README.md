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
real-time product monitoring using detection, tracking and temporal
state analysis.

High-level pipeline:

Video stream → Frame capture → YOLO detection → Multi-object tracking →
Temporal stabilization → Spatial shelf modelling → Decision logic →
Visualization & Structured logging → Offline evaluation

Rather than treating object detection as the final output, the system
models shelf state as a temporally evolving process. Multiple stabilization
layers reduce noise caused by detector variance, short occlusions and
frame-level inconsistencies.

The project is designed as a modular vision system where detection,
tracking, stabilization, analytics and observability are clearly separated,
allowing controlled experimentation and incremental architectural upgrades.

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

Tracker parameters were further refined together with an additional
temporal stabilization layer, improving robustness under occlusions,
temporary object removal and reappearance scenarios commonly observed
in retail environments.

### Phase 2.6 – Temporal Stabilization Layer

To address instability caused by short occlusions and detector jitter,
a dedicated stabilization layer was introduced between tracking and
shelf analytics.

Key features:
- missing-frame memory allowing recently lost tracks to persist temporarily,
- spatial reassociation of objects after short disappearances,
- prevention of count flickering caused by transient detection failures,
- recovery of objects after brief occlusions without affecting shelf state.

This layer significantly improves temporal consistency by ensuring that
short-term visual interruptions do not immediately affect product counts
or alert logic.

The stabilization mechanism operates independently from the tracker,
demonstrating a system-level approach where robustness emerges from
layered temporal reasoning rather than reliance on a single model.

### Phase 2.7 – Offline Evaluation & System Analysis

- offline evaluation pipeline operating on logged system events,
- statistical analysis of shelf behavior and system stability,
- performance diagnostics including: count distribution statistics, FPS performance analysis, alert activation and duration metrics, temporal stability indicators (count changes and jumps).

### Phase 3 – Spatial Shelf Modeling (Slot-Based State Engine)

To move beyond simple object counting, the system was extended with a spatial abstraction layer that models the shelf as a structured grid of slots.

Instead of treating detection count as the primary signal, the system now:
- defines a fixed shelf bounding box,
- divides it into configurable rows and columns,
- assigns detected objects to spatial slots,
- models shelf occupancy as a structured state representation.

Each slot represents a physical product position on the shelf.
The system determines whether a slot is occupied based on the presence of valid tracked objects within its boundaries.

The monitoring logic is now based on:
- number of occupied slots,
- occupancy ratio,
- slot-level binary occupancy map.

This transforms the system from a count-based detector into a spatial state engine capable of representing real retail shelf structure.

---

## Performance

The system operates in real time on a standard laptop without GPU
acceleration, achieving stable performance of approximately 10–15 FPS.

Recent architectural improvements significantly reduced temporal
instability:
- elimination of large count spikes caused by tracking fragmentation,
- stable product counts under short occlusions,
- reduced frame-to-frame count variance.

The project demonstrates that reliable retail analytics can be achieved
through system-level temporal design rather than raw detection accuracy alone.

---

## Project structure

```
smart_retail_shelf_analytics/
├── data/
│ └── groceries_video.mp4
│
├── logs/
│ └── archive/
│ └── shelf_events.csv
│
├── notebooks/
│
├── src/
│ └── detector.py
│ └── evaluation.py
│ └── shelf_logic.py
│ └── shelf_state.py
│ └── video_stream.py
│ └── logger.py
│ └── stabilizer.py
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
- Detection, tracking, spatial abstraction and business logic are intentionally decoupled to allow independent experimentation.
- Shelf structure is explicitly modeled using a slot-based spatial abstraction layer.
- Decision logic operates on abstracted shelf state rather than raw detections.
- The architecture separates perception, spatial reasoning and business semantics.
- Temporal smoothing and delayed decisions reflect real-world retail conditions where short visual disturbances are common.
- Robustness is achieved through layered temporal reasoning (tracking + stabilization + spatial modeling) rather than reliance on detector outputs alone.
- Logging and evaluation are treated as core system components enabling reproducibility and iterative improvement.
- Observability and experiment reproducibility are treated as core engineering requirements.

---

## Next Steps

Planned architectural extensions include:

- per-slot hysteresis to prevent slot flickering under short occlusions,
- zone-aware shelf modeling (front/back row differentiation),
- adaptive shelf bounding box calibration,
- automated shelf calibration via keypoint detection,
- advanced anomaly detection (unexpected product placement),
- multi-product class support,
- quantitative slot-level evaluation metrics,
- dashboard-based visualization layer.

---