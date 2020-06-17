import time
import math
from gpio.Pcf8591 import Pcf8591
import threading

class Thermistor(threading.Thread):
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain
        self.cur_temp = 0
        super().__init__(daemon=True)
        super().start()

    def read(self):
        analog = self.__pcf8591.read(self.__ain)
        if analog <= 0:
            return self.read()
        temp = 5 * float(analog) / 255
        temp = 10000 * temp / (5-temp)
        temp = 1 / (((math.log(temp/10000)) / 3950) + (1/(273.15 + 25)))
        return temp - 273.15

    def run(self):
        while True:
            self.cur_temp = self.read()
            time.sleep(0.5)


if __name__ == '__main__':
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Thermistor(pcf8591, ain=1)
        while True:
            temperature = sensor.read()
            print('섭씨 온도: {}도'.format(temperature))
            time.sleep(1)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")