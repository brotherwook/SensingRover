import paho.mqtt.client as mqtt
import threading
from gpio.Camera import Camera

class CameraPublisher:
    def __init__(self, brokerIp=None, brokerPort=None, cameraTopic=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__cameraTopic = cameraTopic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.state = "off"

    def __on_connect(self, client, userdata, flags, result_code):
        self.state = "on"
        print("** camera mqtt connected **")

    def __on_disconnect(self, client, userdata, rc):
        self.state = "off"
        print("** camera mqtt disconnected **")

    def __connect(self):
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__client.loop_forever()

    def publish(self, message):
        self.__client.publish(self.__cameraTopic, message, retain=False)

    def start(self):
        loopThread = threading.Thread(target=self.__connect)
        loopThread.start()

    def stop(self):
        self.__stop = True
        self.__client.disconnect()

if __name__ == "__main__":
    cameraPublisher = CameraPublisher(brokerIp="192.168.3.250", brokerPort=1883, cameraTopic="/camerapub")
    cameraPublisher.start()

    while cameraPublisher.state == "off":
        pass

    print("camera on")
    camera = Camera(cameraPublisher)