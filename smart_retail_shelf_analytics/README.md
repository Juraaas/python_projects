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

The project is designed as a modular system, where detection, business logic
and visualization are clearly separated.

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
├── notebooks/
│
├── src/
│ └── detector.py
│ └── shelf_logic.py
│ └── video_stream.py
│
├── main.py
├── requirements.txt
└── README.md
└── yolov8n.pt

```

---

## Design considerations 
- The system prioritizes robustness and interpretability over perfect detection accuracy.
- Business logic is intentionally separated from the detection model to allow future extensions without retraining.
- The project focuses on system behavior and decision-making rather than dataset-specific model optimization.

---

## Next Steps

Planned extensions of the project include:
- logging of shelf states and alerts for offline analysis,
- offline evaluation on recorded video data,
- integration of object tracking to further stabilize counts,
- advanced visualization and reporting,
- experimentation with different alerting strategies.

---