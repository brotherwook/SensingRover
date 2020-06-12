from gpio.Camera import Camera
import cv2

class SensingRover:
    def __init__(self):
        self.camera = Camera("192.168.3.250", 1883, "/camerapub")

    def run(self):
        videoCapture = cv2.VideoCapture(0)  # device video0을 쓰기 때문
        # print(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH, 320))
        # print(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT, 240))
        videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        self.camera.connect()

        while True:
            if videoCapture.isOpened():
                retval, frame = videoCapture.read()
                if not retval:
                    print("video capture fail")
                    break
                self.camera.sendBase64(frame)
                print("send")
            else:
                break

        self.camera.disconnect()
        videoCapture.release()

if __name__ == "__main__":
    sensingRover = SensingRover()
    sensingRover.run()