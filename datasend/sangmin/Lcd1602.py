import time
import smbus
import Thermistor
import pcf8591
import socket

# 리눅스의 경우 외부와 연결을 한번은 해줘야 ip를 가져올 수 있다.
def get_interface_ipaddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 아래의 ip는 공유기의 ip이다.
    s.connect(("192.168.3.1",0))
    ipAddress = s.getsockname()[0]
    s.close()
    return ipAddress

class Lcd1602:
	def __init__(self, addr):
		self.__bus = smbus.SMBus(1)
		self.__addr = addr
		self.init()

	def init(self):
		try:
			self.send_command(0x33) # Must initialize to 8-line mode at first
			time.sleep(0.005)
			self.send_command(0x32) # Then initialize to 4-line mode
			time.sleep(0.005)
			self.send_command(0x28) # 2 Lines & 5*7 dots
			time.sleep(0.005)
			self.send_command(0x0C) # Enable display without cursor
			time.sleep(0.005)
			self.send_command(0x01) # Clear Screen
			self.__bus.write_byte(self.__addr, 0x08)
		except:
			return False
		else:
			return True

	# 8bit(word단위)를 전송하는 메소드
	def write_word(self, data):
		temp = data | 0x08
		self.__bus.write_byte(self.__addr ,temp)

	# 동작을 시키기위한 명령어
	def send_command(self, comm):
		# Send bit7-4 firstly
		buf = comm & 0xF0
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

		# Send bit3-0 secondly
		buf = (comm & 0x0F) << 4
		buf |= 0x04               # RS = 0, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

	# 사용자가 출력시키고 싶은 문자열
	def send_data(self, data):
		# Send bit7-4 firstly
		buf = data & 0xF0
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

		# Send bit3-0 secondly
		buf = (data & 0x0F) << 4
		buf |= 0x05               # RS = 1, RW = 0, EN = 1
		self.write_word(buf)
		time.sleep(0.002)
		buf &= 0xFB               # Make EN = 0
		self.write_word(buf)

	def clear(self):
		self.send_command(0x01) # Clear Screen

	def openlight(self):  # Enable the backlight
		self.__bus.write_byte(0x27,0x08)
		self.__bus.close()

	# y는 line num(2줄), x는 한 line에 들어갈수있는 글자수(16자)중 시작 위치
	def write(self, x, y, str):
		if x < 0:
			x = 0
		if x > 15:
			x = 15
		if y <0:
			y = 0
		if y > 1:
			y = 1

		# Move cursor
		addr = 0x80 + 0x40 * y + x
		self.send_command(addr)

		for chr in str:
			self.send_data(ord(chr))

if __name__ == '__main__':
	local_ip= get_interface_ipaddress()
	pcf8591 = pcf8591.Pcf8591(0x48)
	sensor = Thermistor.Thermistor(pcf8591,0)

	lcd = Lcd1602(0x27)

	while True:
		temperature = str(sensor.read())
		lcd.write(0, 0, local_ip)
		lcd.write(0, 1, temperature)
		time.sleep(0.5)
