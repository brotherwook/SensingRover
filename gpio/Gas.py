from gpio.Pcf8591 import Pcf8591
from gpio.Buzzer import ActiveBuzzer
import time

class Gas:
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value


if __name__ == '__main__':
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Gas(pcf8591, ain=2)
        buzzer = ActiveBuzzer(35)
        while True:
            gas = sensor.read()
            print("gas :", gas)
            if gas >= 200:
                buzzer.on()
            else:
                buzzer.off()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")

