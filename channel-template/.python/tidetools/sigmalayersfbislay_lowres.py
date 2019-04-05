import nc_depth_io as ncd
import math


def init():
    global minthick, maxlayers, cent, threshdist, defmaxlayers
    
    global fineBottomFlag
    fineBottomFlag = 1

    minthick=5
    defmaxlayers=2

    cent=(8700, 17093.376121)
    threshdist=6000

    ncd.nc_init("gmsh/islay-jura-bathy.grd")

def val(pt, t):
    global raninit
    try:
        raninit
    except NameError:
        init()
        print "*** Initialising netcdf bathy data"
        raninit=1

    depth = ncd.calculateDepth( pt )
    cdist = math.sqrt( (cent[0]-pt[0])**2.0 + (cent[1]-pt[1])**2.0 )

    if(cdist < threshdist):
        maxlayers = defmaxlayers

    elif(cdist < threshdist+1000):
        if (defmaxlayers>4):
            maxlayers = 4
        else:
            maxlayers = defmaxlayers-1
            
    elif(cdist < threshdist+2000):
        if (defmaxlayers>3):
            maxlayers = 3
        else:
            maxlayers = defmaxlayers-1

    elif(cdist < threshdist+3000):
        if (defmaxlayers>2):
            maxlayers = 2
        else:
            maxlayers=1
    else:
        maxlayers = 1

    if(maxlayers<1):
        maxlayers=1

    # A crafty bit. This means the divisions just miss the bottom, leaving
    # room for finer resolution near the seabed.

    if(cdist < threshdist  and defmaxlayers > 1):
        abvdepth = 0.9 * depth
    else:
        abvdepth = depth

    nlayers=int(math.floor(depth/minthick))
    if(nlayers > maxlayers):
        nlayers=int(maxlayers)
    elif(nlayers < 1):
        nlayers=1

    dz = 0.5 * abvdepth / nlayers

    if (dz < 0.5*minthick):
        dz = 1.1* 0.5*minthick

    return dz
