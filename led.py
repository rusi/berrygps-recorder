import RPi.GPIO as GPIO
import time

BCM_led = -1

def bing(n, d = 0.2):
    for _ in xrange(n):
        GPIO.output(BCM_led, GPIO.HIGH)
        time.sleep(d)
        GPIO.output(BCM_led, GPIO.LOW)
        time.sleep(0.3)
    time.sleep(1.0)

def encode(digit):
    bing((digit // 100)%10 + 1, 0.8)
    bing((digit // 10)%10 + 1, 0.4) 
    bing((digit % 10) + 1, 0.2)
    time.sleep(1.0)

def encodeIP(ipaddr):
    bing(3, 0.05)
    time.sleep(1.0)
    octets = ipaddr.split('.')
    for i, octet in enumerate(octets):
        time.sleep(1.0)
        #bing(i+1, 0.1)
        encode(int(octet))
        time.sleep(1.0)
    time.sleep(1.0)
