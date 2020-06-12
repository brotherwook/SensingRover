import time
from pcf8591 import Pcf8591
from RgbLed import RgbLed
class Flame:
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value

if __name__ == "__main__":
    try:
        pcf8591 = Pcf8591(0x48)
        led = RgbLed(11,13,15)
        sensor = Flame(pcf8591,0)
        while True:
            value = sensor.read()
            print("화염: {}".format(value))
            time.sleep(0.5)

            if value <10:
                print("불이 났습니다!!")
                led.red()
            else:
                led.off()

    except KeyboardInterrupt:
        print()

    finally:
        print("Program exit")
