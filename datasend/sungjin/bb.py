import time
import datasend.sungjin.MqttNetwork.model03.MqttPublisher as publisher
import datasend.sungjin.MqttNetwork.model03.MqttSubscriber as subscriber

publisher = publisher.MqttPublisher(brokerIp="192.168.3.131", brokerPort=1883, cameraTopic='/camerapub',
                                    sensorTopic='/sensor')
subscriber = subscriber.MqttSubscriber(brokerIp="192.168.3.131", brokerPort=1883, commandTopic="/command")
publisher.start()
subscriber.start()
if __name__ == '__main__':
    publisher.sensingRover.servo1.angle(10)
    publisher.sensingRover.servo2.angle(120)
