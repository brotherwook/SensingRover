import time
# sensor module
from Gas import Gas
from Thermistor import Thermistor
from Tracking import TrackingSensor
from Photoresistor  import Photoresistor
from HcSr04 import HcSr04       # 초음파, 거리 측정

# actuator module
from Buzzer import ActiveBuzzer
from DcMotor import DcMotor
from Laser import LaserEmitter
from Lcd1602 import Lcd1602
from RgbLed import RgbLed
from Sg90 import Sg90     # 서보 모터, 각도 조절
from DcMotor import DcMotor # DC 모터, 속도조절

# Hardware PWM control module
from Pca9685 import Pca9685

# ADC(Analog Digital Convertor) & DAC(Digital Analog convertor) module
from pcf8591 import Pcf8591

class SensingRover:
    def __init__(self):

        self.speed=1000
        self.frontTireAngle = 75
        self.str = "Stop!!"
        self.pcf8591 = Pcf8591(0x48)
        self.pca9685 = Pca9685()


        # sensor module
        self.gasSensor = Gas(self.pcf8591, 2)
        self.thermistor =  Thermistor(self.pcf8591, 1)
        self.trackingSensor = TrackingSensor(32)
        self.photoresistor = Photoresistor(self.pcf8591,0)
        self.ultrasonicSensor = HcSr04(38,40)

        # actuator module
        self.dcMotorLeft = DcMotor(11,12,self.pca9685,5)
        self.dcMotorRight = DcMotor(13,15,self.pca9685,4)
        self.sg90 = Sg90(self.pca9685)
        self.buzzer = ActiveBuzzer(35)
        self.lcdScreen = Lcd1602(0x27)

        # SensingRover 생성시 센서 on
        self.gasSensor.on()
        self.thermistor.on()
        self.trackingSensor.on()
        self.photoresistor.on()
        self.ultrasonicSensor.on()
    def sensorMessage(self):
        message = {}
        if self.gasSensor.gasValue != None:
            message["gasValue"] =self.gasSensor.gasValue

        if self.thermistor.temperature != None:
            message["temperature"] = self.thermistor.temperature

        if self.trackingSensor.detectColor != None:
            message["detectColor"] = self.trackingSensor.detectColor

        if self.photoresistor.lightValue != None:
            message["lightValue"] = self.photoresistor.lightValue

        if self.ultrasonicSensor.dist != None:
            message["dist"] = self.ultrasonicSensor.dist

        return message

    # action method

    def action(self, command, topic):

        # forward
        if command == "38":
            print(self.speed)
            self.speed += 100
            if self.speed >4095:
                self.speed = 4095
            self.dcMotorLeft.forward()
            self.dcMotorRight.forward()
            self.dcMotorLeft.setSpeed(self.speed)
            self.dcMotorRight.setSpeed(self.speed)
            if self.str != "Forward!!":
                self.lcdScreen.write(0, 0, self.str)
                self.str = "Forward!!"

        # backward
        elif command == "40":
            self.speed += 100
            if self.speed > 4095:
                self.speed = 4095
            self.dcMotorLeft.backward()
            self.dcMotorRight.backward()
            self.dcMotorLeft.setSpeed(self.speed)
            self.dcMotorRight.setSpeed(self.speed)
            print(self.str)
            if self.str != "Backward!!":
                self.lcdScreen.write(0, 0, self.str)
                self.str = "Backward!!"
        # break
        elif command == "32":
            self.dcMotorLeft.stop()
            self.dcMotorRight.stop()
            self.speed = 1000
            print(self.str)
            if self.str != "Break!!":
                self.lcdScreen.write(0, 0, self.str)
                self.str = "Break!!"

        elif command == "slow":
            self.dcMotorLeft.stop()
            self.dcMotorRight.stop()
            self.speed = 1000
            self.buzzer.off()
            print(self.str)
            if self.str != "Stop!!":
                self.lcdScreen.write(0, 0, self.str)
                self.str = "Stop!!"
        # 좌회전
        elif command == "37":
            self.frontTireAngle -= 5
            if self.frontTireAngle <45:
                self.frontTireAngle = 45
            self.sg90.angle(14,self.frontTireAngle)
        
        # 우회전
        elif command == "39":
            self.frontTireAngle += 5
            if self.frontTireAngle >105:
                self.frontTireAngle = 105
            self.sg90.angle(14,self.frontTireAngle)

        # 정면
        elif command == "97":
            self.frontTireAngle = 75
            self.sg90.angle(14, self.frontTireAngle)

        elif command == "13":
            self.buzzer.on()