import RPi.GPIO as GPIO
import time
import threading


class HcSr04(threading.Thread):
    def __init__(self, trigpin=None, echopin=None):
        self.__trigpin = trigpin
        self.__echopin = echopin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trigpin, GPIO.OUT)
        GPIO.setup(echopin, GPIO.IN)
        self.dist = 0
        super().__init__(daemon=True)
        super().start()

    def distance(self):
        # trigger pin High, 10마이크로초 동안 유지
        GPIO.output(self.__trigpin, GPIO.HIGH)
        time.sleep(0.00001)

        # trigger pin Low(초음파 발생)
        GPIO.output(self.__trigpin, GPIO.LOW)

        startTime = time.time()
        stopTime = time.time()

        cnt = 0

        # echopin이 High 상태로 변할때까지 기다림
        while GPIO.input(self.__echopin) == GPIO.LOW:
            startTime = time.time()
            cnt +=1
            if cnt == 100000:
                return self.distance()

        # echopin이 Low 상태로 변할때까지 기다림
        while GPIO.input(self.__echopin) == GPIO.HIGH:
            stopTime = time.time()

        # 거리 계산(단위: cm)
        during = stopTime - startTime
        dist = during * (343 / 2) * 100
        return dist

    def run(self):
        while True:
            temp = self.distance()
            # 튀는 값 방지
            if 0 < temp < 1000:
                self.dist = temp
            time.sleep(0.3)

#########################################################
if __name__ == "__main__":
    try:
        sensor = HcSr04(trigpin=40, echopin=38)
        while True:
            print(sensor.dist)
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("Program Exit")




