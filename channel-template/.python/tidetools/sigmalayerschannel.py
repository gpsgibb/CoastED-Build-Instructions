import math
from simplechannel import *

minthick=5.0
maxlayers=5

def val(pt, t):

    depth = channelDepth(pt)

    nlayers=int(math.floor(depth/minthick))
    if(nlayers > maxlayers):
        nlayers=int(maxlayers)
    elif(nlayers < 1):
        nlayers=1

    dz = 0.5 * depth / nlayers

    if (dz < 0.5*minthick):
        dz = 1.1* 0.5*minthick

    return dz
