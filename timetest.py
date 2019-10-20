import time
import datetime
import subprocess

import gpsdata

filename = "/home/pi/timetest.txt"
f = open(filename,'w')
try:
    gpsp = gpsdata.GpsPoller() # create the thread
    gpsp.start() # start up the GPS thread

    time.sleep(2)

    t1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")
    t2 = str(datetime.datetime.now())
    print(f"{t1} <=> {t2}")
    print(gpsdata.getGPSrecord())
    f.write(f"{t1} <=> {t2} <=>" + gpsdata.getGPSrecord() + "\n")
    gpsdatetime = None
    while (not gpsdata.isGPSFix()) or (gpsdatetime is None):
        gpsdatetime = str(gpsdata.getGPSDateTime())
        print(gpsdata.getGPSrecord())
        f.write(gpsdata.getGPSrecord() + "\n")
        time.sleep(1)
    print("===")
    f.write("\n===\n")

    gpsdatetime = str(gpsdata.getGPSDateTime())
    print(gpsdatetime)
    f.write(gpsdata.getGPSrecord())
    subprocess.call(["/bin/date", "-s", gpsdatetime])
    print("==Time SET==")
    f.write("\n==Time SET==\n")
    while True:
        t1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        t2 = str(datetime.datetime.now())
        print(f"{t1} <=> {t2}")
        f.write(f"{t1} <=> {t2} <=> " + gpsdata.getGPSrecord() + "\n")
        time.sleep(1)
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    pass
finally:
    f.close()
    gpsp.running = False
    gpsp.join()
