import RPI.GPIO as GPIO

class LazerEmitter:

    ON = "on"
    OFF = "off"

    def __init__(self, channel):
        self.__channel = channel
        self.state = LazerEmitter.ON
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

    def on(self):
        self.state = LazerEmitter.ON
        GPIO.output(self.__channel, GPIO.LOW)

    def off(self):
        self.state = LazerEmitter.OFF
        GPIO.output(self.__channel, GPIO.HIGH)
