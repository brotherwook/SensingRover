import paho.mqtt.client as mqtt
import threading


class MqttSubscriber:
    def __init__(self, SensingRover, brokerip=None, brokerport=1883, topic=None):
        self.__brokerip = brokerip
        self.__brokerport = brokerport
        self.__topic = topic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.sensingRover = SensingRover

    def __on_connect(self, client, userdata, flags, rc):
        print("** connection **")
        self.__client.subscribe(self.__topic, qos=0)

    def __on_disconnect(self, client, userdata, rc):
        print("** disconnection **")

    def __on_message(self, client, userdata, message):
        msg = str(message.payload, encoding="UTF-8")
        print("구독 내용: {}, 토픽: {}, Qos: {}".format(
            str(message.payload, encoding="UTF-8"),
            message.topic,
            message.qos
        ))
        self.sensingRover.write(msg, message.topic)


    def start(self):
        thread = threading.Thread(target=self.__subscribe)
        thread.start()

    def __subscribe(self):
        self.__client.connect(self.__brokerip, self.__brokerport)
        self.__client.loop_forever()

    def stop(self):
        self.__client.unsubscribe(self.__topic)
        self.__client.disconnect()


if __name__ == '__main__':
    mqttSubscriber = MqttSubscriber("192.168.3.179", topic="/sensor")
    mqttSubscriber.start()