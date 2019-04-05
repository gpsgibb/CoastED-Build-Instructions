def init(heightArg, componentArg="x", horizontalIsotropy=0):
    import math
    global channelHeight, sqrtTwo, component, horizontalIsotropyFlag

    channelHeight = heightArg
    component = componentArg
    horizontalIsotropyFlag = horizontalIsotropy 

    sqrtTwo=math.sqrt(2)

def val(X, t):
    import math

    z=abs(X[2])

    if(component=="x"):
        scale=1.0
    elif(component=="y"):
        if(horizontalIsotropyFlag==0):
            scale=0.5
        else:
            scale=1.0
    elif(component=="z"):
        scale=0.25

    if(z<channelHeight/2):
        len = math.sqrt(z * channelHeight)
    else:
        len = channelHeight/sqrtTwo

    return len * scale

