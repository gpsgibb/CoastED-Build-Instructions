def init( maxval_arg, height_arg, windcomp_arg="", scaletime="no" ):
    import windio

    global maxval, maxheight, winddir, windcomp, pi, relaxtime

    pi = 3.1415926535897932384626433832795

    windcomp = windcomp_arg

    wind = windio.readWind()
    winddir = wind.direction

    maxval = maxval_arg
    maxheight = height_arg

    if(scaletime=="yes"):
        relaxtime = wind.relaxtime
    else:
        relaxtime = 0


# -------------------

def val( (x,y,z), t ):
    import math

    truewind = ((270 - 1.0*winddir)/360.0)*2.*pi

    if z >= maxheight:
        val = maxval
    else:
        scaledz = z/maxheight
        val = scaledz * maxval

    if(t>relaxtime or abs(relaxtime)<10e-10):
        timescale=1.0
    else:
        timescale = t/relaxtime
        

    if( windcomp == "u" ):
        val = val * math.cos( truewind )
    elif( windcomp == "v" ):
        val = val * math.sin( truewind )

    return timescale * val
