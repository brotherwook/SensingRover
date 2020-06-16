import RPi.GPIO as GPIO
import time
import threading


class Laser:
    def __init__(self, lazerpin):
        self.__lazerpin = lazerpin    # pin11
        self.state = "off"
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(lazerpin, GPIO.OUT)   # Set LedPin's mode is output
        GPIO.output(lazerpin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

    def lazerOn(self):
        self.state = "on"
        GPIO.output(self.__lazerpin, GPIO.LOW)  # led on

    def lazerOff(self):
        self.state = "off"
        GPIO.output(self.__lazerpin, GPIO.HIGH) # led off

    def destroy(self):
        GPIO.output(self.__lazerpin, GPIO.HIGH)     # led off
        GPIO.cleanup()                     # Release resource


if __name__ == '__main__':     # Program start from here
    laser = Laser(37)
    try:
        while True:
            laser.lazerOn()
            time.sleep(0.5)
            laser.lazerOff()
            time.sleep(0.5)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print()
    finally:
        laser.destroy()
        print("program exit")
