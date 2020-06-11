#import Jetson.GPIO as GPIO
import RPi.GPIO
import time
import threading

class Button(threading.Thread):
	def __init__(self, channel=None):
		self.__channel = channel
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(self.__channel, GPIO.IN)
		self.handler = None
		self.prevState = GPIO.HIGH
		super().__init__(daemon=True)
		self.start()

	def run(self):
		while True:
			# input함수는 blocking X -> 아무것도 입력이 없다면 HIGH상태로 생각
			curState = GPIO.input(self.__channel)
			# print(curState)
			if curState != self.prevState:
				if self.handler is not None:
					self.handler(curState)
				self.prevState = curState
			time.sleep(1)

def handler1(state):
	if state == GPIO.HIGH:
		print("button1: HIGH")
	else:
		print("button1: LOW")

def handler2(state):
	if state == GPIO.HIGH:
		print("button2: HIGH")
	else:
		print("button2: LOW")

if __name__ == "__main__":
	try:

		# initialize GPIO pin
		GPIO.setmode(GPIO.BOARD)
		GPIO.cleanup()
		# button object create
		button1 = Button(11)
		button2 = Button(12)
		# set button event handler
		button1.handler = handler1
		button2.handler = handler2
		time.sleep(1000)
	except KeyboardInterrupt:
		print()
	finally:
		GPIO.cleanup()
