import RPi.GPIO as GPIO
import time


class Tracker:
    def __init__(self, trackpin):
        self.___trackpin = trackpin
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(trackpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read(self):
        if GPIO.input(self.___trackpin) == GPIO.LOW:
            print('...White line is detected')
        else:
            print('...Black line is detected')


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