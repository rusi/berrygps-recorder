import time
import datetime
import subprocess

import gpsdata

#assuming GPSPoller has been started

def setGPSTime():
    gpsdatetime = None
    while (not gpsdata.isGPSFix()) or (gpsdatetime is None):
        gpsdatetime = gpsdata.getGPSDateTime()
        time.sleep(1)
    gpsdatetime = str(gpsdata.getGPSDateTime())
    subprocess.call(["/bin/date", "-s", gpsdatetime])

if __name__ == '__main__':
    try:
        gpsp = gpsdata.GpsPoller() # create the thread
        gpsp.start() # start up the GPS thread

        time.sleep(2)

        setGPSTime()

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
