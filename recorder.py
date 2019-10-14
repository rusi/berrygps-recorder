import led

import RPi.GPIO as GPIO
import time
import commands

import led

BCM_led = 18
BCM_btn = 22

led.BCM_led = BCM_led

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BCM_led, GPIO.OUT)
GPIO.setup(BCM_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

booting = True
recording = False

def displayIPaddress():
    global booting
    while booting:
        ipaddr = commands.getoutput('hostname -I')
        led.bing(3, 0.05)
        time.sleep(1.0)
        if (len(ipaddr) > 0):
            print(ipaddr)
            led.encodeIP(ipaddr)
    GPIO.output(BCM_led, GPIO.LOW)

def onBtnDown(channel):
    global booting
    global recording
    booting = False
    recording = True
    while recording:
        GPIO.output(BCM_led, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(BCM_led, GPIO.LOW)
        time.sleep(1.0)

def onBtnUp(channel):
    global recording
    recording = False

GPIO.add_event_detect(BCM_btn, GPIO.RISING, callback=onBtnDown)
GPIO.add_event_detect(BCM_btn, GPIO.RISING, callback=onBtnUp)

displayIPaddress()

while True:
    time.sleep(10)

GPIO.cleanup()
