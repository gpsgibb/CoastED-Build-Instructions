#!/usr/bin/env python

import os
import sys
from scipy.io import netcdf
from numpy import *


class Range():
    def __init__(self, minval, maxval):
        self.min = minval
        self.max = maxval

        
class Tide():
    def __init__(self, const, lon, lat, amp, phase):
        print "Creating new Tide() object..."
        
        self.constituents=[]
        for cstr in const:
            self.constituents.append(cstr.upper())
            
        self.nc = len(const)
        self.lat=lat
        self.lon=lon
        
        dims = shape(lon)
        self.nx = dims[0]
        self.ny = dims[1]
        self.amp=[]
        self.phase=[]
        
        
        init="no"
        minlon=0
        maxlon=0
        minlat=0
        maxlat=0


        # find range etc.
        for n in range(len(const)):
            print "   adding "+self.constituents[n]

            thisAmp = amp[n]
            thisPhase = phase[n]
            
            newAmp = thisAmp
            newPhase =  thisPhase
            
            for y in range(self.ny):
                for x in range(self.nx):
    
                    # This bit fixes the orientation(vertical flip)
                    newAmp[x][y] = thisAmp[x][y]
                    newPhase[x][y] = thisPhase[x][y]
                    
                    thislon = lon[x][y]
                    thislat = lat[x][y]
    
                    if(init=="no"):
                        minlon=thislon
                        maxlon=thislon
                        minlat=thislat
                        minlat=thislat
    
                        init="yes"
                    else:
                        if(maxlon < thislon):
                            maxlon = thislon
                        if(minlon > thislon):
                            minlon = thislon
    
                        if(maxlat < thislat):
                            maxlat = thislat
                        if(minlat > thislat):
                            minlat = thislat

            self.amp.append(newAmp)
            self.phase.append(newPhase)
            
                
        self.deltaLon = (maxlon - minlon) / (self.nx-1)
        self.deltaLat = (maxlat - minlat) / (self.ny-1)
        
        self.lonRange = Range(minlon, maxlon)
        self.latRange = Range(minlat, maxlat)
    
    
    
    

# -----------------------------------------------------------------------------
# Given a NetCDF file, dump out tidal constituents into xyz files
# -----------------------------------------------------------------------------

def readTideData(ncfilename):

    netsrc = netcdf.NetCDFFile(ncfilename, "r")
    xyzRoot = ncfilename.replace(".nc", "")
    
    # pull out tidal constituent names
    
    
    nc = netsrc.dimensions["nc"]
    nct = netsrc.dimensions["nct"]
    
    convar = netsrc.variables["con"]
    convarArray=convar.getValue()
    
    constNames=[]
    for i in range(nc):
       constStr=""
    
       for j in range(nct):
          constStr = constStr + convarArray[i][j]
    
       constStr = constStr.strip()
       constNames.append(constStr)
    
    
    dims = shape(netsrc.variables["lon_z"])
    nx = dims[0]
    ny = dims[1]
    
    lon = netsrc.variables["lon_z"]
    lat = netsrc.variables["lat_z"]
    ha = netsrc.variables["ha"]
    hp = netsrc.variables["hp"]
    
    
    # Return tide object
    
    return Tide(constNames, lon, lat, ha, hp)

     
# -----------------------------------------------------------------------------

def writeCroppedData(newfile, tide, lonCropRange, latCropRange, xCropRange, yCropRange):
    nn = NetCDF.NetCDFFile(newfile, "w")
    
    nn.createDimension("latitude", tide.ny)
    nn.createDimension("longitude", tide.nx)

    amp=[]
    phase=[]

    lat = nn.createVariable("latitude", 'd', ("longitude", "latitude"))
    lon = nn.createVariable("longitude", 'd', ("longitude", "latitude"))
    
    lon[:] = tide.lon
    lat[:] = tide.lat

    
    n=0
    for const in tide.constituents:
        amp.append(nn.createVariable(const+"amp", 'd', ("longitude", "latitude" )))
        phase.append(nn.createVariable(const+"phase", 'd', ("longitude", "latitude")))

        amp[n][:] = tide.amp[n]
        phase[n][:] = tide.phase[n]

        n=n+1
    
    nn.close()

# -----------------------------------------------------------------------------



(crud, programName) = os.path.split(sys.argv[0])

if(len(sys.argv)<4):
   print "error:"
   print "usage: "+programName+" <netcdf file> <lonmin/lonmax/latmin/latmax> <minx/maxx/miny/maxy>"
   exit(1)


# Get cropping range out for lon / lat

cStrings=sys.argv[2].split("/")

lonCropRange=Range(float(cStrings[0]), float(cStrings[1]))
latCropRange=Range(float(cStrings[2]), float(cStrings[3]))

xStrings=sys.argv[3].split("/")

# Sizes to stretch to (in m)

xCropRange=Range(float(xStrings[0]), float(xStrings[1])) 
yCropRange=Range(float(xStrings[2]), float(xStrings[3])) 


# if (not os.path.isdir(grddir)):
#   print "creating "+grddir+"/  ..."
#   os.mkdir(grddir)


ncfilename=sys.argv[1]

tide = readTideData(ncfilename)

newncfile = ncfilename.replace(".nc", "")+"-crop.nc"
writeCroppedData(newncfile, tide, lonCropRange, latCropRange, xCropRange, yCropRange)

print "*** done"
exit (0)
