import nc_depth_io as ncd
import math


def init(finebottom=0, layers=5):
    global minthick, maxlayers, cent, threshdist, defmaxlayers
    global scaledist
    
    global fineBottomFlag

    print "*** Initialising netcdf bathy data"

    fineBottomFlag = finebottom

    minthick=2.5
    defmaxlayers=layers
    scaledist = 5000.0

    cent=(8700, 17093.376121)
    threshdist=5000.0

    ncd.nc_init("gmsh/islay-jura-bathy.grd")

def val(pt, t):
    global raninit
    try:
        raninit
    except NameError:
        init(finebottom=1, layers=10)
        raninit=1

    depth = ncd.calculateDepth( pt )
    cdist = math.sqrt( (cent[0]-pt[0])**2.0 + (cent[1]-pt[1])**2.0 )

    if(cdist < threshdist):
        maxlayers = defmaxlayers

    elif(cdist < threshdist+scaledist):
        f = (cdist-threshdist) / scaledist
        maxlayers = int((1.0-f) * defmaxlayers + f * 1.0)

    else:
        maxlayers = 1

    if(maxlayers<1):
        maxlayers=1

    # A crafty bit. This means the divisions just miss the bottom, leaving
    # room for finer resolution near the seabed.

    if(cdist < threshdist  and defmaxlayers > 1 and fineBottomFlag==1):
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
