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
    print("booting...")
    while booting:
        ipaddr = commands.getoutput('hostname -I')
        led.bing(3, 0.05)
        time.sleep(1.0)
        if (len(ipaddr) > 0):
            print(ipaddr)
            led.encodeIP(ipaddr)
    GPIO.output(BCM_led, GPIO.LOW)
    print("booting...DONE")

def onBtnPushed(channel):
    global booting
    global recording
    print("pushed")
    booting = False
    recording = True
    led.terminate = True

def record():
    global recording
    print("recording...")
    while GPIO.input(BCM_btn):
        GPIO.output(BCM_led, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(BCM_led, GPIO.LOW)
        time.sleep(1.0)
    recording = False
    print("recording...done")

def idle():
    GPIO.output(BCM_led, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(BCM_led, GPIO.LOW)
    time.sleep(4.0)

GPIO.add_event_detect(BCM_btn, GPIO.RISING, callback=onBtnPushed)

try:
    displayIPaddress()
    while True:
        if recording:
            record()
        else:
            idle()

finally:
    GPIO.cleanup()

