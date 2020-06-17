import paho.mqtt.client as mqtt
import threading
import json
import time
import sensingRover

class MqttSubscriber:
    def __init__(self, brokerIp, brokerPort, pubTopic):
        self.brokerIp = brokerIp
        self.brokerPort = brokerPort
        self.pubTopic = pubTopic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def start(self):
        thread = threading.Thread(target=self.subscribe, daemon=True)
        thread.start()

    def subscribe(self):
        self.client.connect(self.brokerIp, self.brokerPort)
        self.client.loop_forever()

    def on_message(self, client, userdata, message):
        print("명령:{}, 토픽:{}, Qos={}".format(str(message.payload, encoding="UTF-8"), message.topic, message.qos))

    def on_connect(self,client, userdata, flags, rc):
        print("mqtt broker connected")
        self.client.subscribe(self.pubTopic, qos=0)

    def on_disconnect(self,client, userdata, rc):
        print("mqtt broker disconnected")

    def disconnect(self):
        self.client.unsubscribe(self.pubTopic)
        self.client.disconnect()


if __name__ == "__main__":
    mqttsubscriber = MqttSubscriber("192.168.3.242",1883,"/order")
    mqttsubscriber.start()


    while True:
        pass
