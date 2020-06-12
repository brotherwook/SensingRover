import RPi.GPIO as GPIO
import time

class RgbLed:
    #  상수 선언
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

    # 생성자 선언
    def __init__(self, redpin=None, greenpin=None, bluepin=None):
        self.__redpin = redpin
        self.__greenpin = greenpin
        self.__bluepin = bluepin
        self.state = "off"

        # GPIO 설정
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        if redpin is not None:
            GPIO.setup(redpin, GPIO.OUT, initial=GPIO.HIGH)
        if greenpin is not None:
            GPIO.setup(greenpin, GPIO.OUT, initial=GPIO.HIGH)
        if bluepin is not None:
            GPIO.setup(bluepin, GPIO.OUT, initial=GPIO.HIGH)

    def red(self):
        self.state = RgbLed.RED
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.LOW)
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.HIGH)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.HIGH)

    def green(self):
        self.state = RgbLed.GREEN
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.LOW)
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.HIGH)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.HIGH)

    def blue(self):
        self.state = RgbLed.BLUE
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.LOW)
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.HIGH)
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.HIGH)

    def off(self):
        self.state = "off"
        if self.__redpin is not None:
            GPIO.output(self.__redpin, GPIO.HIGH)
        if self.__greenpin is not None:
            GPIO.output(self.__greenpin, GPIO.HIGH)
        if self.__bluepin is not None:
            GPIO.output(self.__bluepin, GPIO.HIGH)

if __name__ == "__main__":
    try:
        led = RgbLed(29, 31, 36)
        for i in range(2):
            led.red()
            time.sleep(1)
            led.off()

            led.blue()
            time.sleep(1)
            led.off()

            led.green()
            time.sleep(1)
            led.off()

    # Ctrl+C눌렀을 때 예외 발생
    except KeyboardInterrupt:
        print()
    finally:
        led.off()
        print("program exit")
