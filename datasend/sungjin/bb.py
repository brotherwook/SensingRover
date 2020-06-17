import time
import gpio.Pca9685 as Pca9685
import gpio.Sg90 as Sg90
import datasend.sungjin.MqttNetwork.model03.MqttPublisher as publisher
import datasend.sungjin.MqttNetwork.model03.MqttSubscriber as subscriber

pca9685 = Pca9685.Pca9685()
udmotor = Sg90.Sg90(pca9685, 0)
lrmotor = Sg90.Sg90(pca9685, 2)
poublisher = publisher.MqttPublisher(brokerIp="192.168.3.131", brokerPort=1883, cameraTopic='/camerapub', sensorTopic='/sensor')
