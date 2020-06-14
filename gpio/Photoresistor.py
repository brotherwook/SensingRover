from gpio.Pcf8591 import Pcf8591
import time
import threading

class Photoresistor(threading.Thread):
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain
        self.photolevel = 0
        super().__init__(daemon=True)
        super().start()

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value

    def run(self):
        while True: #####
            self.photolevel = self.read()
            time.sleep(0.5) #####

if __name__ == '__main__':
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Photoresistor(pcf8591, 0)
        while True:
            value = sensor.read()
            print("조도 : ", value)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")