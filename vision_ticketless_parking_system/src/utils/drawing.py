import cv2

def draw_detections(frame, objects):
    for obj in objects:
        x1, y1, x2, y2 = obj["bbox"]
        label = obj.get("label", "object")
        conf = obj.get("confidence")
        track_id = obj.get("track_id")
        text = label

        if track_id is not None:
            text += f" | ID {track_id}"

        if conf is not None:
            text += f" {conf:.2f}"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

def draw_plates_with_text(frame, plates):
    for plate in plates:
        if "text" not in plate or plate["text"] == "":
            continue

        x1, y1, x2, y2 = plate["bbox"]
        label = f"{plate['text']} {plate.get('ocr_conf', 0.0):.2f}"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )