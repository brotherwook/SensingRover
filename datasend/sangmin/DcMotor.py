import RPi.GPIO as GPIO
from Pca9685 import Pca9685
import time

class DcMotor:
    def __init__(self, out1, out2, pca9685, pwm):
        self.__out1 = out1
        self.__out2 = out2
        self.__pca9685 = pca9685
        self.__pwm = pwm
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
    #, initial=GPIO.LOW
        GPIO.setup(self.__out1, GPIO.OUT)
        GPIO.setup(self.__out2, GPIO.OUT)

    def setSpeed(self,step):
        self.__pca9685.write(self.__pwm, step)

    def forward(self):
        GPIO.output(self.__out1,GPIO.HIGH)
        GPIO.output(self.__out2,GPIO.LOW)

    def backward(self):
        GPIO.output(self.__out1, GPIO.LOW)
        GPIO.output(self.__out2, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.__out1, GPIO.LOW)
        GPIO.output(self.__out2, GPIO.LOW)
        self.setSpeed(0)

if __name__ == "__main__":
    pca9685 = Pca9685()

    dcMotor1 =DcMotor(11,12,pca9685,5)
    dcMotor2 =DcMotor(13,15,pca9685,4)

    dcMotor1.forward()
    print("1")
    dcMotor2.forward()
    print("2")
    dcMotor1.setSpeed(4095)
    print("3")
    dcMotor2.setSpeed(4095)
    print("4")
    time.sleep(5)

    dcMotor1.stop()
    dcMotor2.stop()
    time.sleep(2)

    dcMotor1.backward()
    dcMotor2.backward()
    dcMotor1.setSpeed(4095)
    dcMotor2.setSpeed(4095)
    time.sleep(5)

    dcMotor1.stop()
    dcMotor2.stop()


