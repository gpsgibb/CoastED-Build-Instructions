def val( (nodex, nodey, nodez), t):

    depth=750
    
    closeness = 20
    doublecl = 2 * closeness

    xyzfile = open("myres-grid.xyz", "r")
    buffer = xyzfile.readlines()
    xyzfile.close()

    z = -depth

    # Quick bit of calculation.. take value of nearest point
    for line in buffer:
        (gx, gy, height) = line.split()

        if ( abs(float(gx)-nodex) + abs(float(gy)-nodey) < doublecl ):
            z = float(height) - depth
            break


    return z

