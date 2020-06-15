import time
import gpio.Pca9685 as Pca9685
import gpio.Sg90 as Sg90
# import datasend.sungjin.mqttPublisher as publisher
# import datasend.sungjin.mqttSubscriber as subscriber

pca9685 = Pca9685.Pca9685()
sg90 = Sg90.Sg90(pca9685)
# capublisher = publisher.MqttPublisher(brokerIp="192.168.3.131", topic='/sensor')
# casubscriber = subscriber.MqttSubscriber(brokerip="192.168.3.131", topic='/command')

angleud = 0
anglelr = 0

while True:
    sg90.angle(0, angleud)
    sg90.angle(2, anglelr)
    message = {"motor": "camera", "cudangle": angleud, "clrangle": anglelr}
    # capublisher.publish(message)
    time.sleep(0.1)
    if anglelr == 180:
        break
    angleud += 1
    anglelr += 1

sg90.angle(0, 15)
sg90.angle(2, 90)
message = {"motor": "camera", "cudangle": 15, "clrangle": 90}
# capublisher.publish(message)
