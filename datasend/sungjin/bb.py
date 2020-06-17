import time
import datasend.sungjin.camera.SensorPublisher as publisher
import datasend.sungjin.camera.CommandSubscriber as subscriber
from datasend.sungjin.camera.CameraPublisher import CameraPublisher
from gpio.Camera import Camera
from datasend.sungjin.sensingRover import SensingRover
sensingRover = SensingRover()
publisher = publisher.SensorPublisher(brokerIp="192.168.3.131", brokerPort=1883, sensorTopic='/sensor',sensingRover=sensingRover)
subscriber = subscriber.CommandSubscriber(brokerIp="192.168.3.131", brokerPort=1883, commandTopic="/command",sensingRover=sensingRover)

publisher.start()
subscriber.start()

# cameraPublisher = CameraPublisher(brokerIp="192.168.3.131", brokerPort=1883, cameraTopic="/camerapub")
# cameraPublisher.start()
#
# while cameraPublisher.state == "off":
#     pass
#
# print("camera on")
# camera = Camera(cameraPublisher)