import time
import math
import threading
from pcf8591 import Pcf8591


class Photoresistor():

    def __init__(self,pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain
        self.lightValue = None
        self.stop = False

    def read(self):
        try:
            temp = self.__pcf8591.read(self.__ain)
            temp = 5 * float(temp) / 255
            temp = 10000 * temp / (5 - temp)
            temp = 1 / ((math.log(temp / 10000) / 3950) + (1 / (273.15 + 25)))
        except:
            return self.lightValue
        else:
            return (temp - 273.15)

    def run(self):
        while self.stop:
            self.lightValue = self.read()
            time.sleep(0.5)

    def on(self):
        self.stop = True
        thread = threading.Thread(target=self.run, daemon= True)
        thread.start()

    def off(self):
        self.stop = False
        self.lightValue = None

if __name__ == "__main__":
    try:
        pcf8591 = Pcf8591(0x48)
        sensor = Photoresistor(pcf8591,0)
        while True:
            light = sensor.read()
            print("조도 :{}".format(light))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")


