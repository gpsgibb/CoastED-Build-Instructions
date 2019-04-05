import simplechannel as sc
from math import sin, cos, pi 

def init(boundary, ramptimehours=48.0, scale=1.0):
    global boundaryName, ramptime, boundaryPts
    global scaleperm

    scaleperm = scale
    boundaryName=boundary

    ramptime=ramptimehours*60.0*60.0


# Fluidity calls this for each point on the boundary

def val( (x,y,z), t ):
            
    # now create interpolated values
    
    m2phase = 0.0
    m2amp = 0.5
    if(boundaryName=="north"):
        m2phase=pi

    m2ang = 2.0*pi/(12.421*3600.0)
    
    # Finally, generate difference in hydrostatic pressure due to tidal forcing
    g=9.81
    density=1.027

    # Add all tidal constituent fluctuations
    f = m2amp*cos(m2ang*t-m2phase) 

    if( abs(ramptime) < 1e-10):
        scalef=0.0
    else:
        if(t < ramptime):
            scalef=scaleperm*(1.0-(ramptime-t)/ramptime)
        else:
            scalef=scaleperm

    return density*g*scalef*f
