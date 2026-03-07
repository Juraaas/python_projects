# Smart Retail Shelf Analytics

A research-driven, production-oriented computer vision pipeline for real-time retail shelf monitoring using YOLO-based detection, multi-object tracking, temporal stabilization and spatial state modeling.

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

Video stream → Frame capture → Detection Scheduler → YOLO detection → Multi-object tracking (ByteTrack) → Temporal stabilization → Spatial shelf modelling → Shelf state abstraction → Decision logic → Structured logging → Pipeline profiling → Offline evaluation

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

#### Update 

Additional logged metrics now include:
- raw_detection_count
- occupied_slots
- occupancy_ratio
- avg_count (rolling average)
- low_stock_counter
- event_type (periodic or alert_change)
- fps

This hybrid event-driven logging significantly improves observability while minimizing log redundancy.

The system explicitly logs alert state transitions, enabling:
- alert latency analysis
- false positive detection
- temporal stability benchmarking
- cross-experiment configuration comparison

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

Each detected and tracked object is mapped into a spatial slot based on its center position.

#### Per-slot temporal hysteresis

To prevent slot flickering under short occlusions or detector instability, each slot implements temporal hysteresis:
- **presence_threshold** – number of consecutive frames required to activate a slot
- **absence_threshold** – number of consecutive frames required to deactivate a slot
This ensures that slot state transitions are stable and temporally grounded.

The system now produces a structured state representation:
- occupied_slots
- total_slots
- occupancy_ratio
- occupancy_map (binary slot vector)

This introduces a major architectural shift:

Detection
→ Tracking
→ Stabilization
→ Spatial Mapping
→ Slot-Level Hysteresis
→ Shelf State Abstraction
→ Decision Logic

Monitoring no longer depends on raw object count but on stable, spatially structured occupancy state.

### Phase 2.8 – Pipeline Profiling & Performance Diagnostics

To improve system observability and support performance-oriented
development, the pipeline now includes fine-grained runtime profiling.

Each major processing stage is measured independently:

- detection_time
- tracking_time
- stabilization_time
- spatial_time
- decision_time
- pipeline_time (end-to-end processing time)

These metrics are automatically logged alongside shelf state data.

This profiling layer enables:

- bottleneck identification
- performance regression detection
- cross-experiment performance comparison
- real-time system diagnostics

Initial experiments show that object detection accounts for the majority
of pipeline latency, while tracking and higher-level reasoning layers
introduce minimal computational overhead.

This insight guides further system optimization strategies such as
detection stride scheduling and lightweight model selection.

### Phase 2.9 – Detection Scheduling

To improve real-time performance while preserving tracking stability, the
system implements detection stride scheduling.

Instead of running the object detector on every frame, detection is
performed periodically while the tracker maintains object state between
detections.

Pipeline behavior:
Frame N → DETECT (YOLO + tracker update)
Frame N + 1 → TRACK (tracker prediction)
Frame N + 2 → TRACK
Frame N + 3 → DETECT

This strategy privdes several advantages:
- significantly reduces average detection workload
- improves overall system FPS
- maintains stable object identities between detection updates
- enables lightweight real-time operation on CPU-only systems

### Phase 3 – Offline Evaluation & System Analysis

Offline evaluation pipeline using logged experiment data and statistical shelf behavior analysis with performance diagnostics including:
- occupancy distribution,
- FPS statistics,
- alert activation metrics,
- temporal stability indicators (count changes & jumps)
Evaluation reflects structured shelf state behavior rather than frame-level detection noise.

#### Real-Time Pipeline Telemetry

In addtion to logging performance metrics, the system provides a real-time-on-screen profiling overlay that visualizes pipeline performance for each frame.

---

## Current Capabilities

The system supports:
- configurable shelf bounding box and grid layout (rows × columns)
- real-time slot occupancy visualization
- per-slot temporal hysteresis
- event-driven alert logging
- identity-independent spatial occupancy logic
- rolling average state smoothing
- delayed low-stock alert triggering
- reproducible metadata tracking
- offline statistical evaluation
- detection stride scheduling for real-time optimization
- real-time pipeline telemetry overlay and frame-level execution diagnostics

---

## Performance

On a standard laptop (CPU-only):

- 13–15 FPS raw detection throughput, 40-60 FPS effective pipeline throughput with detection stride scheduling
- ~55 ms average detection latency
- ~1 ms tracking overhead
- negligible cost of stabilization and spatial reasoning layers

Pipeline profiling reveals that object detection is the dominant
computational bottleneck, accounting for the vast majority of
processing time.

This confirms an important architectural insight:
higher-level reasoning layers (tracking, temporal stabilization and
spatial modeling) introduce minimal computational overhead while
significantly improving system stability and decision quality.

As a result, the system can incorporate sophisticated state modeling
without sacrificing real-time performance.

---

## Project structure

```
smart_retail_shelf_analytics/
├── configs/
│ └── default.yaml
│
├── data/
│ └── groceries_video.mp4
│
├── logs/
│ └── archive/
│ └── shelf_events.csv
│ └── experiment_YYYY-MM-DD_HH-MM-SS.csv
│ └── experiment_YYYY-MM-DD_HH-MM-SS_metadata.json
│
├── notebooks/
│
├── src/
│ └── config_loader.py
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

### Short-Term (System Hardening & Evaluation)

- quantitative alert latency analysis
- slot-level stability metrics
- automated experiment comparison tool
- hyperparameter sensitivity analysis (presence/absence thresholds)
Goal: turn system into evaluation-driven engineering project.

### Mid-Term (Advanced Shelf Intelligence)

- multi-product class support
- zone-aware shelf modeling
- anomaly detection (misplaced products)
- restocking event detection
Goal: expand from occupancy monitoring to structured retail intelligence.

### Long-Term (Deployment-Oriented Enhancements)

- automated shelf calibration
- adaptive bounding box detection
- lightweight deployment optimization
- dashboard-based visualization layer
Goal: production-ready system architecture.

---