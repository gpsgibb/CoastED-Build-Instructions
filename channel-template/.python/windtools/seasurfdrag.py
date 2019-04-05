# Calculate sea surface drag-coefficient as a function of hub-height wind speed

def init():
    from windio import readWind
    from inflow import val as inflowVal, init as inflowInit
    from seadefaults import getWindspeedDragData

    global cD


    (u0_arr, cD_arr) = getWindspeedDragData()

    # Find the free-stream wind speed u0 at 10m
    inflowInit("west", "u")

    wind = readWind()
    u0_10m=inflowVal([0, 0, 10], wind.relaxtime)
    
    targ_u0=u0_10m

    
    # Find this u0 in array, and interpolate cD accordingly

    last_u0=0
    last_cD=cD_arr[0]
    cD=cD_arr[0]

    ix=0
    for this_u0 in u0_arr:
        this_cD=cD_arr[ix]
        
        if(targ_u0 > last_u0 and targ_u0 <= this_u0):
            grad = (this_cD-last_cD)/(this_u0-last_u0)
            delta = targ_u0-last_u0

            cD = delta * grad + last_cD
            
        # If we are beyond the last defined values of u0/cD, pick the last cD
        elif(targ_u0 > this_u0):
            cD = cD_arr[-1]

        last_u0=this_u0
        last_cD=this_cD
        ix=ix+1



def val(X, t):
    return cD

    