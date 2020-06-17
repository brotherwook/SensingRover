import cv2
import paho.mqtt.client as mqtt
import threading
import base64

class ImageMqttPublisher:
    def __init__(self, brokerIp, brokerPort, pubTopic):
        self.brokerIp = brokerIp
        self.brokerPort = brokerPort
        self.pubTopic = pubTopic
        self.client = None

    def connent(self):
        thread = threading.Thread(target=self.__run, daemon=True)
        thread.start()

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.brokerIp, self.brokerPort)
        self.client.loop_forever()

    def __on_connect(self, client, userdate, flags, rc):
        print("ImageMqttClient mqtt broker connected")

    def __on_disconnect(self, client, userdate, rc):
        print("ImageMqttClient mqtt broker disconnected")

    def disconnect(self):
        if self.client != None:
            self.client.on_disconnect()

    def sendBase64(self, frame):
        if self.client is None:
            return
        if not self.client.is_connected() :
            return

        retval, bytes = cv2.imencode(".jpg", frame)

        if retval == False:
            print("image encoding fail")
            return
        print(bytes)
        b64_bytes = base64.b64encode(bytes)
        self.client.publish(self.pubTopic, b64_bytes)

if __name__  == "__main__":
    videoCapture = cv2.VideoCapture(0)
    videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    imageMqttPublisher = ImageMqttPublisher("192.168.3.242",1883,"/camerapub")
    imageMqttPublisher.connent()
    while True:
        if videoCapture.isOpened():
            retval, frame = videoCapture.read()
            if not retval:
                print("Video capture fail")
                break
            imageMqttPublisher.sendBase64(frame)
        else:
            break

    imageMqttPublisher.disconnect()
    videoCapture.release()