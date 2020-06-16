import paho.mqtt.client as mqtt
import threading
import time
from datasend.sungjin.sensingRover import SensingRover ###################!!!!!!!!!!!!!!!!!!!!!!
import json

# model02은 sensor publisher, camera publisher, command subscriber 3개로 분리한 것
# 사용하기전에 ###################!!!!!!!!!!!!!!!!!!!!!! 부분 수정후 사용

class CommandSubscriber:
    def __init__(self, brokerIp=None, brokerPort=1883, commandTopic=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__commandTopic = commandTopic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__stop = False
        self.sensingRover = SensingRover()

    def __on_connect(self, client, userdata, flags, result_code):
        print("** mqtt connected **")
        self.__subscribe(self.__client)

    def __on_disconnect(self, client, userdata, rc):
        print("** mqtt disconnected **")

    def __on_message(self, client, userdata, message):
        strMessage = str(message.payload, encoding="UTF-8")
        strMessage = json.loads(strMessage)
        print("수신 내용:", strMessage)
        self.sensingRover.write(strMessage)
        pass # SensingRover의 write() 호출
        # print("구독 내용: {}, 토픽: {}, Qos: {}".format(
        #     str(message.payload, encoding="UTF-8"),
        #     message.topic,
        #     message.qos
        # ))

    def __connect(self):
        self.__stop = False
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__client.loop_forever()

    def __subscribe(self, client):
        topic = self.__commandTopic
        self.__client.subscribe(topic)

    def start(self):
        loopThread = threading.Thread(target=self.__connect)
        loopThread.start()

    def stop(self):
        self.__stop = True
        self.__client.disconnect()

if __name__ == "__main__":
    commandSubscriber = CommandSubscriber(brokerIp="192.168.3.250", brokerPort=1883, commandTopic="/command") ###################!!!!!!!!!!!!!!!!!!!!!!
    commandSubscriber.start()