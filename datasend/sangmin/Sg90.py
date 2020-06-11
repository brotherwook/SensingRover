import time
import gpio.Pca9685

class Sg90:
    def __init__(self, pca9685, frequency=50):
        self.__pca9685 = pca9685
        # Pca9685가 츌력 주파수(hz)를 설정
        # 대부붙의 모터를 50hz사용
        pca9685.frequency = frequency

    def __map(self, angle):
        return int(164 + angle*((553-164)/180))

    def angle(self, channel, angle):
        self.__pca9685.write(channel, self.__map(angle))

if __name__ == "__main__":
    pca9685 =  Pca9685.Pca9685()
    sg90 = Sg90(pca9685)

    channel = 0
    # 0도
    sg90.angle(channel, 0)
    time.sleep(2)

    # 90도
    sg90.angle(channel, 90)
    time.sleep(2)

    # 180
    sg90.angle(channel, 180)
    time.sleep(2)

    print("Program exit")
