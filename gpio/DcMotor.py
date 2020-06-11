import time
import RPi.GPIO as GPIO
import gpio.Pca9685 as Pca9685

class DcMotor:
    def __init__(self, pca9685):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        channel = [11, 12, 13, 15]
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
        self.__pca9685 = pca9685

    def forward(self):
        # 왼쪽 바퀴
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)

        # 오른쪽 바퀴
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    def backward(self):
        # 왼쪽 바퀴
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)

        # 오른쪽 바퀴
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)

    def stop(self):
        # 왼쪽 바퀴
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.HIGH)

        # 오른쪽 바퀴
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.HIGH)

    def setSpeed(self, speed):
        # 0 ~ 4095
        self.__pca9685.write(5, speed)
        self.__pca9685.write(4, speed)


if __name__ == '__main__':
    pca9685 = Pca9685.Pca9685()
    motor = DcMotor(pca9685)

    # 전진
    motor.forward()
    motor.setSpeed(4095)
    time.sleep(5)

    # 정지
    motor.stop()
    time.sleep(10)

    # 후진
    motor.backward()
    motor.setSpeed(4095)
    time.sleep(5)

    motor.stop()
    GPIO.cleanup()