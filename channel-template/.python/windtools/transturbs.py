#!/usr/bin/python

import sys
import math
from turbineio import readTurbines


if len(sys.argv) < 6:
    print "usage: transturbs.py <wind dir> <ysize> <xoff> <infile> <outfile>"
    exit(1)
else:
    winddir=float(sys.argv[1])
    ysize=float(sys.argv[2])
    xoriginoff=float(sys.argv[3])
    inname=sys.argv[4]
    outname=sys.argv[5]


turbines=readTurbines(inname)    
if turbines is None:
    exit(1)


xsum=0.0
ysum=0.0
zsum=0.0


nturbs=0.0
for turb in turbines:
    if not (turb.type=="off"):

        xsum=xsum+turb.coords[0]
        ysum=ysum+turb.coords[1]
        zsum=zsum+turb.coords[2]

        nturbs=nturbs+1.0



if(nturbs<=0):
    print "error: can't find any turbines!"
    exit(1)


xav=xsum/nturbs
yav=ysum/nturbs
zav=zsum/nturbs

pi = math.pi

truewind = ((270 - 1.0*winddir)/360.0)*2.*pi

# calculate rotated turbines.

minx=10e10

newturbs=[]
for turb in turbines:

    xc = turb.coords[0]-xav
    yc = turb.coords[1]-yav

    ynewcent = ysize/2.0

    # Note -ve angle
    xcrot = (   xc * math.cos(truewind) + yc * math.sin(truewind) )
    ycnew = ( - xc * math.sin(truewind) + yc * math.cos(truewind) ) + ynewcent

    if(xcrot < minx):
        minx=xcrot

    # rotx, as we still have to calculate new x offset
    turb.rotx = xcrot
    turb.newy = ycnew
    turb.newz = turb.coords[2]


xtrans=(-minx)+xoriginoff

# calculate the right x displacement
for turb in turbines:
    turb.newx=turb.rotx+xtrans


# now rip through turbines file

infile = open( inname, "r" )
outfile = open( outname, "w" )
line = infile.readline().strip("\n")

verySmall=0.000000000001


# This is the 'turbine' label 
while(line):
    words = line.strip().split(" ")

    if words[0] == "coords":

        for turb in turbines:
            xdel=abs(turb.coords[0]-float(words[2]))
            ydel=abs(turb.coords[1]-float(words[3]))
            zdel=abs(turb.coords[2]-float(words[4]))
    
            if(xdel < verySmall and ydel < verySmall and zdel < verySmall):
                print >>outfile,"  coords = ", turb.newx, turb.newy, turb.newz
    else:

        print >>outfile, line
        
    # Read in first line of section
    line = infile.readline().strip("\n")

infile.close()
outfile.close()

print "*** rotated/transformed turbines written to:", outname
