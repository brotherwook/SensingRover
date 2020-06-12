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
        self.pcf8591 = Pcf8591(0x48)
        self.pca9685 = Pca9685()
        self.buzzer = ActiveBuzzer(35)
        self.DCMoter = DcMotor(self.pca9685)
        self.gas = Gas(self.pcf8591, 2) # 클래스 생성자에서 스레드 생성
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
    def message(self):
        message = {}
        message["buzzer"] = self.buzzer.state # on, off
        message["dcmotor_speed"] = self.dcmotor.speed # pwm값
        message["dcmotor_dir"] = self.dcmotor.direction # forward, backward
        message["gas"] = self.gas.gaslevel # 계속 변화하는 가스 수치 값
        message["distance"] = self.hcsr.dist # 계속 변화하는 거리값
        message["laser"] = self.laser.state # on, off
        message["photo"] = self.photo.photolevel # 계속 변화하는 조도값
        message["led"] = self.led.state # red, green, blue
        message["servo1"] = self.servo1.cur_angle # servo모터 각도
        message["servo2"] = self.servo2.cur_angle
        message["servo3"] = self.servo3.cur_angle
        message["servo4"] = self.servo4.cur_angle
        message["temperature"] = self.thermistor.cur_temp # 계속 변화하는 온도 ( 지금은 1초 주기인데 늘려도 괜찮을듯)
        message["tracker"] = self.tracker.state # black , white 수시로 변경되서 얘도 스레딩처리
        message = json.dumps(message)
        return message

    def write(self,message):
        self.DCMoter.setSpeed(message["speed"])