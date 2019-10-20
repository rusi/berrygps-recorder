# ref: http://ozzmaker.com/using-python-with-a-gps-receiver-on-a-raspberry-pi/
# ref: http://ozzmaker.com/how-to-save-gps-data-to-a-file-using-python/

from gps import *
import threading

gpsd = None

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd
        gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        self.running = True #setting the thread running to true

    def run(self):
        global gpsd
        while self.running:
            gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

def getGPSheader():
    return 'gpstime,lat,lon,alt,eps,epx,epv,ept,speed (m/s),climb,track,status,mode,sats,used'

def getGPSDateTime():
    global gpsd
    return gpsd.utc

def isGPSFix():
    return gpsd.fix.mode > 1 # MODE_NO_FIX

def getGPSrecord():
    global gpsd
    # report = gpsd.next()

    gpstime = gpsd.utc # + ' + ' + str(gpsd.fix.time)
    lat     = gpsd.fix.latitude
    lon     = gpsd.fix.longitude
    alt     = gpsd.fix.altitude # meter
    eps     = gpsd.fix.eps
    epx     = gpsd.fix.epx
    epv     = gpsd.fix.epv
    ept     = gpsd.fix.ept
    speed   = gpsd.fix.speed # m/s
    climb   = gpsd.fix.climb
    track   = gpsd.fix.track
    status  = gpsd.fix.status # STATUS_NO_FIX = 0, STATUS_FIX = 1, STATUS_DGPS_FIX = 2
    mode    = gpsd.fix.mode   # MODE_NO_FIX = 1, MODE_2D = 2, MODE_3D = 3
    sats    = len(gpsd.satellites)
    used    = gpsd.satellites_used

    # pprint.pprint(report)
    # if report['class'] == 'TPV':
    #     gpstime = str(getattr(report,'time',''))
    #     lat     = str(getattr(report,'lat',0.0))
    #     lon     = str(getattr(report,'lon',0.0))
    #     alt     = str(getattr(report,'alt','nan'))
    #     epv     = str(getattr(report,'epv','nan'))
    #     ept     = str(getattr(report,'ept','nan'))
    #     speed   = str(getattr(report,'speed','nan'))
    #     climb   = str(getattr(report,'climb','nan'))
    #     mode    = str(getattr(report,'mode','nan'))
    #     status  = str(getattr(report,'status','nan'))
    #     sats    = str(len(gpsd.satellites))

    return f"{gpstime},{lat},{lon},{alt},{eps},{epx},{epv},{ept},{speed},{climb},{track},{status},{mode},{sats},{used}"
    # return ",,,,,,,,,,,"

if __name__ == '__main__':
    import time
    import pprint
    import datetime

    print(getGPSheader())
    #f = open(time.strftime("%Y%m%d-%H%M%S")+'-data.csv','w')
    #f.write(gpsdata.getGPSheader() + "\n")
    #f.write(gpsdata.getGPSrecord() + "\n")

    # gpsd.stream(WATCH_ENABLE)
    gpsp = GpsPoller() # create the thread
    try:
        gpsp.start() # start up the GPS thread
        while True:
            time.sleep(1)
            data = getGPSrecord()
            data = str(datetime.datetime.now()) + "," + data
            print(data)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print("Done.\nExiting.")
        # f.close()
    finally:
        gpsp.running = False
        gpsp.join()
