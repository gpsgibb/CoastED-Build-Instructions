# Absorption layer for model edge stability
def val( (x,y,z), t ):

    # relaxhours=3.0
    # relaxhours=1.0/12.0
    relaxhours=1.0

    minx=0.0
    miny=0.0

    maxx=21453.7278466
    maxy=36651.1955983

    thickness=500.0

    relaxtime=60.0*60.0*relaxhours

    abs=0.0
    wt=0.0
    wt2=0.0

    if(x < minx+thickness):
        wt=1.0-(x-minx)/thickness
    elif(x > maxx-thickness):
        wt=1.0-(maxx-x)/thickness

    if(y < miny+thickness):
        wt2=1.0-(y-miny)/thickness
    elif(y > maxy-thickness):
        wt2=1.0-(maxy-y)/thickness

    if(wt2>wt):
        wt=wt2

    abs=wt/relaxtime

    return [abs, abs, abs]
