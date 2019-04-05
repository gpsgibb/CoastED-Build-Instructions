def convertToCarte(lon, lat):
    minlon=-6.239758
    minlat=55.688614
   
    sizelon=-5.895145-minlon
    sizelat=56.023011-minlat
    
    minx=0.0
    miny=0.0
    
    sizex=21453.7278466
    sizey=36651.1955983
    
    scalex=sizelon/sizex
    scaley=sizelat/sizey
   
    x = (lon-minlon)/scalex + minx
    y = (lat-minlat)/scaley + miny

    if(x<minx):
        x=minx
    elif(x>minx+sizex):
        x=minx+sizex
        
    # To account for small errors
    if(y<miny):
        y=miny
    elif(y>miny+sizey):
        y=miny+sizey
    
    return (x,y)

class BoundaryPoint():
    def __init__(self, lon, lat, \
                 m2amp, m2phase, s2amp, s2phase, n2amp, n2phase, k2amp, k2phase, \
                 k1amp, k1phase, o1amp, o1phase):
        
        (x, y) = convertToCarte(lon, lat)
        
        self.x = x
        self.y = y
        
        self.m2amp=m2amp
        self.m2phase=m2phase*2.0*pi/360.0
        
        self.s2amp=s2amp
        self.s2phase=s2phase*2.0*pi/360.0
        
        self.n2amp=n2amp
        self.n2phase=n2phase*2.0*pi/360.0
        
        self.k2amp=k2amp
        self.k2phase=k2phase*2.0*pi/360.0
        
        self.k1amp=k1amp
        self.k1phase=k1phase*2.0*pi/360.0
        
        self.o1amp=o1amp
        self.o1phase=o1phase*2.0*pi/360.0




def tidal_const_init():
    global northBoundaryPts, westBoundaryPts, southBoundaryPts, eastBoundaryPts
    global m2ang, s2ang, n2ang, k2ang, k1ang, o1ang

    print "*** Initialising tidal boundary points"

    northBoundaryPts=[]
    westBoundaryPts=[]
    southBoundaryPts=[]
    eastBoundaryPts=[]
          
    # Column names
    fp = open("tidalconst/islay_tidal_const.csv", "r")
    headerline = fp.readline()
    
    csvline = fp.readline()
    
    northlat=56.0230
    westlon=-6.2398
    southlat=55.6886
    eastlon=-5.8951
    
    while (csvline != ""):
        (lat, lon, m2amp, m2phase, s2amp, s2phase, n2amp, n2phase, \
         k2amp, k2phase, k1amp, k1phase, o1amp, o1phase, \
         p1amp, p1phase, q1amp, q1phase) = [float(x) for x in csvline.split(",")]

        # Binning points according to which boundary we are looking for

        foundIn=[]
        for tempBoundaryName in ["north", "west", "south", "east"]:
            if(tempBoundaryName =="north"):
                if (abs(lat-northlat) < 0.01):
                    foundIn.append(tempBoundaryName)
            
            elif(tempBoundaryName=="west"):
                if (abs(lon-westlon) < 0.01):
                    foundIn.append(tempBoundaryName)
                    
            elif(tempBoundaryName=="south"):
                if (abs(lat-southlat) < 0.01):
                    foundIn.append(tempBoundaryName)
                    
            elif(tempBoundaryName=="east"):
                if (abs(lon<eastlon) < 0.01):
                    foundIn.append(tempBoundaryName)
    
        if(len(foundIn)>0):
            pt=BoundaryPoint(lon, lat, m2amp, m2phase, s2amp, s2phase, \
                             n2amp, n2phase, k2amp, k2phase, \
                             k1amp, k1phase, o1amp, o1phase )

        for tempBoundaryName in foundIn:

            if(tempBoundaryName=="north"):
                northBoundaryPts.append(pt)

            elif(tempBoundaryName=="west"):
                westBoundaryPts.append(pt)

            elif(tempBoundaryName=="south"):
                southBoundaryPts.append(pt)
                
            elif(tempBoundaryName=="east"):
                eastBoundaryPts.append(pt)
                
        # Important to have this, otherwise - infinite loop
        csvline = fp.readline()
        # END OF LOOP

    fp.close()

    # boundaryPts=dampenCoastalAmps(boundaryPts)
       
    # Set these for later
    toangvel =  2.0*pi / (60*60)

    m2ang = toangvel  / 12.4206012 
    s2ang = toangvel  / 12.0
    n2ang = toangvel  / 12.65834751
    k2ang = toangvel  / 11.96723606
    k1ang = toangvel  / 23.93447213
    o1ang = toangvel  / 25.81933871

    tidal_init_flag=1


# set boundary and ramptime for this boundary
    
def init(boundary, ramptimehours=48.0, scale=1.0):
    global boundaryName, ramptime, boundaryPts
    global scaleperm

    scaleperm = scale
    boundaryName=boundary
    
    if(boundaryName=="north"):
        boundaryPts = northBoundaryPts

    elif(boundaryName=="west"):
        boundaryPts = westBoundaryPts

    elif(boundaryName=="south"):
        boundaryPts = southBoundaryPts

    elif(boundaryName=="east"):
        boundaryPts = eastBoundaryPts

    ramptime=ramptimehours*60.0*60.0


# Fluidity calls this for each point on the boundary

def val( (x,y,z), t ):
    
    p1=""
    p2=""

    lb=""
    # loop to catch pt between known points
    for b in boundaryPts:

        # This assumes more than 1 point to interpolate...
        if(lb != ""):
            if(boundaryName=="north"):
                if(x > lb.x and x<= b.x):
                    d1=x-lb.x
                    p1=lb
                    d2=b.x-x
                    p2=b
    
            if(boundaryName=="west"):
                if(y > lb.y and y<=b.y):
                    d1=y-lb.y
                    p1=lb
                    d2=b.y-y
                    p2=b
    
            if(boundaryName=="south"):
                if(x > lb.x and y<=b.y):
                    d1=x-lb.x
                    p1=lb
                    d2=b.x-x
                    p2=b
                    
            if(boundaryName=="east"):
                if(y > lb.y and y<=b.y):
                    d1=y-lb.y
                    p1=lb
                    d2=b.y-y
                    p2=b

        lb=b

        # END OF LOOP

    # if we found neighbouring points, interpolate
    if(p1 != "" and p2 != ""):
        totd=abs(d2+d1)
        w1=1.0-(d1/totd)
        w2=1.0-(d2/totd)
        
    else:
        # if we exceed the boundaries, do something sensible
        if( (boundaryName=="north" or boundaryName=="south")):
            if(x <= boundaryPts[0].x):
                p1=boundaryPts[0]
                p2=boundaryPts[1]
                w1=1.0
                w2=0.0
            elif(x > boundaryPts[-1].x):
                p1=boundaryPts[-1]
                p2=boundaryPts[-2]
                w1=1.0
                w2=0.0

        elif( (boundaryName=="east" or boundaryName=="west")):
            if(y <= boundaryPts[0].y):
                p1=boundaryPts[0]
                p2=boundaryPts[1]
                w1=1.0
                w2=0.0
            elif(y > boundaryPts[-1].y):
                p1=boundaryPts[-1]
                p2=boundaryPts[-2]
                w1=1.0
                w2=0.0
        else:
            # Can do nothing else: give up
            os.write(2, "*** tidalbcislay: Could not find points to interpolate between\n")
            exit(1)
            
    # now create interpolated values
    
    m2amp = w1* p1.m2amp + w2 * p2.m2amp
    s2amp = w1* p1.s2amp + w2 * p2.s2amp
    n2amp = w1* p1.n2amp + w2 * p2.n2amp
    k2amp = w1* p1.k2amp + w2 * p2.k2amp
    k1amp = w1* p1.k1amp + w2 * p2.k1amp
    o1amp = w1* p1.o1amp + w2 * p2.o1amp

    s2amp=0.
    n2amp=0.
    k2amp=0.
    k1amp=0.
    o1amp=0.

    m2phase = w1* p1.m2phase + w2 * p2.m2phase
    s2phase = w1* p1.s2phase + w2 * p2.s2phase
    n2phase = w1* p1.n2phase + w2 * p2.n2phase
    k2phase = w1* p1.k2phase + w2 * p2.k2phase
    k1phase = w1* p1.k1phase + w2 * p2.k1phase
    o1phase = w1* p1.o1phase + w2 * p2.o1phase
    
    # Finally, generate difference in hydrostatic pressure due to tidal forcing
    g=9.81
    density=1.027

    # Add all tidal constituent fluctuations
    f = m2amp*cos(m2ang*t-m2phase) \
        + s2amp*cos(s2ang*t-s2phase) \
        + n2amp*cos(n2ang*t-n2phase) \
        + k2amp*cos(k2ang*t-k2phase) \
        + k1amp*cos(k1ang*t-k1phase) \
        + o1amp*cos(o1ang*t-o1phase) 

    if( abs(ramptime) < 1e-10):
        scalef=0.0
    else:
        if(t < ramptime):
            scalef=scaleperm*(1.0-(ramptime-t)/ramptime)
        else:
            scalef=scaleperm

    return density*g*scalef*f

    
global tidal_module_init
try:
    tidal_module_init
except NameError:
    from math import cos, pi 
    import os
    
    tidal_const_init()
    
    tidal_module_init=1
