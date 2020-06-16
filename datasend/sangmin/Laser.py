import RPi.GPIO as GPIO

class LaserEmitter:

    ON = "on"
    OFF = "off"

    def __init__(self, channel):
        self.__channel = channel
        self.state = LaserEmitter.ON
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        self.state = LaserEmitter.ON
        GPIO.output(self.__channel, GPIO.LOW)

    def off(self):
        self.state = LaserEmitter.OFF
        GPIO.output(self.__channel, GPIO.HIGH)
