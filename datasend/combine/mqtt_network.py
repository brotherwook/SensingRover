from datasend.combine.publisher import MqttPublisher
from datasend.combine.subscriber import MqttSubscriber
from datasend.combine.sensingRover import SensingRover
from datasend.combine.CameraPublisher import CameraPublisher
from gpio.Camera import Camera

cameraPublisher = CameraPublisher(brokerIp="192.168.3.179", brokerPort=1883, cameraTopic="/camerapub")
cameraPublisher.start()

while cameraPublisher.state == "off":
    pass

print("camera on")
camera = Camera(cameraPublisher)


sensingRover = SensingRover()
publisher = MqttPublisher(sensingRover, "192.168.3.179", topic="/sensor")
subscriber = MqttSubscriber(sensingRover, brokerip="192.168.3.179", brokerport=1883, topic="/command/#")

publisher.start()
subscriber.start()