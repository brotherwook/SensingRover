import paho.mqtt.client as mqtt
import threading
import time
from datasend.sungjin.sensingRover import SensingRover ###################!!!!!!!!!!!!!!!!!!!!!!

# model02은 sensor publisher, camera publisher, command subscriber 3개로 분리한 것
# 사용하기전에 ###################!!!!!!!!!!!!!!!!!!!!!! 부분 수정후 사용

class CameraPublisher:
    def __init__(self, brokerIp=None, brokerPort=1883, cameraTopic=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__cameraTopic = cameraTopic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__stop = False
        self.sensingRover = SensingRover()

    def __on_connect(self, client, userdata, flags, result_code):
        print("** mqtt connected **")
        cameraThread = threading.Thread(target=self.__cameraPublish)
        cameraThread.start()

    def __on_disconnect(self, client, userdata, rc):
        print("** mqtt disconnected **")

    def __connect(self):
        self.__stop = False
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__client.loop_forever()

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
    cameraPublisher = CameraPublisher(brokerIp="192.168.3.250", brokerPort=1883, cameraTopic="/camerapub") ###################!!!!!!!!!!!!!!!!!!!!!!
    cameraPublisher.start()