import paho.mqtt.client as mqtt
import threading
import time
from datasend.sungjin.sensingRover import SensingRover ###################!!!!!!!!!!!!!!!!!!!!!!

# 사용하기전에 ###################!!!!!!!!!!!!!!!!!!!!!! 부분 수정후 사용

class MqttPublisher:
    def __init__(self, brokerIp=None, brokerPort=1883, sensorTopic=None, cameraTopic=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__sensorTopic = sensorTopic
        self.__cameraTopic = cameraTopic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__stop = False
        self.sensingRover = SensingRover()

    def __on_connect(self, client, userdata, flags, result_code):
        print("** mqtt connected **")
        sensorThread = threading.Thread(target=self.__sensorPublish)
        sensorThread.start()
        cameraThread = threading.Thread(target=self.__cameraPublish)
        cameraThread.start()

    def __on_disconnect(self, client, userdata, rc):
        print("** mqtt disconnected **")

    def __connect(self):
        self.__stop = False
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__client.loop_forever()

    def __sensorPublish(self):
        self.__stop = False
        while not self.__stop:
            message = self.sensingRover.sensorMessage()
            self.__client.publish(self.__sensorTopic, message, retain=False)
            # print("발행 내용:", self.__sensorTopic, message)
            time.sleep(1)

    def __cameraPublish(self):
        self.__stop = False
        while not self.__stop:
            message = self.sensingRover.cameraMessage()
            self.__client.publish(self.__cameraTopic, message, retain=False)
            # print("발행 내용:", self.__cameraTopic, message)

    def start(self):
        loopThread = threading.Thread(target=self.__connect)
        loopThread.start()

    def stop(self):
        self.__stop = True
        self.__client.disconnect()

if __name__ == "__main__":
    mqttPublisher = MqttPublisher(brokerIp="192.168.3.250", brokerPort=1883, sensorTopic="/sensor", cameraTopic="/camerapub") ###################!!!!!!!!!!!!!!!!!!!!!!
    mqttPublisher.start()