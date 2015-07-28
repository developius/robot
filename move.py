from sr.robot import *

import time

R = Robot()

#      Board   motor
#         |    |
#R.motors[0].m0.power

left = R.motors[0].m0
right = R.motors[0].m1

"""frontRight = R.motors[0].m0
frontLeft = R.motors[1].m0
backRight = R.motors[0].m1
backLeft = R.motors[1].m1"""

def drive(speed, seconds):
    """frontRight.power = speed
    frontLeft.power = speed
    backRight.power = speed
    backLeft.power = speed"""
    left.power = speed
    right.power = speed

    time.sleep(seconds)

    left.power = 0
    right.power = 0

    """frontRight.power = 0
    fronLeft.power = 0
    backRight.power = 0
    backLeft.power = 0"""

def turn(speed, seconds):
    """frontRight.power = -speed
    frontLeft.power = speed
    backRight.power = -speed
    backLeft.power = speed"""
    left.power = speed
    right.power = -speed

    time.sleep(seconds)

    left.power = 0
    right.power = 0
    """frontRight.power = 0
    fronLeft.power = 0
    backRight.power = 0
    backLeft.power = 0"""

while True:
    drive(100, 1)
    turn(50, 1)



