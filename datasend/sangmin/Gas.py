import time
import threading
import  pcf8591

class Gas():
    def __init__(self,pcf8591,ain=0):
        self.__pcf8591 = pcf8591
        self.__ain = ain
        self.gasValue = None
        self.stop = False

    def read(self):
        value = self.__pcf8591.read(self.__ain)
        return value

    def run(self):
        while self.stop:
            self.gasValue = self.read()
            time.sleep(0.5)

    def on(self):
        self.stop = True
        thread = threading.Thread(target=self.run, daemon= True)
        thread.start()

    def off(self):
        self.stop = False
        self.gasValue = None

if __name__ == "__main__":
    try:
        pcf8591 = pcf8591.Pcf8591(0x48)
        sensor = Gas(pcf8591,2)
        while True:
            gas = sensor.read()
            print("가스량: {}".format(gas))
            # time.sleep(0.5)

    except KeyboardInterrupt:
        print()
    finally:
        print("Program exit")