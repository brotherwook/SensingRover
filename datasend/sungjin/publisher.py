import paho.mqtt.client as mqtt
import threading
import time
from datasend.sungjin.sensingRover import SensingRover

class MqttPublisher:
    def __init__(self, brokerIp=None, brokerPort=1883, topic=None, cameraTopic=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__topic = topic
        self.__cameraTopic = cameraTopic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__stop = False
        self.sensingRover = SensingRover()

    def __on_connect(self):
        print("** connection **")

    def __on_disconnect(self):
        print("** disconnection **")

    def __publish(self):
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__stop = False
        self.__client.loop_start()
        while not self.__stop:
            message = self.sensingRover.message()
            self.__client.publish(self.__topic, message, retain=False)
            print("발행 내용:", self.__topic, message)
            time.sleep(1)
        self.__client.loop_stop()

    def __cameraPublish(self):
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__stop = False
        self.__client.loop_start()
        while not self.__stop:
            message = self.sensingRover.cameraMessage()
            self.__client.publish(self.__cameraTopictopic, message, retain=False)
            print("발행 내용:", self.__cameraTopic, message)
        self.__client.loop_stop()

    def start(self):
        thread = threading.Thread(target=self.__publish)
        thread.start()
        cameraThread = threading.Thread(target=self.__cameraPublish)
        cameraThread.start()

    def stop(self):
        self.__client.disconnect()
        self.__stop = True


if __name__ == '__main__':
    mqttPublisher = MqttPublisher("192.168.3.250", topic="/sensor", cameraTopic="/camerapub")
    mqttPublisher.start()