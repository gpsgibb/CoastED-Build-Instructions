# Currently only works for BEM turbines in new format


def init(scale=1, restrict_after_first=0):
    from turbineio import readTurbines
    
    global turbines, fieldScale, restrictAfterFirst, turbinesDisabled
    
    fieldScale=scale
    restrictAfterFirst=restrict_after_first
    
    turbines=readTurbines("turbines.dat")

    turbinesDisabled=1
    if not (turbines is None):
        for turb in turbines:
            if not turb.type == "off":
                turbinesDisabled=0

#-----------------------------------------------------------------------

def val( (x,y,z), t ):
    global firstTime

    if turbinesDisabled==1:
        return 0.

    if(not 'firstTime' in globals()):
        firstTime=t


    notFirst=1
    if(abs(firstTime-t) < 10e-10):
        notFirst=0

    # If we have no turbines, return 0
    if(turbines is None):
        return 0.


    tPres=0.
    newTPres=0.

    for turb in turbines:
        if not (turb.type=="off"):

            transx = x - turb.coords[0]
            transy = y - turb.coords[1]
            transz = z - turb.coords[2]

            rp = ( transx**2 + transy**2 + transz**2 )**.5

            if(rp > turb.length/2 and restrictAfterFirst==1 and notFirst==1):
                newTPres = 0
            else:
                scalen = 2 *turb.radius * fieldScale

                if( rp < scalen ):
                    newTPres = (1-rp/scalen)**4.0
                
                    if newTPres > tPres:
                        tPres = newTPres
            

    return tPres
