# Smart Retail Shelf Analytics

A production-oriented computer vision system for real-time retail shelf monitoring using YOLO-based detection, multi-object tracking, temporal stabilization and spatial state modeling.

The system goes beyond simple object detection and models shelf availability as a temporally evolving spatial state, enabling robust and explainable stock monitoring under real-world retail conditions.

---

## Project motivation

Manual shelf inspection in retail environments is:
- time-consuming,
- error-prone,
- operationally expensive,
- difficult to scale across large stores.

An automated vision-based monitoring system can:
- detect low-stock situations early,
- provide structured operational data,
- reduce labor cost,
- support data-driven restocking decisions.

Instead of focusing purely on object detection accuracy, this project explores how modern computer vision models can be integrated into a robust, layered decision-making system where:
- temporal stability,
- spatial reasoning,
- observability,
- architectural clarity
are treated as first-class engineering goals.

---

## System overview

The system processes video input from a webcam or video file and performs
real-time product monitoring using detection, tracking and temporal
state analysis.

High-level pipeline:

Video stream → Frame capture → YOLO detection → Multi-object tracking →
Temporal stabilization → Spatial shelf modelling → Shelf state abstraction → Decision logic → Structured logging → Offline evaluation

Rather than treating object detection as the final output, the system
models shelf state as a temporally evolving process.

---

## Implemented features

### Phase 1 – Detection MVP
- real-time video capture from webcam or video file,
- object detection using a pretrained YOLOv8 model,
- visualization of detected objects with bounding boxes and confidence scores,
- FPS measurement to evaluate real-time performance.

Initial proof-of-concept focused on validating detection pipeline and real-time performance.

### Phase 2 – Shelf Analytics & Decision Logic
- product counting based on filtered detections,
- rolling window averaging to stabilize counts across frames,
- configurable minimum stock threshold,
- delayed alert triggering to reduce false positives caused by transient occlusions,

This introduced temporal reasoning and basic decision logic.

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

### Phase 2.6 – Object Tracking & Temporal Stabilization 
- multi-object tracking for persistent IDs
- missing-frame tolerance
- object reappearance handling
- reduction of count flickering
- robustness under short occlusions

Stability was achieved through layered temporal reasoning rather than reliance on raw detector outputs.

### Phase 2.7 – Spatial Shelf Modeling (Slot-Based State Engine)

To move beyond simple object counting, a spatial abstraction layer was introduced.
The shelf is modeled as:
- a fixed bounding box,
- divided into configurable rows and columns,
- representing physical product slots.
Each slot represents a physical product position. Detected and tracked objects are mapped into slots, producing a structured state representation:
- occupied_slots
- total_slots
- occupancy_ratio
- slot-level binary occupancy_map

This introduces a major architectural shift:
Detection
→ Tracking
→ Stabilization
→ Spatial Mapping
→ Shelf State Abstraction
→ Decision Logic

The system is now:
- identity-independent (robust to tracker ID switches),
- spatially grounded,
- aligned with real retail deployment logic.
Monitoring no longer depends on raw object count, but on structured shelf occupancy state.

### Phase 3 – Offline Evaluation & System Analysis

Offline evaluation pipeline using logged experiment data and statistical shelf behavior analysis with performance diagnostics including:
- occupancy distribution,
- FPS statistics,
- alert activation metrics,
- temporal stability indicators (count changes & jumps)
Evaluation reflects structured shelf state behavior rather than frame-level detection noise.

---

## Current Capabilities

The system supports:
- configurable shelf bounding box and grid layout (rows × columns)
- real-time slot occupancy visualization
- rolling average state smoothing
- delayed low-stock alert triggering
- structured experiment logging
- reproducible metadata tracking
- offline statistical evaluation

---
## Performance

On a standard laptop (CPU-only):
- 13-15 FPS average real-time performance
- low count variance under normal conditions
- controlled alert activation
- robustness under temporary occlusions

System stability improvements include:
- elimination of tracking-induced count spikes
- reduced frame-to-frame variance
- structured spatial state modeling
- improved alert consistency

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

- Decision stability over frame-level detection perfection.
- Clear separation between perception, spatial abstraction and business logic.
- Layered temporal reasoning (tracking + stabilization + spatial modeling).
- Shelf structure explicitly modeled.
- Identity-independent occupancy logic.
- Reproducible experiment-driven development.
- Observability as a core engineering requirement.
- Production-oriented CV pipeline mindset.

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