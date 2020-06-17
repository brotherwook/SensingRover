#import Jetson.GPIO as GPIO
import RPi.GPIO as GPIO
import time

class ActiveBuzzer:
	
	ON = "on"
	OFF = "off"

	def __init__(self,channel):
		self.__channel = channel
		self.state = ActiveBuzzer.OFF
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

	def on(self):
		self.state = ActiveBuzzer.ON
		GPIO.output(self.__channel, GPIO.LOW)

	def off(self):
		self.stat = ActiveBuzzer.OFF
		GPIO.output(self.__channel, GPIO.HIGH)


if __name__ == "__main__":

	try:
	
		buzzer = ActiveBuzzer(35)
		
		for i in range(5):
			buzzer.on()
			time.sleep(0.5)
			buzzer.off()
			time.sleep(0.5)

	except KeyboardInterrupt:
		print()
	finally:
		buzzer.off()
		GPIO.cleanup()
		print("program exit")


