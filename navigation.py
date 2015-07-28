from sr.robot import *
from math import sqrt, sin, asin, radians, pi

import time

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

print arena_markers

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
    h = asin(dx * (sin(pi/2))/dist3)
    i = asin(dist1 * (sin(theta))/dist3)
    j = pi - h - i
    Rx = sin(j) * (dist1)/(sin(pi/2))
    k = asin(dy * (sin(pi/2))/dist3)
    l = asin(dist2 * (sin(theta))/dist3)
    m = pi - k - l
    Ry = sin(m) * (dist2)/(sin(pi/2))
    Rcoords = (Rx,Ry)
    return Rcoords

tokens = filter(arena_filter, R.see())
print coords(tokens[0],tokens[1])
