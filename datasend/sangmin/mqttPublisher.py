import paho.mqtt.client as mqtt
import threading
import json
import time
import sensingRover

class MqttPublisher:
    def __init__(self, brokerIp, brokerPort, pubTopic, sensingRover):
        self.brokerIp = brokerIp
        self.brokerPort = brokerPort
        self.pubTopic = pubTopic
        self.sensingRover = sensingRover
        self.client = None
        self.stop = False

    def connect(self):
        thread = threading.Thread(target=self.__run, daemon=True)
        thread.start()


    # client connect and publish
    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.brokerIp,self.brokerPort)
        self.stop = False
        self.client.loop_start()

        while not self.stop:
            message = self.sensingRover.sensorMessage()

            if message == {}:
                message["error"] = "All sensors are turned off"
                print(message)
            else:
                message = json.dumps(message)
                self.client.publish(self.pubTopic, message, retain=False)
                #print(message)
            time.sleep(0.5)
        self.client.loop_forever()


    def __on_connect(self,client, userdata, flags, rc):
        print("MqttClient mqtt broker connected")

    def __on_disconnect(self,client, userdata, rc):
        print("MqttClient mqtt broker disconnected")

    def disconnect(self):
        self.client.disconnect()
        self.stop = True

if __name__ == "__main__":
    sensingRover = sensingRover.SensingRover()
    mqttpublisher = MqttPublisher("192.168.3.242",1883,"/sensor",sensingRover)
    mqttpublisher.connect()


    while True:
        pass
