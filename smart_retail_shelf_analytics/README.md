# Smart Retail Shelf Analytics

A **research-driven computer vision pipeline** for real-time retail shelf monitoring — built around YOLO-based detection, multi-object tracking, and spatial state modeling. The system treats shelf availability not as a frame-level detection problem, but as a **temporally evolving spatial state**, enabling robust and explainable stock monitoring under real-world retail conditions.

---

## The Problem

Manual shelf inspection is time-consuming, error-prone, and hard to scale. But simply plugging in an object detector isn't enough — raw detections flicker, objects get occluded, and per-frame counts don't reflect reality.

This project explores how temporal stability, spatial reasoning, and architectural clarity can be treated as first-class engineering goals — not afterthoughts — in a production-oriented CV pipeline.

---

## How It Works

```
Video Stream → Frame Capture → Detection Scheduler → YOLO Detection → ByteTrack
     → Temporal Stabilization → Spatial Shelf Modeling → Decision Logic → Structured Logging
```

Rather than using detection as the final output, the system models shelf state as a process that evolves over time. Each layer adds stability and structure before a decision is made.

---

## Key Design Decisions

**Slot-based spatial modeling** — the shelf is modeled as a fixed bounding box divided into a configurable grid of rows and columns. Each tracked object is mapped to a physical slot based on its center position. Monitoring is based on structured occupancy state, not raw object count.

**Per-slot temporal hysteresis** — each slot has independent presence and absence thresholds (consecutive frames required to activate or deactivate). This eliminates flickering caused by brief occlusions or detector instability, without smoothing away real state changes.

**Identity-independent occupancy logic** — slot state is determined by spatial position, not tracker ID. This makes the system robust against tracking fragmentation and ID switches mid-session.

**Detection stride scheduling** — YOLO runs periodically while ByteTrack maintains object state between detections. This brings effective throughput from ~13 FPS (raw detection) to 40–60 FPS on CPU-only hardware, with no loss in tracking stability.

**Observability as a core requirement** — every experiment logs structured shelf state, per-stage profiling timings, and metadata. A hybrid event-driven logging strategy (periodic snapshots + alert state transitions) minimizes data volume while preserving everything needed for evaluation and reproducibility.

---

## Pipeline Architecture

```
Detection
  → Tracking (ByteTrack)
    → Temporal Stabilization
      → Spatial Slot Mapping
        → Per-Slot Hysteresis
          → Shelf State Abstraction
            → Decision Logic
```

Initial profiling confirms that object detection accounts for the vast majority of pipeline latency (~55 ms), while tracking, stabilization, and spatial modeling introduce under 1 ms combined. This validates the architectural choice to invest in higher-level reasoning layers without sacrificing real-time performance.

---

## Evaluation Framework

The project includes a systematic offline evaluation pipeline — not just a prototype:

**Experiment logging** — every run generates a timestamped CSV and a `_metadata.json` file containing system configuration, tracker/detector parameters, and logging settings. Fully reproducible across runs.

**Slot stability metrics** — `slot_flip_rate`, `avg_slot_flip_rate`, and `slot_transition_count` quantify how often each slot oscillates between occupied and empty. Low flip rates indicate that temporal hysteresis parameters are well-calibrated.

**Automated experiment comparison** — `compare_experiments.py` loads all logged runs and outputs a cross-experiment summary across FPS, count statistics, alert frequency, stability indicators, and slot flip rates:

```
=========== EXPERIMENT COMPARISON ============

Experiment: experiment_2026-03-07_14-40-59
Avg FPS: 42.10 | Avg Count: 8.23 | Alert Activations: 3
Alert Ratio: 0.021 | Avg Slot Flip Rate: 0.00018
```

This turns configuration tuning (stride settings, hysteresis thresholds, tracker parameters) into a measurable, data-driven process.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Object detection | YOLOv8 |
| Object tracking | ByteTrack |
| Spatial modeling | Custom slot-based state engine |
| Temporal stabilization | Custom hysteresis logic |
| Logging & evaluation | CSV + JSON, pandas |
| Configuration | YAML |

---

## Performance (CPU-only, standard laptop)

| Component | Performance |
|---|---|
| Raw detection throughput | 13–15 FPS |
| Effective pipeline FPS (with stride scheduling) | 40–60 FPS |
| Avg detection latency | ~55 ms |
| Tracking overhead | ~1 ms |
| Stabilization + spatial reasoning | Negligible |

---

## Project Structure

```
smart_retail_shelf_analytics/
│
├── configs/
│   └── default.yaml
│
├── data/
│   └── groceries_video.mp4
│
├── logs/
│   ├── archive/
│   ├── experiment_YYYY-MM-DD_HH-MM-SS.csv
│   └── experiment_YYYY-MM-DD_HH-MM-SS_metadata.json
│
├── src/
│   ├── config_loader.py
│   ├── detector.py
│   ├── evaluation.py
│   ├── shelf_logic.py
│   ├── shelf_state.py
│   ├── video_stream.py
│   ├── logger.py
│   ├── stabilizer.py
│   └── tracker.py
│
├── evaluate.py
├── compare_experiments.py
├── main.py
└── requirements.txt
```

---

## Roadmap

**Short-term** — hyperparameter sensitivity analysis (hysteresis thresholds), alert latency benchmarking, expanded slot stability metrics.

**Mid-term** — multi-product class support, zone-aware shelf modeling, misplaced product detection, restocking event recognition.

**Long-term** — automated shelf calibration, adaptive bounding box detection, lightweight deployment optimization, dashboard-based visualization layer.
