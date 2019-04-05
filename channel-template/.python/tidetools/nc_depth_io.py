class Depth():
    def __init__(self, xMap, yMap, zMap, minDepth):

        self.nx=shape(xMap)[0]
        self.ny=shape(yMap)[0]
        self.minDepth = minDepth
        
        init="no"
        xMin=0
        xMax=0
        yMin=0
        yMax=0


        self.x = xMap
        self.y = yMap

        self.depth = zeros( (self.nx, self.ny) )


    	for j in range(self.ny):
            for i in range(self.nx):
                
                # Set the depth
                if(zMap[j][i] > -minDepth):
                    self.depth[i][j] = minDepth
                else:
                    self.depth[i][j] = -zMap[j][i]


# -----------------------------------------------------------------------------
# Given a NetCDF file, dump out tidal constituents into xyz files
# -----------------------------------------------------------------------------

def readDepthData(ncfilename, minDepth):
    netsrc = netcdf.NetCDFFile(ncfilename, "r") 

    # Return Depth object
    return Depth(netsrc.variables["x"], netsrc.variables["y"], \
                     netsrc.variables["z"], minDepth)

def calculateDepth(point):
    x = point[0]
    y = point[1]

    im = int( (x-gridorigx)/griddx )
    jm = int( (y-gridorigy)/griddy )

    if(im > iMax-1):
        im = -1

    if(jm > jMax-1):
        jm = -1

    # If can't find index, return with default depth
    if(im==-1 or jm==-1):
        return defaultDepth


    # Now define xLeft, xRight, indices, etc.

    xLeft=ddat.x[im]
    yDown=ddat.y[jm]

    if(im < iMax-1):
        iRight = im+1
    else:
        iRight = im

    if(jm < jMax-1):
        jUp = jm+1
    else:
        jUp = jm

                
    xRight = ddat.x[iRight]
    yUp = ddat.y[jUp]

    #
    # p3 ---- p4
    # 
    # |       |
    # |       |
    #
    # p1 ---- p2

    z1 = ddat.depth[im][jm]
    z2 = ddat.depth[iRight][jm]
    z3 = ddat.depth[im][jUp]
    z4 = ddat.depth[iRight][jUp]

    cellx = xRight-xLeft
    celly = yUp-yDown

    dx = x-xLeft
    dy = y-yDown

    ndx = (x-xLeft)/cellx
    ndy = (y-yDown)/celly

    mxUp = (z4-z3)/cellx
    mxDown = (z2-z1)/celly

    myLeft = (z3-z1)/celly
    myRight = (z4-z2)/celly

    mx = (1-ndy) * mxDown + ndy * mxUp
    my = (1-ndx) * myLeft + ndx * myRight

    depth = z1 + dx*mx + dy*my

    return depth



def nc_init(ncFileName, minDepth=3):
    global ddat, verySmall, defaultDepth
    global iMax, jMax, gridorigx, gridorigy, griddx, griddy

    ddat = readDepthData(ncFileName, minDepth)
    iMax = shape(ddat.x)[0]
    jMax = shape(ddat.y)[0]

    gridorigx = ddat.x[0]
    gridorigy = ddat.y[0]

    griddx = ddat.x[1] - gridorigx
    griddy = ddat.y[1] - gridorigy

    verySmall=10e-4


    defaultDepth = minDepth


global nc_raninit
try:
    nc_raninit
except NameError:
    from scipy.io import netcdf
    from numpy import *
    nc_raninit=1
