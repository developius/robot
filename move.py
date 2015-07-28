from sr.robot import *

import time

R = Robot()

#      Board   motor
#         |    |
#R.motors[0].m0.power

frontRight = R.motors[0].m0
frontLeft = R.motors[1].m0
backRight = R.motors[0].m1
backLeft = R.motors[1].m1

def drive(speed, seconds):
    frontRight.power = speed
    frontLeft.power = speed
    backRight.power = speed
    backLeft.power = speed

    time.sleep(seconds)

    frontRight.power = 0
    fronLeft.power = 0
    backRight.power = 0
    backLeft.power = 0

def turn(speed, seconds):
    frontRight.power = -speed
    frontLeft.power = speed
    backRight.power = -speed
    backLeft.power = speed

    time.sleep(seconds)

    frontRight.power = 0
    fronLeft.power = 0
    backRight.power = 0
    backLeft.power = 0

while True:
    drive(100, 1)
    turn(50, 1)



