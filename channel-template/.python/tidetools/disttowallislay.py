def val(pt, t):

    # Very crude wall estimate. Examines distance to bottom only
    bottomdepth = ncd.calculateDepth( pt )
    absdist = abs(bottomdepth + pt[2])

    distToWall= u_tau*absdist / nu

    return distToWall

def init():
    global u_tau, nu
    
    mu = 1.8e-4
    density = 1.027
    nu = mu / density
    kappa = 0.41
    ks = 3.5 *5
    y0 = ks / 30.0

    # Assume flow speed 2.0 m/s, at 30m above seabed
    udef=2.0
    ydef=30.0
        
    u_tau = kappa * udef / math.log(ydef/y0)

global dist_init
try:
    dist_init
except NameError:
    import nc_depth_io as ncd
    import math

    ncd.nc_init("gmsh/islay-jura-bathy.grd")
    
    print "*** Initialising distance to wall field"
    init()
    dist_init=1
