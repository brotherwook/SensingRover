import time
import math
from pcf8591 import Pcf8591
from Buzzer import ActiveBuzzer
from RgbLed import RgbLed
class Thermistor:

    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        temp = self.__pcf8591.read(self.__ain)  #0~255
        temp = 5 * float(temp)/255
        temp = 10000* temp/(5-temp)
        temp = 1/((math.log(temp/10000)/3950) + (1/(273.15+25)))
        return (temp-273.15)

if __name__ == "__main__":
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Thermistor(pcf8591,1)
        bz = ActiveBuzzer(35)
        led = RgbLed(16,18,22)

        while True:
            temperature = sensor.read()
            print("섭씨 온도: {}도".format(temperature))
            time.sleep(0.5)
            if(temperature>30):
                bz.on()
                led.red()
            else:
                bz.off()
                led.green()

    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")


