#-------------------------



def init(arg_boundary, arg_velcomponent, arg_roughness=0.0001 ):

    from windio import readWind

    global boundary, velcomponent, pi
    global winddir, windspeed, windheight, relaxtime, linesArray
    global relaxtime

    global heightdefined, roughnesslength, featureheight

    pi = 3.1415926535897932384626433832795
    

    # time for boundaries to go from 0 ->u0 m/s
    # change this if get instabilities


    boundary = arg_boundary
    velcomponent = arg_velcomponent
    roughnesslength = arg_roughness


    wind = readWind()
        
    winddir = wind.direction
    windspeed = wind.speed
    windheight = wind.u0_height
    relaxtime = wind.relaxtime
    featureheight = wind.featureheight

    linesArray={}
    try:
        grdfile = open( "height-grid.xyz", "r" )
        heightdefined=1

        linect=0
        linestr=grdfile.readline()
        
        while ( linestr ):
            linesArray[linect]=linestr
            linestr=grdfile.readline()
            linect = linect+1
            
        grdfile.close()

    except IOError:
        heightdefined=0
    



#-------------------------




def val ( (nodex, nodey, nodez), t):
    import math

    truewind = ((270 - 1.0*winddir)/360.0)*2.*pi

    u0=windspeed
    zR=roughnesslength
    zTop=1000

    # Charnock parameter, as defined in Charnock, 
    # "Wind stress over a water surface"
    # ch=0.007

    # Von Karman
    K = 0.41

    verySmall = 0.0000000001
    zfloor=0

    between=0

    newlines=0
    maxlines=len(linesArray)


    z = nodez + featureheight

    if( t<relaxtime ):
        u0t = (t/relaxtime) * u0
    else:
        u0t = u0


    uTau = u0t * K / math.log((windheight+zR)/zR)

    speed = (uTau / K) * math.log((z+zR)/zR)

    if(   velcomponent=="u" ):
        velcomp = speed * math.cos( truewind )
    elif( velcomponent=="v" ):
        velcomp = speed * math.sin( truewind )

    return velcomp
    

