def init( maxval_arg, height_arg, windcomp_arg, scaletime="no" ):
    import windio

    global maxval, maxheight, winddir, windcomp, pi, relaxtime

    pi = 3.1415926535897932384626433832795

    windcomp = windcomp_arg

    wind = windio.readWind()
    winddir = wind.direction
    if(scaletime=="yes"):
        relaxtime = wind.relaxtime
    else:
        relaxtime = 0

    maxval = maxval_arg
    maxheight = height_arg


# -------------------

def val( (x,y,z), t ):
    import math

    truewind = ((270 - 1.0*winddir)/360.0)*2.*pi


    if z >= maxheight:
        truemaxval = maxval
    else:
        scaledz = z/maxheight
        truemaxval = scaledz * maxval

    paralen = truemaxval
    tanglen = paralen

    vertlen = truemaxval / 3.0

    if(t>relaxtime or abs(relaxtime)<10e-10):
        scale=1.0
    else:
        scale = t/relaxtime
        
    if( windcomp == "u" ):
        val = paralen * math.cos( truewind ) - tanglen * math.sin( truewind )  
    elif( windcomp == "v" ):
        val = paralen * math.sin( truewind ) + tanglen * math.cos( truewind )  

    elif( windcomp =="w" ):
        val = vertlen

    return scale * val
