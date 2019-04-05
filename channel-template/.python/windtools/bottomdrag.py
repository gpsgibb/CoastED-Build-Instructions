# --------------------------------------------------------------------------

def init():
    global roughnessbuffer

    xyzfile = open("roughness-grid.xyz", "r")

    roughnessbuffer = xyzfile.readlines()
    xyzfile.close()


# --------------------------------------------------------------------------

def val( (nodex, nodey, nodez), t):
    import math

    closeness = 100

    # Karman constant
    K = 0.41

    roughness = 0.0
    drag_coeff = 0.0

    # Quick bit of calculation.. take value of nearest point                    
    for line in roughnessbuffer:
        (gx, gy, grough, gfeat, gdrag_coeff) = line.split()

        if ( abs(float(gx)-nodex) + abs(float(gy)-nodey) < closeness ):

            roughness = float(grough)
            feature_ht = float(gfeat)
            drag_coeff = float(gdrag_coeff)

            # zero_plane_disp = (2./3.) * feature_ht
            # dz = feature_ht - zero_plane_disp
            
            # drag_coeff = ( K / ( math.log( (roughness+dz) / roughness ) ) )
            
            break


    return drag_coeff
