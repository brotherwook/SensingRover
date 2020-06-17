from mqttPublisher import MqttPublisher
from mqttSubscriber import MqttSubscriber
from sensingRover import SensingRover


sensingRover = SensingRover()

mqttpublisher = MqttPublisher("192.168.3.242",1883,"/sensor",sensingRover)
mqttpublisher.connect()

mqttsubscriber = MqttSubscriber("192.168.3.242",1883,"/order",sensingRover)
mqttsubscriber.start()


while True:
    pass