#!/usr/bin/env python

from turbineio import readTurbines
import math

pi = math.pi

turbs=readTurbines("turbines.dat")

upwindDs = 2.0
downwindDs = 10.0

for turb in turbs:
    if(turb.id=="C08"):
        c08_x=turb.coords[0]
        c08_y=turb.coords[1]
        D = 2*turb.radius
        
    if(turb.id=="C01"):
        c01_x=turb.coords[0]
        c01_y=turb.coords[1]


xspan=c08_x - c01_x
yspan=c08_y - c01_y

theta=math.tan(yspan/xspan)

thetadeg=360*theta / (2*pi)

print "theta(deg):", thetadeg

c08_dx = -upwindDs * D * math.cos(theta)   
c08_dy = -upwindDs * D * math.sin(theta)   

c01_dx = downwindDs * D * math.cos(theta)   
c01_dy = downwindDs * D * math.sin(theta)   

startx=c08_x + c08_dx
starty=c08_y + c08_dy

endx=c01_x + c01_dx
endy=c01_y + c01_dy

print "C08-XXXX ", startx
print "C08-YYYY", starty

print "C01-XXXX ", endx
print "C01-YYYY", endy
