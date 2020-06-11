import time
import threading
import  pcf8591
import  RgbLed

class Gas:

    def __init__(self,pcf8591,ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value

if __name__ == "__main__":
    try:
        pcf8591 = pcf8591.Pcf8591(0x48)
        led = RgbLed.RgbLed(11,13,15)
        sensor = Gas(pcf8591,0)
        while True:
            gas = sensor.read()
            print("가스량: {}".format(gas))
            time.sleep(0.5)

    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")