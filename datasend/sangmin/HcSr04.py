import Jetson.GPIO as GPIO
import gpio.Buzzer as Buzzer
import time

class HcSr04:
    def __init__(self, trigpin=None, echopin=None):
        self.__trigpin = trigpin
        self.__echopin = echopin

        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)
        GPIO.setup(trigpin, GPIO.OUT)
        GPIO.setup(echopin, GPIO.IN)


    def distance(self):
        # trigger pin Low, 2마이크로초 동안 유지
        GPIO.output(self.__trigpin, GPIO.LOW)
        time.sleep(0.000002)

        # trigger pin High, 10마이크로초 동안 유지
        GPIO.output(self.__trigpin, GPIO.HIGH)
        time.sleep(0.00001)

        # trigger pin Low, 초음파 발생
        GPIO.output(self.__trigpin, GPIO.LOW)

        # echopin이 High 상태로 변할 때 까지 기다림
        count=0
        while GPIO.input(self.__echopin) == GPIO.LOW:
            count += 1
            if count >100:
                return self.distance()

        # 초음파 출발 시간 얻기
        time1 = time.time()

        # echopin이 Low 상태로 변할 때 까지 기다림
        count=0
        while GPIO.input(self.__echopin) == GPIO.HIGH:
            count += 1
            if count > 100:
                return self.distance()

        # 초음파 도착 시간 얻기
        time2 = time.time()

        during = time2 - time1
        dist = during * 340 /2 * 100
        print(during)
        return dist

if __name__ == "__main__":

    try:

        bz = Buzzer.ActiveBuzzer(13)
        sensor = HcSr04(trigpin=11, echopin=12)

        while True:
            distance = sensor.distance()
            print("거리: {}".format(distance))
            if distance <=30 :
                bz.on()
            else:
                bz.off()
            time.sleep(0.3)

    except KeyboardInterrupt:
        print()
    finally:
        GPIO.cleanup()
        print("Program Exit")
