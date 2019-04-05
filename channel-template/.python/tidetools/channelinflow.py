#-------------------------



def init(arg_roughness, ywall1_arg=-10e10, ywall2_arg=10e10, profile="log" ):

    from windio import readWind

    global boundary, velcomponent, pi
    global winddir, windspeed, windheight, relaxtime, linesArray
    global relaxtime

    global heightdefined, roughnesslength, featureheight, profileType
    global ywall1, ywall2

    pi = 3.1415926535897932384626433832795
    
    profileType = profile

    # time for boundaries to go from 0 ->u0 m/s
    # change this if get instabilities


    roughnesslength = arg_roughness

    ywall1 = ywall1_arg
    ywall2 = ywall2_arg


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

    distFromBottom = nodez
    distFromWall1 = abs(nodey-ywall1)
    distFromWall2 = abs(nodey-ywall2)

    if(distFromBottom < distFromWall1 and distFromBottom < distFromWall2):
        dist = distFromBottom
    else:
        if(distFromWall1 < distFromWall2):
            dist = distFromWall1
        else:
            dist = distFromWall2

    z = dist + featureheight

    if( t<relaxtime ):
        u0t = (t/relaxtime) * u0
    else:
        u0t = u0

    # Generate profile according to type selected (log, power, ...)

    if(profileType=="log"):
        # log law.
        #
        # Added 8.5 constant from:
        # "Turbulence in Open-Channel Flows", Nezu & Nagakawa 1993.

        uTau = u0t  /( (1.0/K) * math.log((windheight+zR)/zR) + 8.5 )
        speed = (uTau / K) * math.log((z+zR)/zR) + 8.5 * uTau
    
    elif(profileType=="power"):
        # Replaced with 1/7 power law
        if(dist>zR):
            speed = u0t * (dist/windheight)**(1/7)
        else:
            speed = 0

    else:
        print "channelinflow.py: profileType not recognised"

    return speed
    

