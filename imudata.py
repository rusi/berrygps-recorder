import IMU

IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

def getIMUmeasureGheader():
    return "Gx,Gy,Gz"

def getIMUmeasureG():
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()

    Gx = (ACCx * 0.244) / 1000
    Gy = (ACCy * 0.244) / 1000
    Gz = (ACCz * 0.244) / 1000

    return f"{Gx},{Gy},{Gz}"

