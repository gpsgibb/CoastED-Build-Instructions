from simplechannel import *

def val( (x,y,z), t ):

    # relaxhours=3.0
    # relaxhours=1.0/12.0
    relaxhours=0.5

    thickness=500.0

    relaxtime=60.0*60.0*relaxhours

    abs=0.0
    wt=0.0
    wt2=0.0

    # if(x < thickness):
    #     wt=1.0-x/thickness
    # elif(x > maxx-thickness):
    #     wt=1.0-(maxx-x)/thickness

    if(y < thickness):
        wt2=1.0-y/thickness
    elif(y > maxy-thickness):
        wt2=1.0-(maxy-y)/thickness

    if(wt2>wt):
        wt=wt2

    abs=wt/relaxtime

    return [abs, abs, abs]
