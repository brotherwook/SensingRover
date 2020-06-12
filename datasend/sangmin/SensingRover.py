import RPi.GPIO as GPIO
import threading
import time
import json
import pcf8591
import Gas
import mqtt_publisher

class SensingRover:
    def __init__(self):
        self.__pcf8591 = pcf8591.Pcf8591(0X48)
        self.__gasSensor = Gas.Gas(self.__pcf8591, 0)
        self.gasFlag = False
        self.curGas=-1

    def gasCheck(self):
        self.gasFlag = True
        while self.gasFlag:
            self.curGas = self.__gasSensor.read()

    def gasCheckOn(self):
        self.gasThread = threading.Thread(target=self.gasCheck, deamon=True)
        self.gasThread.start()

    def gasCheckOff(self):
        self.gasFlag = False
        self.curGas=-1


if __name__ == "__main__":
    sensingRover = SensingRover()
    sensingRover.gasCheckOn()
    while True:
        gas = sensingRover.curGas
        message = {"gas" : gas}
        if gas == -1:
            continue
            # 다른 센서 값과 같이 보낼시 continue X

        message =json.dumps(message)

        time.sleep(1)
