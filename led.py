import RPi.GPIO as GPIO
import time
import threading

BCM_led = -1
terminate = False

class FlashingLED(threading.Thread):
    def __init__(self, ledOn, ledOff):
        threading.Thread.__init__(self)
        self.running = threading.Event()
        self.ledOn = ledOn
        self.ledOff = ledOff

    def run(self):
        while not self.running.is_set():
            GPIO.output(BCM_led, GPIO.HIGH)
            self.running.wait(self.ledOn)
            GPIO.output(BCM_led, GPIO.LOW)
            self.running.wait(self.ledOff)

    def stop(self):
        self.running.set()


def bing(n, d = 0.2):
    for _ in range(n):
        if terminate:
            return
        GPIO.output(BCM_led, GPIO.HIGH)
        time.sleep(d)
        GPIO.output(BCM_led, GPIO.LOW)
        time.sleep(0.3)
    time.sleep(1.0)

def encode(digit):
    if not terminate:
        bing((digit // 100)%10 + 1, 0.8)
    if not terminate:
        bing((digit // 10)%10 + 1, 0.4)
    if not terminate:
        bing((digit % 10) + 1, 0.2)
    if not terminate:
        time.sleep(1.0)

def encodeIP(ipaddr):
    bing(3, 0.05)
    time.sleep(1.0)
    octets = ipaddr.split('.')
    for i, octet in enumerate(octets):
        if terminate:
            return
        time.sleep(1.0)
        #bing(i+1, 0.1)
        encode(int(octet))
        time.sleep(1.0)
    time.sleep(1.0)


if __name__ == '__main__':
    BCM_led = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BCM_led, GPIO.OUT)

    try:
        btnled = FlashingLED(0.1, 0.9)
        btnled.start()
        print("start")
        time.sleep(5)
        print("stop")
    except (KeyboardInterrupt, SystemExit): # when you press ctrl+c
        print("cenceled")
    finally:
        btnled.stop()
        print("end")
