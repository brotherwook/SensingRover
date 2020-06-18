import time
import math
from pcf8591 import Pcf8591
from Buzzer import ActiveBuzzer
from RgbLed import RgbLed

class Photeresistor:

    def __init__(self,pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        temp = self.__pcf8591.read(self.__ain)
        temp = 5 * float(temp) / 255
        temp = 10000 * temp / (5 - temp)
        temp = 1 / ((math.log(temp / 10000) / 3950) + (1 / (273.15 + 25)))
        return (temp - 273.15)

if __name__ == "__main__":
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Photeresistor(pcf8591,0)
        bz = ActiveBuzzer(12)
        led = RgbLed(11,13,15)
        while True:
            light = sensor.read()
            print("조도 :{}".format(light))
            time.sleep(0.5)
            if(light <20):
                led.blue()
            else:
                led.off()
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")


