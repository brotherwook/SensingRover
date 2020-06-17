import RPI.GPIO as GPIO

class TrackingSensor:
    def __init__(self, TrackPin, LedPin):
        self.__TrackPin = TrackPin
        self.__LedPin = LedPin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarning(False)
        GPIO.setup(TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def detect(self):
        detectColor ="Error"

        if GPIO.input(self.__TrackPin) == GPIO.LOW:
            detectColor = "White"
            GPIO.output(self.__LedPin, GPIO.LOW)
        else :
            detectColor = "Black"
            GPIO.output(self.__LedPin, GPIO.HIGH)

        return detectColor

