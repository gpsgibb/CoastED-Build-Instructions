#-------------------------



def init(arg_boundary, arg_velcomponent ):

    global boundary, velcomponent
    global winddir, windspeed, relaxtime
    global relaxtime

    # time for boundaries to go from 0 ->u0 m/s
    # change this if get instabilities

    relaxtime=60.0 


    boundary = arg_boundary
    velcomponent = arg_velcomponent

    windfile = open ("wind.dat", "r")
    words = windfile.readline().split()
    windfile.close()

    winddir = float( words[0] )
    windspeed = float( words[1] )
    relaxtime = float( words[2] )


#-------------------------




def val ( (nodex, nodey, nodez), t):
    import math

    pi = 3.1415926535897932384626433832795


    u0=windspeed
    zR=0.03
    zTop=500

    K = 0.41
    verySmall = 0.0001

    zfloor=0

    z = (nodez+zR) - zfloor
    if( z<zR ):
        z = zR


    zS = zTop - zfloor


    if( t<relaxtime ):
        u0t = (t/relaxtime) * u0
    else:
        u0t = u0


    uTau = K * u0t / math.log(zS/zR)
    speed = (uTau / K) * math.log(z/zR)

    truewind = ((270 - 1.0*winddir)/360.0)*2.*pi

    if(   velcomponent=="u" ):
        velcomp = speed * math.cos( truewind )
    elif( velcomponent=="v" ):
            velcomp = speed * math.sin( truewind )


    return velcomp

