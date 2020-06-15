from gpio.Pcf8591 import Pcf8591
from gpio.Buzzer import ActiveBuzzer
import time
import threading

class Gas(threading.Thread):
    def __init__(self, pcf8591, ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain
        self.gaslevel = 0
        super().__init__(daemon=True)
        super().start()

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value

    def run(self):
        while True:
            self.gaslevel = self.read()
            time.sleep(0.5)
