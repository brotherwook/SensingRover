import RPi.GPIO as GPIO
import threading
import time
class TrackingSensor():
    def __init__(self, TrackPin):
        self.__TrackPin = TrackPin
        self.detectColor = None
        self.stop = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)



    def detect(self):

        if GPIO.input(self.__TrackPin) == GPIO.LOW:
            self.detectColor = "White"
        else :
            self.detectColor = "Black"
        return self.detectColor

    def run(self):
        while self.stop:
            self.detectColor = self.detect()
            time.sleep(0.5)

    def on(self):
        self.stop = True
        thread = threading.Thread(target=self.run, daemon= True)
        thread.start()

    def off(self):
        self.stop = False
        self.detectColor = None

if __name__ == "__main__" \
               "":
    temp = TrackingSensor(32)
    while True:
        print(temp.detect())
        time.sleep(0.5)
