import paho.mqtt.client as mqtt
import threading
from datasend.sungjin.sample01.sensingRover import SensingRover


# model02은 sensor publisher, camera publisher, command subscriber 3개로 분리한 것
# 사용하기전에 ###################!!!!!!!!!!!!!!!!!!!!!! 부분 수정후 사용

class CommandSubscriber:
    def __init__(self, brokerIp=None, brokerPort=1883, commandTopic=None, sensingRover=None):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__commandTopic = commandTopic
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message
        self.__stop = False
        self.sensingRover = sensingRover

    def __on_connect(self, client, userdata, flags, result_code):
        print("** mqtt connected **")
        self.__subscribe(self.__client)

    def __on_disconnect(self, client, userdata, rc):
        print("** mqtt disconnected **")

    def __on_message(self, client, userdata, message):
        data = str(message.payload, encoding="UTF-8")
        print(data)
        angleud = self.sensingRover.servo1.cur_angle
        anglelr = self.sensingRover.servo2.cur_angle
        if data == 'CameraUp':
            angleud += 5
            if angleud > 180:
                angleud = 180
            self.sensingRover.servo1.angle(angleud)
        if data == 'CameraDown':
            angleud -= 5
            if angleud < 0:
                angleud = 0
            self.sensingRover.servo1.angle(angleud)
        if data == 'CameraLeft':
            anglelr += 5
            if anglelr > 145:
                anglelr = 145
            self.sensingRover.servo2.angle(anglelr)
        if data == 'CameraRight':
            anglelr -= 5
            if anglelr < 35:
                anglelr = 35
            self.sensingRover.servo2.angle(anglelr)
        if data == 'CameraCenter':
            self.sensingRover.servo1.angle(30)
            self.sensingRover.servo2.angle(90)
        if data == 'LedRed':
            if self.sensingRover.rgbled.state == "off":
                self.sensingRover.rgbled.red()
            elif self.sensingRover.rgbled.state == 'red':
                self.sensingRover.rgbled.off()
            elif self.sensingRover.rgbled.state == 'green':
                self.sensingRover.rgbled.yellow()
            elif self.sensingRover.rgbled.state == 'blue':
                self.sensingRover.rgbled.magenta()
            elif self.sensingRover.rgbled.state == 'cyan':
                self.sensingRover.rgbled.white()
            elif self.sensingRover.rgbled.state == 'magenta':
                self.sensingRover.rgbled.blue()
            elif self.sensingRover.rgbled.state == 'yellow':
                self.sensingRover.rgbled.green()
            elif self.sensingRover.rgbled.state == 'white':
                self.sensingRover.rgbled.cyan()
        if data == 'LedGreen':
            if self.sensingRover.rgbled.state == 'off':
                self.sensingRover.rgbled.green()
            elif self.sensingRover.rgbled.state == 'red':
                self.sensingRover.rgbled.yellow()
            elif self.sensingRover.rgbled.state == 'green':
                self.sensingRover.rgbled.off()
            elif self.sensingRover.rgbled.state == 'blue':
                self.sensingRover.rgbled.cyan()
            elif self.sensingRover.rgbled.state == 'cyan':
                self.sensingRover.rgbled.blue()
            elif self.sensingRover.rgbled.state == 'magenta':
                self.sensingRover.rgbled.white()
            elif self.sensingRover.rgbled.state == 'yellow':
                self.sensingRover.rgbled.red()
            elif self.sensingRover.rgbled.state == 'white':
                self.sensingRover.rgbled.magenta()
        if data == 'LedBlue':
            if self.sensingRover.rgbled.state == 'off':
                self.sensingRover.rgbled.blue()
            elif self.sensingRover.rgbled.state == 'red':
                self.sensingRover.rgbled.magenta()
            elif self.sensingRover.rgbled.state == 'green':
                self.sensingRover.rgbled.cyan()
            elif self.sensingRover.rgbled.state == 'blue':
                self.sensingRover.rgbled.off()
            elif self.sensingRover.rgbled.state == 'cyan':
                self.sensingRover.rgbled.white()
            elif self.sensingRover.rgbled.state == 'magenta':
                self.sensingRover.rgbled.green()
            elif self.sensingRover.rgbled.state == 'yellow':
                self.sensingRover.rgbled.white()
            elif self.sensingRover.rgbled.state == 'white':
                self.sensingRover.rgbled.yellow()
        if data == 'LedOff':
            print('||||||||||||||||||||||||||||||||')
            self.sensingRover.rgbled.off()
        # SensingRover의 write() 호출
        # print("구독 내용: {}, 토픽: {}, Qos: {}".format(
        #     str(message.payload, encoding="UTF-8"),
        #     message.topic,
        #     message.qos
        # ))

    def __connect(self):
        self.__stop = False
        self.__client.connect(self.__brokerIp, self.__brokerPort)
        self.__client.loop_forever()

    def __subscribe(self, client):
        topic = self.__commandTopic
        self.__client.subscribe(topic)

    def start(self):
        loopThread = threading.Thread(target=self.__connect)
        loopThread.start()

    def stop(self):
        self.__stop = True
        self.__client.disconnect()


if __name__ == "__main__":
    commandSubscriber = CommandSubscriber(brokerIp="192.168.3.250", brokerPort=1883,
                                          commandTopic="/command")  ###################!!!!!!!!!!!!!!!!!!!!!!
    commandSubscriber.start()
