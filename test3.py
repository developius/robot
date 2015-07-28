from sr.robot import *
from math import sqrt, sin, asin, radians, pi

import time

SEARCHING, DRIVING = range(2)

R = Robot()

token_filter = lambda m: m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER)
arena_filter = lambda m: m.info.marker_type in (MARKER_ARENA)

arena_markers = {}
for i in range(7):
    arena_markers[i] = ((i+1), 0)
for i in range(7,14):
    arena_markers[i] = (0,(i-6))
for i in range(14,21):
    arena_markers[i] = ((i-13),0)
for i in range(21,28):
    arena_markers[i] = (0,(i-20))

print(arena_markers)

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def coords(m1,m2): #offset1,offset2,dist1,dist2,rot1,rot2):
    x1 = arena_markers[m1.info.offset][0]
    y1 = arena_markers[m1.info.offset][1]
    x2 = arena_markers[m2.info.offset][0]
    y2 = arena_markers[m2.info.offset][1]
    print "m1 = ", m1.info.offset
    print "am1 = ", arena_markers[m1.info.offset]
    print "am1 = ", arena_markers[m1.info.offset]
    print "m2 = ", m2.info.offset
    print "am2 = ", arena_markers[m2.info.offset]
    print "am2 = ", arena_markers[m2.info.offset]
    dx = abs(x1 - x2)
    print x1
    print x2
    print dx
    dy = abs(y1 - y2)
    print y1
    print y2
    print dy
    dist1 = m1.dist
    dist2 = m2.dist
    dist3 = sqrt((dx^2)+(dy^2))
    theta = radians(abs(m1.rot_y - m2.rot_y))
    #if dx == 0:
    #    h = 0
    #else:
    h = asin(dx/dist3)
    i = asin(dist1 * (sin(theta))/dist3)
    print i
    j = pi - h - i
    print j
    Rx = sin(j)/dist1
    print Rx
    #if dy == 0:
    #    k = 0
    #else:
    k = asin(dy/dist3)
    l = asin(dist2 * (sin(theta))/dist3)
    print l
    m = pi - k - l
    print m
    Ry = sin(m)/dist2
    print Ry
    return (Rx,Ry)

state = SEARCHING

while True:
    if state == SEARCHING:
        print "Searching..."
        tokens = filter(arena_filter, R.see())
        if len(tokens) > 1:
            print coords(tokens[0],tokens[1])
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
        tokens = filter(arena_filter, R.see())
        if len(tokens) < 2:
            state = SEARCHING

        else:
            print coords(tokens[0],tokens[1])
            m = tokens[0]
            if m.dist < 0.4:
                print "Found it!"
                state = SEARCHING

            elif -15 <= m.rot_y <= 15:
                print "Ah, that'll do."
                drive(50, 0.5)

            elif m.rot_y < -15:
                print "Left a bit..."
                turn(-12.5, 0.5)

            elif m.rot_y > 15:
                print "Right a bit..."
                turn (12.5, 0.5)
