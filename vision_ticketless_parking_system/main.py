import cv2

from src.video_stream import VideoStream

def main():
    stream = VideoStream(source=0)

    while True:
        ret, frame = stream.read()

        if not ret:
            break

        cv2.imshow("Vision parking Entry stream", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

