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

    def connect(self):
        thread = threading.Thread(target=self.__run, daemon=True)
        thread.start()

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.brokerIp, self.brokerPort)
        self.client.loop_forever() # 연결 시켜주고 끊키면 재연결 시켜줌

    def __on_connect(self, client, userdata, flags, rc):
        print("ImageMqttClient mqtt broker connected")

    def __on_disconnect(self, client, userdata, rc):
        print("ImageMqttClient mqtt broker disconnected")

    def disconnect(self):
        self.client.disconnect() # 명시적으로 연결을 끊어서 loop_forever가 재연결 하지 않음

    def sendBase64(self, frame): # 한컷의 이미지가 들어온다 frame
        if self.client is None:
            return
        # MQTT Broker가 연결되어 있지 않을 경우
        if not self.client.is_connected():
            return
        # JPEG 포맷으로 인코딩
        retval, bytes = cv2.imencode(".jpg", frame) # 보통 스트리밍 서비스는 JPEG을 많이 씀. PNG는 사이즈가 너무 큼
        # 인코딩이 실패났을 경우
        if not retval:
            print("image encoding fail")
            return
        # Base64 문자열로 인코딩
        b64_bytes = base64.b64encode(bytes) # 바로 보내도 되지만 base64로 다시 인코딩하는 이유는 html tag에서 바로 쓸 수 있기 때문이다.
        # MQTT Broker에 보내기
        self.client.publish(self.pubTopic, b64_bytes)

if __name__ == "__main__":
    videoCapture = cv2.VideoCapture(0) # device video0을 쓰기 때문
    # print(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH, 320))
    # print(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT, 240))
    videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    imageMqttPublisher = ImageMqttPublisher("192.168.3.250", 1883, "/camerapub")
    imageMqttPublisher.connect()

    while True:
        if videoCapture.isOpened():
            retval, frame = videoCapture.read()
            if not retval:
                print("video capture fail")
                break
            imageMqttPublisher.sendBase64(frame)
            print("send")
        else:
            break

    imageMqttPublisher.disconnect()
    videoCapture.release()