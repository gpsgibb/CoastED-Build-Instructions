def init( arg_mindx, arg_maxdx, \
              arg_mindy, arg_maxdy, \
              arg_mindz, arg_maxdz, \
              arg_height, \
              outputValue="matrix"):

    global mindx, mindy, mindz
    global maxdx, maxdy, maxdz
    global height

    global defaultOutputValue

    mindx = float(arg_mindx)
    mindy = float(arg_mindy)
    mindz = float(arg_mindz)

    maxdx = float(arg_maxdx)
    maxdy = float(arg_maxdy)
    maxdz = float(arg_maxdz)
    height = float(arg_height)

    defaultOutputValue = outputValue 


# -------------------

def val( (x,y,z), t ):

    if( z >= height ):
        maxwt = 1.0
    else:
        maxwt = (z/height)

    minwt = 1.0-maxwt


    retdx = minwt*mindx + maxwt*maxdx
    retdy = minwt*mindy + maxwt*maxdy
    retdz = minwt*mindz + maxwt*maxdz
        

    if(defaultOutputValue=="matrix"):
        minMaxLengths=[ [retdx, 0, 0,], \
                            [0, retdy, 0], \
                            [0, 0, retdz] ]
    elif(defaultOutputValue=="vector"):
        minMaxLengths=[ retdx, retdy, retdz ]

    return minMaxLengths
