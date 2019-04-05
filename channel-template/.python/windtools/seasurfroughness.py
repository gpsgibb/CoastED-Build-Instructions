# Calculate sea surface drag-coefficient as a function of hub-height wind speed

def init():
    from windio import readWind
    from inflow import val as inflowVal, init as inflowInit
    from seadefaults import getWindspeedRoughnessData

    global z0

    (u0_arr, z0_arr) = getWindspeedRoughnessData()

    # Find the free-stream wind speed u0 at 10m
    inflowInit("west", "u")

    wind = readWind()
    u0_10m=inflowVal([0, 0, 10], wind.relaxtime)
    
    targ_u0=u0_10m

    
    # Find this u0 in array, and interpolate cD accordingly

    last_u0=0
    last_z0=z0_arr[0]
    z0=z0_arr[0]

    ix=0
    for this_u0 in u0_arr:
        this_z0=z0_arr[ix]
        
        if(targ_u0 > last_u0 and targ_u0 <= this_u0):
            grad = (this_z0-last_z0)/(this_u0-last_u0)
            delta = targ_u0-last_u0
            
            z0 = delta * grad + last_z0
            
        # If we are beyond the last defined values of u0/cD, pick the last cD
        elif(targ_u0 > this_u0):
            z0 = z0_arr[-1]

        last_u0=this_u0
        last_z0=this_z0
        ix=ix+1



def val(X, t):
    return z0

    