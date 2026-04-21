# Computer Vision Systems & Machine Learning Engineering

This repository is focused on **Computer Vision system design and machine learning engineering**, with an emphasis on building **end-to-end, production-oriented AI pipelines**.

The primary goal is not only model training, but the design of **complete systems that combine perception, tracking, temporal reasoning, and decision-making logic**.

Projects in this repository demonstrate:
- real-time Computer Vision pipelines
- object detection and multi-object tracking systems
- temporal consistency and stabilization mechanisms
- event-driven architectures
- applied machine learning for real-world scenarios
- reproducible experiments and evaluation workflows

The main focus is **Computer Vision engineering for real-world systems**, not isolated ML experiments.

---

## Featured Project


## Featured Project

- [Vision Ticketless Parking System](./vision_ticketless_parking_system)
  - End-to-end real-time ANPR (Automatic Number Plate Recognition) system
  - Multi-stage Computer Vision pipeline: detection → tracking → OCR → temporal stabilization
  - Asynchronous OCR processing using Redis + RQ worker architecture
  - Event-driven system for parking session lifecycle management
  - Robust plate recognition under motion blur and occlusions
  - Designed as a scalable architecture for real-world parking infrastructure

This project represents a **full CV system architecture**, combining:
- perception (YOLO-based detection)
- tracking (ByteTrack)
- temporal reasoning (OCR stabilization)
- asynchronous compute pipeline (Redis workers)
- event generation and state management
It is the most advanced system in this repository and reflects real-world CV engineering practices.  

### Other projects

- [Smart Retail Shelf Analytics](./smart_retail_shelf_analytics)
  - Real-time Computer Vision system built for retail shelf monitoring
  - YOLOv8-based object detection
  - Multi-object tracking with temporal stabilization
  - Occlusion-robust product counting and low-stock detection
  - Structured experiment logging and offline evaluation pipeline with stability metrics
  - Modular computer vision architecture focused on decision stability
The system focuses on decision stability, monitoring logic, and reproducible experiments, which are essential in CV deployments.

- [Titanic Survival Prediction](./titanic_ml)
  - Binary classification problem
  - End-to-end ML pipeline (EDA → preprocessing → training → evaluation)
  - Multiple models compared using common metrics

- [Customer Segmentation – Clustering Analysis](./customer_segmentation)
  - Unsupervised learning project for customer behavior analysis
  - Transaction-level data transformed into customer-level RFM features
  - Clustering used to identify meaningful customer segments for business insights

---

## Planned Extensions

- additional real-time Computer Vision systems
- scalable tracking and video analytics architectures
- production-grade CV pipeline optimization
- distributed inference and async processing systems
- deployment-oriented ML/CV engineering

---