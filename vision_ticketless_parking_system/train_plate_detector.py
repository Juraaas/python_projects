from ultralytics import YOLO

def train():
    model = YOLO("yolov8n.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=30,
        imgsz=512,
        batch=4,
        device=0,
        project="runs",
        name="plate_detector",
        half=True,
        workers=0,
    )

if __name__ == "__main__":
    train()