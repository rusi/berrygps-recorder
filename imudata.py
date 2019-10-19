import IMU
import math
import datetime

# If the IMU is upside down (Skull logo facing up), change this value to 1
IMU_UPSIDE_DOWN = 0

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading value.
magXmin =  842
magYmin =  -374
magZmin =  -2314
magXmax =  895
magYmax =  -325
magZmax =  -2237

#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0


def kalmanFilterY(accAngle, gyroRate, DT):
    global KFangleY
    global Q_angle
    global Q_gyro
    global y_bias
    global YP_00
    global YP_01
    global YP_10
    global YP_11
    y=0.0
    S=0.0

    KFangleY = KFangleY + DT * (gyroRate - y_bias)

    YP_00 = YP_00 + ( - DT * (YP_10 + YP_01) + Q_angle * DT )
    YP_01 = YP_01 + ( - DT * YP_11 )
    YP_10 = YP_10 + ( - DT * YP_11 )
    YP_11 = YP_11 + ( + Q_gyro * DT )

    y = accAngle - KFangleY
    S = YP_00 + R_angle
    K_0 = YP_00 / S
    K_1 = YP_10 / S

    KFangleY = KFangleY + ( K_0 * y )
    y_bias = y_bias + ( K_1 * y )

    YP_00 = YP_00 - ( K_0 * YP_00 )
    YP_01 = YP_01 - ( K_0 * YP_01 )
    YP_10 = YP_10 - ( K_1 * YP_00 )
    YP_11 = YP_11 - ( K_1 * YP_01 )

    return KFangleY

def kalmanFilterX(accAngle, gyroRate, DT):
    global KFangleX
    global Q_angle
    global Q_gyro
    global x_bias
    global XP_00
    global XP_01
    global XP_10
    global XP_11
    x=0.0
    S=0.0

    KFangleX = KFangleX + DT * (gyroRate - x_bias)

    XP_00 = XP_00 + ( - DT * (XP_10 + XP_01) + Q_angle * DT )
    XP_01 = XP_01 + ( - DT * XP_11 )
    XP_10 = XP_10 + ( - DT * XP_11 )
    XP_11 = XP_11 + ( + Q_gyro * DT )

    x = accAngle - KFangleX
    S = XP_00 + R_angle
    K_0 = XP_00 / S
    K_1 = XP_10 / S

    KFangleX = KFangleX + ( K_0 * x )
    x_bias = x_bias + ( K_1 * x )

    XP_00 = XP_00 - ( K_0 * XP_00 )
    XP_01 = XP_01 - ( K_0 * XP_01 )
    XP_10 = XP_10 - ( K_1 * XP_00 )
    XP_11 = XP_11 - ( K_1 * XP_01 )

    return KFangleX

###############################

IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
kalmanX = 0.0
kalmanY = 0.0

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

def getIMUdataHeader():
    return "ACCx,ACCy,ACCz,GYRx,GYRy,GYRz,MAGx,MAGy,MAGz,AccXangle,AccYangle,gyroXangle,gyroYangle,gyroZangle,CFangleX,CFangleY,heading,tiltCompensatedHeading,kalmanX,kalmanY"

a = datetime.datetime.now()
def getIMUdata():
    global a
    global gyroXangle
    global gyroYangle
    global gyroZangle
    global CFangleX
    global CFangleY
    global kalmanX
    global kalmanY
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()

    #Normalize accelerometer raw values.
    if not IMU_UPSIDE_DOWN:
        #Use these two lines when the IMU is up the right way. Skull logo is facing down
        accXnorm = ACCx / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        accYnorm = ACCy / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    else:
        #Us these four lines when the IMU is upside down. Skull logo is facing up
        accXnorm = -ACCx / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
        accYnorm =  ACCy / math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    ##### COMPASS #####################################
    #Apply compass calibration
    MAGx -= (magXmin + magXmax) /2
    MAGy -= (magYmin + magYmax) /2
    MAGz -= (magZmin + magZmax) /2

    if IMU_UPSIDE_DOWN:
        MAGy = -MAGy # If IMU is upside down, this is needed to get correct heading.
    #Calculate heading
    heading = 180 * math.atan2(MAGy,MAGx)/M_PI
    #Only have our heading between 0 and 360
    if heading < 0:
        heading += 360

    ##### GYRO ########################################
    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)

    #Convert Gyro raw to degrees per second
    rate_gyr_x = GYRx * G_GAIN
    rate_gyr_y = GYRy * G_GAIN
    rate_gyr_z = GYRz * G_GAIN

    #Calculate the angles from the gyro.
    gyroXangle += rate_gyr_x * LP
    gyroYangle += rate_gyr_y * LP
    gyroZangle += rate_gyr_z * LP

    ##### ACCEL ########################################
    #Convert Accelerometer values to degrees
    if not IMU_UPSIDE_DOWN:
        # If the IMU is up the correct way (Skull logo facing down), use these calculations
        AccXangle = (math.atan2(ACCy,ACCz) * RAD_TO_DEG)
        AccYangle = (math.atan2(ACCz,ACCx) + M_PI) * RAD_TO_DEG
    else:
        #Us these four lines when the IMU is upside down. Skull logo is facing up
        AccXangle = (math.atan2(-ACCy, -ACCz) * RAD_TO_DEG)
        AccYangle = (math.atan2(-ACCz, -ACCx) + M_PI) * RAD_TO_DEG
    #Change the rotation value of the accelerometer to -/+ 180 and
    #move the Y axis '0' point to up.  This makes it easier to read.
    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0

    ##### FILTERS ########################################
    #Complementary filter used to combine the accelerometer and gyro values.
    CFangleX = AA * (CFangleX + rate_gyr_x * LP) + (1 - AA) * AccXangle
    CFangleY = AA * (CFangleY + rate_gyr_y * LP) + (1 - AA) * AccYangle

    #Kalman filter used to combine the accelerometer and gyro values.
    kalmanY = kalmanFilterY(AccYangle, rate_gyr_y, LP)
    kalmanX = kalmanFilterX(AccXangle, rate_gyr_x, LP)

    ####################################################################
    ###################Tilt compensated heading#########################
    ####################################################################
    #Calculate pitch and roll
    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm / math.cos(pitch))

    #Calculate the new tilt compensated values
    magXcomp = MAGx * math.cos(pitch) + MAGz * math.sin(pitch)

    #The compass and accelerometer are orientated differently on the LSM9DS0 and LSM9DS1 and the Z axis on the compass
    #is also reversed. This needs to be taken into consideration when performing the calculations
    if(IMU.LSM9DS0):
        magYcomp = MAGx * math.sin(roll) * math.sin(pitch) + MAGy * math.cos(roll) - MAGz * math.sin(roll) * math.cos(pitch)   #LSM9DS0
    else:
        magYcomp = MAGx * math.sin(roll) * math.sin(pitch) + MAGy * math.cos(roll) + MAGz * math.sin(roll) * math.cos(pitch)   #LSM9DS1

	#Calculate tilt compensated heading
    tiltCompensatedHeading = 180 * math.atan2(magYcomp, magXcomp) / M_PI
    if tiltCompensatedHeading < 0:
        tiltCompensatedHeading += 360

    return f"{ACCx},{ACCy},{ACCz},{GYRx},{GYRy},{GYRz},{MAGx},{MAGy},{MAGz},{AccXangle},{AccYangle},{gyroXangle},{gyroYangle},{gyroZangle},{CFangleX},{CFangleY},{heading},{tiltCompensatedHeading},{kalmanX},{kalmanY}"

if __name__ == '__main__':
    import time
    import pprint

    print(getIMUdataHeader())
    try:
        while True:
            data = getIMUdata()
            data = str(datetime.datetime.now()) + "," + data
            print(data)
            time.sleep(0.1)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        print("Done.\nExiting.")
