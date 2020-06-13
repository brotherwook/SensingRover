import cv2
import threading
import base64

class Camera(threading.Thread):
    def __init__(self):
        self.videoCapture = cv2.VideoCapture(0)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.message = None
        super().__init__(daemon=True)
        super().start()

    def run(self):
        try:
            while True:
                if self.videoCapture.isOpened():
                    retval, frame = self.videoCapture.read()
                    if not retval:
                        print("video capture fail")
                        continue
                    self.encode(frame)
                else:
                    print("video not open")
        finally:
            self.videoCapture.release()
            print("videoCapture released")

    def encode(self, frame):
        retval, bytes = cv2.imencode(".jpg", frame)
        if not retval:
            print("image encoding fail")
            return
        b64_bytes = base64.b64encode(bytes)
        self.message = b64_bytes