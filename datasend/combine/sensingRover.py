from gpio.Laser import Laser
from gpio.HcSr04 import HcSr04
from gpio.Sg90 import Sg90
from gpio.DcMotor import DcMotor
from gpio.Tracker import Tracker
from gpio.Pcf8591 import Pcf8591
from gpio.Pca9685 import Pca9685
from gpio.Buzzer import ActiveBuzzer
from gpio.Gas import Gas
from gpio.Photoresistor import Photoresistor
from gpio.RgbLed import RgbLed
from gpio.Thermistor import Thermistor
from gpio.Lcd1602 import Lcd1602
import json

class SensingRover:
    def __init__(self):
        self.frontTireAngle = 75

        self.pcf8591 = Pcf8591(0x48)
        self.pca9685 = Pca9685()
        self.buzzer = ActiveBuzzer(35)
        self.dcmotor = DcMotor(self.pca9685)
        self.gas = Gas(self.pcf8591, ain=2) # 클래스 생성자에서 스레드 생성
        self.hcsr = HcSr04(trigpin=40, echopin=38) # 클래스 생성자에서 스레드 생성
        self.laser = Laser(37)
        self.photo = Photoresistor(self.pcf8591, 0) # 클래스 생성자에서 스레드 생성
        self.led = RgbLed(redpin=16, greenpin=18, bluepin=22)
        self.servo1 = Sg90(self.pca9685, 0)  # 카메라 서보1
        self.servo2 = Sg90(self.pca9685, 1)  # 카메라 서보2
        self.servo3 = Sg90(self.pca9685, 8)  # 초음파 서보
        self.servo4 = Sg90(self.pca9685, 9)  # 앞바퀴 서보
        self.thermistor = Thermistor(self.pcf8591, 1) # 클래스 생성자에서 스레드 생성
        self.tracker = Tracker(32) # 클래스 생성자에서 스레드 생성
        self.lcd = Lcd1602(0x27)

    def sensorMessage(self):
        message = {}
        message["buzzer"] = self.buzzer.state # on, off
        message["dcmotor_speed"] = str(self.dcmotor.speed) # pwm값
        message["dcmotor_dir"] = self.dcmotor.direction # forward, backward
        message["gas"] = str(self.gas.gaslevel) # 계속 변화하는 가스 수치 값
        message["distance"] = str(self.hcsr.dist) # 계속 변화하는 거리값
        message["laser"] = self.laser.state # on, off
        message["photo"] = str(self.photo.photolevel) # 계속 변화하는 조도값
        message["led"] = self.led.state # red, green, blue
        message["servo1"] = str(self.servo1.cur_angle)  # 카메라 서보1
        message["servo2"] = str(self.servo2.cur_angle)  # 카메라 서보2
        message["servo3"] = str(self.servo3.cur_angle)  # 초음파 서보
        message["servo4"] = str(self.servo4.cur_angle)  # 앞바퀴 서보
        message["temperature"] = str(self.thermistor.cur_temp) # 계속 변화하는 온도 ( 지금은 1초 주기인데 늘려도 괜찮을듯)
        message["tracker"] = self.tracker.state # black , white 수시로 변경되서 얘도 스레딩처리
        message = json.dumps(message)
        return message
    
    def cameraMessage(self): 
        message = self.camera.message
        return message

    # if elif 조건에 없으면 아무동작 안하게 만들기
    def write(self, message, topic):

        # ============ 형욱 예나 ===============
        if topic.__contains__("/servo3"):
            if message.isdecimal():
                self.servo3.angle(int(message))

        if topic.__contains__("/laser"):
            if message == "on":
                self.laser.lazerOn()
            elif message == "off":
                self.laser.lazerOff()

        if topic.__contains__("/speed"):
            if message.isdecimal():
                self.dcmotor.setSpeed(int(message))

        if topic.__contains__("/direction"):
            if message == "forward":
                self.dcmotor.forward()
            elif message == "backward":
                self.dcmotor.backward()
            elif message == "stop":
                self.dcmotor.stop()

        if topic.__contains__("/buzzer"):
            if message == "on":
                self.buzzer.on()
            elif message == "off":
                self.buzzer.off()
            else:
                pass

        # =============== 성진 휘래 =================
        if message == 'CameraUp':
            angleud = self.servo1.cur_angle
            angleud += 5
            if angleud > 180:
                angleud = 180
            self.servo1.angle(angleud)
        if message == 'CameraDown':
            angleud = self.servo1.cur_angle
            angleud -= 5
            if angleud < 0:
                angleud = 0
            self.servo1.angle(angleud)
        if message == 'CameraLeft':
            anglelr = self.servo2.cur_angle
            anglelr += 5
            if anglelr > 145:
                anglelr = 145
            self.servo2.angle(anglelr)
        if message == 'CameraRight':
            anglelr = self.servo2.cur_angle
            anglelr -= 5
            if anglelr < 35:
                anglelr = 35
            self.servo2.angle(anglelr)
        if message == 'CameraCenter':
            self.servo1.angle(30)
            self.servo2.angle(90)

        # ========== 상민 찬혁 ===========
            # 좌회전
        if message == "37":
            self.frontTireAngle -= 5
            if self.frontTireAngle < 45:
                self.frontTireAngle = 45
            self.servo4.angle(self.frontTireAngle)

        # 우회전
        if message == "39":
            self.frontTireAngle += 5
            if self.frontTireAngle > 105:
                self.frontTireAngle = 105
            self.servo4.angle(self.frontTireAngle)

        # 정면
        if message == "97":
            self.frontTireAngle = 75
            self.servo4.angle(self.frontTireAngle)

        if message == "13":
            self.buzzer.on()