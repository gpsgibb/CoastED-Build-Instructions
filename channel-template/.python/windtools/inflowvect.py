#-------------------------



def init():
    from windio import readWind

    global boundary, velcomponent, pi
    global winddir, windspeed, windheight, relaxtime, linesArray
    global relaxtime

    global heightdefined

    pi = 3.1415926535897932384626433832795
    

    # time for boundaries to go from 0 ->u0 m/s
    # change this if get instabilities


    wind = readWind()
        
    winddir = wind.direction
    windspeed = wind.speed
    windheight = wind.u0_height
    relaxtime = wind.relaxtime

    heightdefined=0
    



#-------------------------




def val ( (nodex, nodey, nodez), t):
    import math

    truewind = ((270 - 1.0*winddir)/360.0)*2.*pi

    u0=windspeed
    zR=0.001
    zTop=1000

    K = 0.41
    verySmall = 0.0001


    zfloor=0
    between=0



    # If height grid file was not found
    z = (nodez+zR) - zfloor
    if( z<zR ):
        z = zR

    # Now use windheight instead
    # zS = zTop - zfloor
    zS = windheight - zfloor

    if( t<relaxtime ):
        u0t = (t/relaxtime) * u0
    else:
        u0t = u0


    uTau = K * u0t / math.log(zS/zR)
    speed = (uTau / K) * math.log(z/zR)

    velcomp_u = speed * math.cos( truewind )
    velcomp_v = speed * math.sin( truewind )

    return (velcomp_u, velcomp_v, 0)

