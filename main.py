from sr.robot import *

import time, math

SEARCHING, DRIVING = range(2)

R = Robot()

token_filter = lambda m: m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER)

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turnDegrees(degrees):
    markers = R.see()
    lowestDifferenceYet = 1000 #Arbitrary

    if degrees >= 0:
        for marker in markers:
            if marker.info.marker_type == MARKER_ARENA:
                difference = abs(degrees - marker.rot_y)
                if difference < lowestDifferenceYet:
                    lowestDifferenceYet = difference #Pull out the best marker for turning
                    bestMarkerOffset = marker.offset

        initialRotation = bestMarker.rot_y
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        turn(100, (degrees/50)) #NEEDS CALIBRATION

    if degrees < 0:
        for marker in markers:
            if marker.info.marker_type == MARKER_ARENA:
                difference = abs(degrees + marker.rot_y)
                if difference < lowestDifferenceYet:
                    lowestDifferenceYet = difference #Pull out the best marker for turning
                    bestMarkerOffset = marker.offset

        initialRotation = bestMarker.rot_y
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        turn(-100, (degrees/50)) #NEEDS CALIBRATION

    markers = R.see()#Scan to make finer adjustment
    for marker in markers:
        if marker.info.marker_type == MARKER_ARENA and marker.offset == bestMarkerOffset:
            bestMarker = marker

    if degrees >= 0:
        newDifference = initialRotation - bestMarker.rot_y #How far we are off the specified degrees
        if newDifference > 10: #We didn't turn far enough
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            turn(100, (degrees/50)) #NEEDS CALIBRATION

        elif newDifference < -10: #We turned too far
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            turn(-100, (degrees/50)) #NEEDS CALIBRATION

    if degrees < 0: #Polarity needs fixing here
        newDifference = initialRotation + bestMarker.rot_y #How far we are off the specified degrees
        if (degrees + newDifference) > 10: #We turned too far
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            turn(100, (degrees/50)) #NEEDS CALIBRATION

        elif (degrees + newDifference) < -10: #We didn't turn far enough
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            turn(-100, (degrees/50)) #NEEDS CALIBRATION


def drive(speed, seconds):
    startTime = time.time()
    R.motors[0].m0.power = speed #Start motors
    R.motors[0].m1.power = speed

    while (time.time() - startTime) < seconds:
        markers = R.see()
        print "I can see", len(markers), "markers."

        for marker in markers:
            if marker.info.marker_type == MARKER_ROBOT and marker.dist < 2: #If it's a robot
                distanceToSide = math.sin(marker.rot_y) * marker.dist # calculate how far to the side of our robot the other is
                print "Distance to Side: " + str(distanceToSide)

                if -30 <= distanceToSide <= 30:
                    #Avoid robot
                    if distanceToSide <= 0: #If marker is to the Left
                        print "marker is to the Left"
                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        turn(100, 0.25)#NEEDS CALIBRATION

                        distanceToSide = -distanceToSide #Convert negative value to positive value

                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        timeToMove = (30 - distanceToSide)#NEEDS CALIBRATION
                        R.motors[0].m0.power = 100
                        R.motors[0].m1.power = 100
                        time.sleep(0.3) #timeToMove)

                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        #NEEDS CALIBRATION
                        turn(-100, 0.25) #Turn back to the orignal direction

                    else: #If marker is to the Right
                        print "marker is to the Right"
                        turn(-100, 0.25)#NEEDS CALIBRATION

                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        timeToMove = (30 - distanceToSide)#NEEDS CALIBRATION
                        R.motors[0].m0.power = 100
                        R.motors[0].m1.power = 100
                        time.sleep(0.3) #timeToMove)

                        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        #NEEDS CALIBRATION
                        turn(100, 0.25) #Turn back to the orignal direction
                else:
                    time.sleep(2)

    R.motors[0].m0.power = 0 #Stop motors
    R.motors[0].m1.power = 0

def tokenScan():
    tokens = filter(token_filter, R.see())
    """
    lowestDistanceYet = 1000 #Arbitrary
    if len(tokens) > 0:
        orderedTokenList = {}
        for token in tokens:
            if token.dist < lowestDistanceYet:
                    lowestDistanceYet.extend(token.dist) #Pull out the best marker for turning
            orderedTokenList =
            orderedTokenList[token.dist] = token

        sorted(orderedTokenList, key=lambda token: (orderedTokenList[i]))
        print "OrderedTokenList: ", orderedTokenList
    else: #Can't find any tokens
        return False
    """
    tokens_sorted = sorted(tokens, key = lambda token: token.dist)
    print tokens_sorted

state = SEARCHING

while True:
    if state == SEARCHING:
        tokenScan()
        print "Searching..."
        tokens = filter(token_filter, R.see())
        if len(tokens) > 0:
            m = tokens[0]
            print "Token sighted. {0} is {1}m away, bearing {2} degrees." \
                  .format(m.info.offset, m.dist, m.rot_y)
            state = DRIVING

        else:
            print "Can't see anything."
            turn(25, 0.3)
            time.sleep(0.2)

    elif state == DRIVING:
        print "Aligning..."
        tokens = filter(token_filter, R.see())
        if len(tokens) == 0:
            state = SEARCHING

        else:
            m = tokens[0]
            print "Marker M: ", m

            if m.dist < 0.4: #If it's close enough to grab
                print "Marker within grabbing range"
                if R.grab():
                    print "Grab Succesful"

                    turn(50, 0.5)#Drive home
                    drive(50, 1)
                    R.release()
                    drive(-50, 0.5)
                else:
                    print "Grab failed"
                exit()

            elif -15 <= m.rot_y <= 15:
                print "Marker within acceptable angle"
                drive(50, 0.5)

            elif m.rot_y < -15:
                print "Left a bit..."
                turn(-12.5, 0.5)

            elif m.rot_y > 15:
                print "Right a bit..."
                turn (12.5, 0.5)
