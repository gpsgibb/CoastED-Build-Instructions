# Currently only works for BEM turbines in new format

from turbineio import readTurbines

def init( arg_mindx, arg_maxdx, \
              arg_mindy, arg_maxdy, \
              arg_mindz, arg_maxdz, \
              outputValue="matrix",
              scale=1,
              noturbminscale=1,
              upwindscale=1,
              downwindscale=1,
              crosswindscale=1):


    global turbines, defaultOutputValue
    global mindx, mindy, mindz, maxdx, maxdy, maxdz
    global globalScale, overrideOffSwitch
    global upwindScaleValue, downwindScaleValue, crosswindScaleValue

    if(abs(float(noturbminscale)) > 1):
        overrideOffSwitch=1
    else:
        overrideOffSwitch=0        


    mindx = float(arg_mindx) * float(noturbminscale)
    mindy = float(arg_mindy) * float(noturbminscale)
    mindz = float(arg_mindz) * float(noturbminscale)

    maxdx = float(arg_maxdx)
    maxdy = float(arg_maxdy)
    maxdz = float(arg_maxdz)

    defaultOutputValue = outputValue 
    globalScale=scale

    # This will scale the distance it takes to achieve  max value
    upwindScaleValue = upwindscale
    downwindScaleValue = downwindscale
    crosswindScaleValue = crosswindscale
    
    
    turbines = readTurbines("turbines.dat")
# -------------------

def val( (x,y,z), t ):
    import math

    dx=dy=dz=0

    # As we may now be dealing with multiple turbines, we have to deal with the
    # interpolation function values from all of them. By default, we opt for 
    # the most conservative (lowest) values - ie. highest mesh resolutions.

    con_dx=maxdx
    con_dy=maxdy
    con_dz=maxdz

    # If we have no turbines, just return maximum values of range
    if(turbines is None):
        if(defaultOutputValue=="matrix"):
            minMaxLengths=[ [maxdx, 0, 0,], \
                           [0, maxdy, 0], \
                           [0, 0, maxdz] ]
        elif(defaultOutputValue=="vector"):
            minMaxLengths=[ maxdx,maxdy, maxdz ]
                
        return minMaxLengths


    # If we do, loop through them
    for turb in turbines:

        if (not (turb.type=="off")) or overrideOffSwitch==1:
 
            relx = x - turb.coords[0]
            rely = y - turb.coords[1]
            relz = z - turb.coords[2]

            if(upwindScaleValue != 1 and relx<0):
                relx = relx / upwindScaleValue  
                
            if(downwindScaleValue != 1 and relx>0):
                relx = relx / downScaleValue

            rely = rely / crosswindScaleValue

            rp = math.sqrt( relx**2 + rely**2 + relz**2 )

            saferad = 5.*turb.radius*globalScale
            scaledist = 20.*turb.radius*globalScale
            
            rpextent = rp-saferad

            if ( rp < saferad ):
                fac = 0
            elif( rpextent < scaledist ):
                fac = rpextent / scaledist
            else:
                fac = 1

            dx = (1-fac) *mindx + fac *maxdx
            dy = (1-fac) *mindy + fac *maxdy
            dz = (1-fac) *mindz + fac *maxdz


            if abs(con_dx) > abs(dx):
                con_dx=dx

            if abs(con_dy) > abs(dy):
                con_dy=dy

            if abs(con_dz) > abs(dz):
                con_dz=dz

    if(defaultOutputValue=="matrix"):
        minMaxLengths=[ [con_dx, 0, 0,], \
                       [0, con_dy, 0], \
                       [0, 0, con_dz] ]
    elif(defaultOutputValue=="vector"):
        minMaxLengths=[ con_dx, con_dy, con_dz ]

    return minMaxLengths
