import RPi.GPIO as GPIO
import time
import pcf8591
import Photoresistor

class SensingRover:
    def __init__(self):
        self.__pcf8591 = pcf8591.Pcf8591()
        self.__photoresitor = Photoresistor.Photeresistor(self.__pcf8591, 0)

