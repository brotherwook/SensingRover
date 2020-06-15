import RPi.GPIO as GPIO
import time
import threading


class Tracker(threading.Thread):
    def __init__(self, trackpin):
        self.___trackpin = trackpin
        self.state = None
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(trackpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        super().__init__()
        super().start()

    def run(self):
        while True:
            self.read()

    def read(self):
        if GPIO.input(self.___trackpin) == GPIO.LOW:
            self.state = "White"
        else:
            self.state = "Black"


if __name__ == '__main__':     # Program start from here
    tracker = Tracker(32)
    try:
        while True:
            tracker.read()
            time.sleep(0.5)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print()
    finally:
        GPIO.cleanup()
        print("program exit")
