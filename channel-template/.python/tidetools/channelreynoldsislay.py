def init(height, componentArg="x", \
             wall="off", y1=0.0, y2=0.0, \
             top="off", ztop=0.0):
    import windio, math

    global chanheight, component, uH, zH, uTau
    global cD, zR
    global y1val, y2val, sidewall, chanw, wallthresh, vwallthresh
    global topwall, ztopval

    chanheight = height
    component = componentArg

    # Von Karman
    K=0.41
    
    y1val = 1.0*y1
    y2val = 1.0*y2

    ztopval = 1.0*ztop

    chanw = abs(y1val-y2val)
    # Distance from wall at which we drop off Reynolds stress
    wallthresh = 10.0
    vwallthresh = 2.5

    sidewall = wall
    topwall = top
    
    wind = windio.readWind()
    uH = wind.speed
    zH= wind.u0_height 
    zRough = wind.featureheight


    uTau = uH * K / math.log(zH/zRough)
    

def val(X, t):
    from math import exp 

    z = X[2]


    # From Stacey et al, 1999.

    utausq_exp = (uTau**2.0) * exp(-2*z / chanheight)

    if component=="x":
        compscale = 5.29
    elif component=="y":
        compscale = 2.66
    else:
        compscale = 1.61
        

    wscale=1.0

    # Drop cross-stream Reynolds stress near vertical wall
    if (component=="y" and sidewall=="on"):
        mindist = abs(X[1]-y1val)
        maxdist = abs(X[1]-y2val)

        if(mindist > maxdist):
            dist = maxdist
        else:
            dist = mindist

        if(dist < wallthresh):
            wscale = dist/wallthresh

    elif (component=="z" and topwall=="on"):
        mindist = X[2]
        maxdist = abs(X[2]-ztopval)

        if(mindist > maxdist):
            dist = maxdist
        else:
            dist = mindist

        if(dist < vwallthresh):
            wscale = dist/vwallthresh

    value = (compscale * utausq_exp) * wscale
            
    return value
