def init():
    global shallowz0, deepz0
    global shallowDepth, deepDepth
    global cD0

    global kappa

    # Now using standard FVCOM approach

    # Specify roughness lengths
    shallowz0=4e-3
    deepz0=8e-3

    cD0=0.0025
    
    shallowDepth=15.0
    deepDepth=30.0

    kappa=0.41

def val(pt, t):
    depth = abs(pt[2])
    if(depth<1):
        depth = 1.0

    if( depth < shallowDepth ):
        z0 = shallowz0

    elif( depth < deepDepth ):
        f = (depth-shallowDepth)/(deepDepth-shallowDepth)
        z0 = shallowz0*(1.0-f) + deepz0*f

    else:
        z0 = deepz0


    cD=max( kappa**2.0/math.log((depth/z0)**2.0), cD0)

    return cD


global impinit
try:
    raninit
except NameError:
    import math

    print "*** Initialising drag data"
    init()
    raninit=1

