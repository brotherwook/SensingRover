from datasend.brotherwook.publisher import MqttPublisher
from datasend.brotherwook.subscriber import MqttSubscriber
from datasend.brotherwook.sensingRover import SensingRover
from datasend.sungjin.camera.CameraPublisher import CameraPublisher
from gpio.Camera import Camera

# cameraPublisher = CameraPublisher(brokerIp="192.168.3.60", brokerPort=1883, cameraTopic="/camerapub")
# cameraPublisher.start()
# camera = Camera(cameraPublisher)

sensingRover = SensingRover()
publisher = MqttPublisher(sensingRover, "192.168.3.179", topic="/sensor")
subscriber = MqttSubscriber(sensingRover, brokerip="192.168.3.179", brokerport=1883, topic="/command/#")


publisher.start()
subscriber.start()