import RPi.GPIO as GPIO
import time

BCM_led = -1
terminate = False

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
