import RPi.GPIO as GPIO
import time
import subprocess
import datetime
import pprint
import os

import led
import gpsdata
import gpstime
import imudata

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
        # get IP address; ref: https://circuitdigest.com/microcontroller-projects/display-ip-address-of-raspberry-pi
        rc, ipaddr = subprocess.getstatusoutput('hostname -I')
        # ipaddr = commands.getoutput('ifconfig wlan0 | grep "inet" | cut -d" " -f10')
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
    filename = "/home/pi/data/" + time.strftime("%Y%m%d-%H%M%S")+'-data.csv'
    print(filename)
    f = open(filename,'w')

    f.write("datetime," + gpsdata.getGPSheader() + "," + imudata.getIMUmeasureGheader() + "," + imudata.getIMUdataHeader() + "\n")

    btnled = led.FlashingLED(0.1, 0.9)
    btnled.start()

    imudata.resetIMUdata()
    while True:
        time.sleep(0.1)
        data = str(datetime.datetime.now()) + "," + gpsdata.getGPSrecord() + "," + imudata.getIMUmeasureG() + "," + imudata.getIMUdata()
        # print(data)
        f.write(data + "\n")
        if not GPIO.input(BCM_btn):
            break
    btnled.stop()

    f.flush()
    f.close()
    os.chmod(filename, 0o666)
    os.sync()
    recording = False
    print("recording...done")

def idle():
    GPIO.output(BCM_led, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(BCM_led, GPIO.LOW)
    time.sleep(4.0)

GPIO.add_event_detect(BCM_btn, GPIO.RISING, callback=onBtnPushed)

gpsp = gpsdata.GpsPoller() # create the thread

try:
    btnled = led.FlashingLED(0.5, 0.5)
    btnled.start()
    gpsp.start() # start up the GPS thread
    time.sleep(2)
    gpstime.setGPSTime()
    btnled.stop()

    displayIPaddress()

    while True:
        if recording:
            record()
        else:
            idle()

except (KeyboardInterrupt, SystemExit): # when you press ctrl+c
    print("Exiting...")

finally:
    gpsp.running = False
    GPIO.cleanup()
    gpsp.join()
