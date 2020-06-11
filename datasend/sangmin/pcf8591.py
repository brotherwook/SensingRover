import smbus

class Pcf8591:
    def __init__(self, addr):
        # Jetson Nano Board는 i2c bus가 두개가 존재 0번, 1번
        # 0번은 board 내부에서 사용하는 선, 개발자는 1번을 제어할 수 있다.
        self.__bus = smbus.SMBus(1)

        # 장치(PCF8591) I2C bus 번호
        self.__addr = addr
    # channel: AIN 0~3,
    def read(self, channel):
        try:
            if channel == 0:
                self.__bus.write_byte(self.__addr, 0x40)
            elif channel == 1:
                self.__bus.write_byte(self.__addr, 0x41)
            elif channel == 2:
                self.__bus.write_byte(self.__addr, 0x42)
            elif channel == 3:
                self.__bus.write_byte(self.__addr, 0x43)
            self.__bus.read_byte(self.__addr)
            value = self.__bus.read_byte(self.__addr)
        except Exception as e:
            print(e)
            # ADC(Analog to Digital Converter는 0~255값만 전달한다. value가 -1일 경우 오류로 판단
            value=-1
        return value

    # value: AOUT으로 출력되는 값, 반드시 정수형태여야 한다.
    def write(self, value):
        try:
            value = int(value)
            # master에서 데이터를 보낼 때는 어떠한 channel로 내보내도 AOUT으로 연결 시켜준다.
            self.__bus.write_byte_data(self.__addr, 0x40, value)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    pcf8591 = Pcf8591(0x48)

    while True:
        value = pcf8591.read(0)
        light = value * (255-125)/255 + 125
        print(light)
        pcf8591.write(light)