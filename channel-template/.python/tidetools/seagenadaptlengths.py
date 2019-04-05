# Currently only works for BEM turbines in new format

from turbineio import readTurbines

def init(argmindx, argmaxdx, \
             argmindy, argmaxdy, \
             argmindz, argmaxdz, \
             beamwidth, \
             outtype="matrix", \
             bottomdx=0.0, bottomdy=0.0, bottomdz=0.0, bottomheight=0.0, \
             shape="seagen" ):

    global mindx, mindy, mindz, maxdx, maxdy, maxdz
    global botdx, botdy, botdz, both
    
    global cb_width, outputType, shapeType

    mindx = float(argmindx)
    mindy = float(argmindy)
    mindz = float(argmindz)

    maxdx = float(argmaxdx)
    maxdy = float(argmaxdy)
    maxdz = float(argmaxdz)

    cb_width = float(beamwidth)
    outputType = outtype
    
    botdx  = float(bottomdx)
    botdy = float(bottomdy)
    botdz = float(bottomdz)
    both = float(bottomheight)
    
    shapeType=shape

    turbInit()
    
   
#----------------------------


def turbInit(scale=1.0,
              noturbminscale=1.0,
              upwindscale=0.1,
              downwindscale=1.0,
              crosswindscale=0.25):


    global turbines, defaultOutputValue
    global turbmindx, turbmindy, turbmindz, turbmaxdx, turbmaxdy, turbmaxdz
    global globalScale, overrideOffSwitch
    global upwindScaleValue, downwindScaleValue, crosswindScaleValue

    if(abs(float(noturbminscale)) > 1):
        overrideOffSwitch=1
    else:
        overrideOffSwitch=0        

    # If the scale is so small, we're not dealing with element dimensions
    # - will fix this properly later'
    if(mindx < 0.25):
        turbmindx = mindx
        turbmindy = mindy 
        turbmindz = mindz
    else:
        turbmindx = 0.33333333333333333
        turbmindy = 0.33333333333333333 
        turbmindz = 0.33333333333333333


    turbmaxdx = maxdx
    turbmaxdy = maxdy
    turbmaxdz = maxdz

    defaultOutputValue = outputType 
    globalScale=scale


    # This will scale the distance it takes to achieve  max value
    upwindScaleValue = upwindscale
    downwindScaleValue = downwindscale
    crosswindScaleValue = crosswindscale
    
    
    turbines = readTurbines("turbines.dat")
    

def structVal( X, t):

    import math

    # check for distance on leading edge / above or below crossbeam
    cx=250.0
    cy=100.0
    cz=16.0

    x = X[0]-cx
    # No difference between left or right beam
    y =abs( X[1]-cy)
    z = X[2]-cz

    # This decides at what distance to start scaling mesh up from min
    fracthresh = 0.25

    cbdia = 4.0
    twdia = 3.0

    # cb_updist = 5 * cbdia
    # cb_vertdist = 5 * cbdia
    # cb_downdist = 40 * cbdia

    # tw_updist = 5*twdia
    # tw_vertdist = 5*twdia
    # tw_downdist = 50*twdia


    # cb_updist = 5.0 * cbdia
    cb_updist = 2.5 * cbdia
    cb_vertdist = 5.0 * cbdia
    cb_downdist = 175.0

    # tw_updist = 5.0 * twdia
    tw_updist = 2.5 * twdia
    tw_vertdist = 5.0 * twdia
    tw_downdist = 225.0

    # flag. Tests whether inside or outside minimum values

    maxfrac = 1.0

    # crossbeam. Check if upstream or downstream
    if (x<0) :
        if(y < cb_width/2):
            if(shapeType=="seagen"):
                ineq1 = ((x/cb_updist)**2.0 + (z/cb_vertdist)**2.0)**0.5
            else:
                ineq1=1.0
                
            ineq2 = ((x/tw_updist)**2.0 + (y/tw_updist)**2.0)**0.5

            if(ineq1 <= 1 or ineq2 <= 1):
                if(ineq1 < ineq2):
                    maxfrac = ineq1
                else:
                    maxfrac = ineq2

        else:
            if(shapeType=="seagen"):
                ineq1 = ((x/cb_updist)**2.0 +((y-cb_width/2)/cb_updist)**2.0 +(z/cb_vertdist)**2.0)**0.5

                if(ineq1 <= 1):
                    maxfrac = ineq1
    else:
        if(y < cb_width/2):
            if(shapeType=="seagen"):
                ineq1 = ((x/cb_downdist)**2.0 + (z/cb_vertdist)**2.0)**0.5
            else:
                ineq1=1.0
                
            ineq2 = ((x/tw_downdist)**2.0 + (y/tw_updist)**2.0)**0.5

            if(ineq1 <= 1 or ineq2 <= 1):
                if(ineq1 < ineq2):
                    maxfrac = ineq1
                else:
                    maxfrac = ineq2

        else:
            if(shapeType=="seagen"):
                ineq1 = ((x/cb_downdist)**2.0+((y-cb_width/2)/cb_updist)**2.0 +(z/cb_vertdist)**2.0)**0.5

                if(ineq1 <= 1):
                    maxfrac = ineq1

        
    # This warps the scaling to start from a minimum distance
    # Commented out, it scales out from line sources
        
    d = maxfrac
    if(d<fracthresh):
        maxfrac = 0.0
    else:
        maxfrac = (1.0/(1-fracthresh))*(d-fracthresh)

    minfrac = 1.0 - maxfrac

#    if minfrac > 10e-5:
#        minfrac=1.0
#        maxfrac=0.0

    sizex = minfrac*mindx + maxfrac*maxdx
    sizey = minfrac*mindy + maxfrac*maxdy
    sizez = minfrac*mindz + maxfrac*maxdz

    # scale from sizex/y/z --> botdx/dy/dz
    if(abs(both) > 10e-10 and X[2] < both):
        sizex = (sizex-botdx)/both + botdx 
        sizey = (sizey-botdy)/both + botdy 
        sizez= (sizez-botdz)/both + botdz


    minLengths = [ sizex, sizey, sizez ]

    return minLengths

# -------------------

def turbVal( (x,y,z), t ):
    import math

    dx=dy=dz=0

    # As we may now be dealing with multiple turbines, we have to deal with the
    # interpolation function values from all of them. By default, we opt for 
    # the most conservative (lowest) values - ie. highest mesh resolutions.

    con_dx=turbmaxdx
    con_dy=turbmaxdy
    con_dz=turbmaxdz

    # If we have no turbines, just return maximum values of range
    if(turbines is None):
        minMaxLengths=[ turbmaxdx,turbmaxdy, turbmaxdz ]
                
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

            relz = relz / crosswindScaleValue

            rp = math.sqrt( relx**2 + rely**2 + relz**2 )

            saferad = 5.*turb.radius*globalScale
            scaledist = 10.*turb.radius*globalScale
            
            rpextent = rp-saferad

            if ( rp < saferad ):
                fac = 0
            elif( rpextent < scaledist ):
                fac = rpextent / scaledist
            else:
                fac = 1

            dx = (1-fac) *turbmindx + fac *turbmaxdx
            dy = (1-fac) *turbmindy + fac *turbmaxdy
            dz = (1-fac) *turbmindz + fac *turbmaxdz


            if abs(con_dx) > abs(dx):
                con_dx=dx

            if abs(con_dy) > abs(dy):
                con_dy=dy

            if abs(con_dz) > abs(dz):
                con_dz=dz

    minMaxLengths=[ con_dx, con_dy, con_dz ]

    return minMaxLengths


    # -------------------

def val( X, t ):
    # get corresponding lengths from struct and turbine mesh lengths
    tlens = turbVal(X, t)

    if(shapeType=="none"):
        stlens=tlens
    else:
        stlens = structVal(X, t)


    if(stlens[0]<tlens[0]):
        retx=stlens[0]	
    else:
        retx=tlens[0]	
                
    if(stlens[1]<tlens[1]):
        rety=stlens[1]
    else:
        rety=tlens[1]

    if(stlens[2]<tlens[2]):
        retz=stlens[2]
    else:
        retz=tlens[2]	

    if(outputType=="matrix"):
        return [ [retx, 0, 0], \
                     [0, rety, 0], \
                     [0, 0, retz] ]
        
    else:
        return [ retx, rety, retz ]
	

