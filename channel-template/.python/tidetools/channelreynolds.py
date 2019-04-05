def init(heightArg, componentArg="x", u0NormArg=3.0, scaleArg=1.0, hscale=2):
    import windio

    global channelHeight, component, u0, u0Norm, relaxtime, scaledZ, values
    global allScale, heightScale

    wind = windio.readWind()
    relaxtime=wind.relaxtime
    u0 = wind.speed

    u0Norm=u0NormArg
    allScale = scaleArg
    heightScale = hscale
    
    channelHeight = heightArg
    component = componentArg


    # From Fluidity SEM example

    if(component=="x"):
        scaledZ=[0.0, 0.05, 0.1, 0.15,0.2, 0.25,0.3, 0.9,1.0]
        values=[0.0,0.0085,0.032,0.0675,0.096,0.0933,\
                      0.069,0.0375,0.0365]

    elif(component=="y"):
        scaledZ=[0.0, 0.05, 0.1, 0.15,0.2, 0.25,0.3, 0.9,1.0]
        values=[0.0,0.0085,0.032,0.0675,0.096,0.0933,\
                      0.069,0.0375,0.0365]

#        scaledZ=[0.0, 0.15,0.2,0.3,0.7,1.0]
#        values=[0.0,0.02,0.02,0.004,0.001,0.0005]

    elif(component=="z"):
        scaledZ=[0.0,0.3,0.9,1.0]
        values=[0.0,0.015,0.012,0.0]




def val(X, t):

    # Reynolds stresses used only really apply to bottom 1/2 of channel.
    zn = heightScale * X[2] / channelHeight
    if(zn > 1.0):
        zn=1.0


    if(t<relaxtime):
        tscale=t/relaxtime
    else:
        tscale=1.0


    # valscale=tscale/u0Norm
    
#    if (u0< u0Norm):
#        valscale=(u0/u0Norm)**2.0
#    else:
#        valscale=(u0/u0Norm)

    # Scale it to something sensible.
    if(abs(allScale) < 10e-10):
        valscale=(u0/u0Norm)
    else:
        valscale=allScale * (u0/u0Norm) 
        

    value = 0
    for i in range(len(scaledZ)-1):
        if (zn>=scaledZ[i] and zn<=scaledZ[i+1]):
            value=values[i]+(zn-scaledZ[i])*((values[i+1]-values[i]) \
                                                  /(scaledZ[i+1]-scaledZ[i]))

    # Assuming Re stress profiles vary linearly with flow speed in tidal
    # channels. See following paper:
    #
    # 'Reynolds Stress and Turbulent Energy Production in a Tidal Channel',
    # T.P. Rippeth et al, J. Phys Ocean., 2001

    value = valscale*value
            
    return value
