# sensor module
from Gas import Gas
from Thermistor import Thermistor
from Tracking import TrackingSensor
from Photoresistor  import Photoresistor
from HcSr04 import HcSr04       #초음파, 거리 측정

# actuator module
from Buzzer import ActiveBuzzer
from DcMotor import DcMotor
from Laser import LaserEmitter
from Lcd1602 import Lcd1602
from RgbLed import RgbLed
from Sg90 import Sg90     #서보 모터, 각도 조절

# Hardware PWM control module
from Pca9685 import Pca9685

# ADC(Analog Digital Convertor) & DAC(Digital Analog convertor) module
from pcf8591 import Pcf8591

class SensingRover:
    def __init__(self):

        # sensor module
        self.pcf8591 = Pcf8591(0x48)
        self.gasSensor = Gas(self.pcf8591, 2)
        self.thermistor =  Thermistor(self.pcf8591, 1)
        self.trackingSensor = TrackingSensor(32)
        self.photoresistor = Photoresistor(self.pcf8591,0)
        self.ultrasonicSensor = HcSr04(38,40)

        # SensingRover 생성시 센서 on
        self.gasSensor.on()
        self.thermistor.on()
        self.trackingSensor.on()
        self.photoresistor.on()
        self.ultrasonicSensor.on()

        # actuator module
        """
         웹 클라이언트 구현 후
        """

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



