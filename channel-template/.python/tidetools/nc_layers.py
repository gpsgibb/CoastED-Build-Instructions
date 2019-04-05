def init(cenx, ceny):
    global centrept

    centrept = (cenx, ceny)


def val(pt,t):

    maxDist=10000

    dist = ((centrept[0]-pt[0])**2. + (centrept[1]-pt[1])**2.)**0.5


    if( dist < 0.5*maxDist ):
        layerSpacing = 10

    elif( dist < 0.75*maxDist ):
        layerSpacing = 25

    elif( dist < maxDist ):
        layerSpacing = 50

    else:
        layerSpacing = 100

    return layerSpacing
    
