#!/usr/bin/python

import turbineio
import sys

class TurbineStat():
    def __init__(self, id, powerSum, averagePower, newCoords):
        self.id = id
        self.powerSum = powerSum
        self.averagePower = averagePower
        self.newCoords= newCoords
        self.xDist=newCoords[0]
        self.order=0




if (len(sys.argv)<3):
    print "usage: downwindpower.py <wind dir1,dir2,dir3,...> <output.csv>"
    exit(1)

dirs = sys.argv[1].split(",")

orderedTurbs=[]

startTime=2600
endTime=3200
dt=0.5
period=(endTime-startTime)

turbStats={}

directionResults={}

for wdir in dirs:
    print "Calculating for wind dir="+wdir+"..."
    
    turbines=turbineio.readTurbines(wdir+"/turbines.dat")

    # Find minimum x value    
    minx=10e10
    for turb in turbines:
        coords=turb.coords
        if( coords[0]<minx):
            minx=coords[0]
    
    for turb in turbines:
        coords=turb.coords
        newCoords = (coords[0]-minx, coords[1], coords[2])
        turbStats[turb.id]=TurbineStat(turb.id, 0.0, 0.0, newCoords)
    
    
    csvFile=open(wdir+"/turbines-output.csv", "r")
    
    columnList=turbineio.csvColumnList(csvFile)

    lp=turbineio.csvReadLineDiagnostics(csvFile, columnList)
    while(lp):
        
        if(lp["t"] >=startTime and lp["t"]<=endTime):
            id=lp["id"]

            turbStats[id].powerSum=turbStats[id].powerSum+lp["power"]    

        lp=turbineio.csvReadLineDiagnostics(csvFile, columnList)

    sortedArray = []
    for id in turbStats:
        turbStats[id].averagePower=turbStats[id].powerSum/(period/dt+1)
        sortedArray.append(turbStats[id])

    sortedArray.sort(key=lambda ts: ts.xDist)
        
    directionResults[wdir]=sortedArray
        
csvFile.close()

print "Writing to "+sys.argv[2]+"."

outputCSV=open(sys.argv[2], "w")
headerStr=""

for wdir in dirs:
    if(headerStr==""):
        headerStr="x ("+wdir+"), "+"power ("+wdir+"), id ("+wdir+")"
    else:
        headerStr=headerStr+", "+"x ("+wdir+"), "+"power ("+wdir+"), id ("+wdir+")"
        
outputCSV.write(headerStr+"\n")
    
# Always same number
for i in range(len(turbines)):
    first=1
    
    lineStr=""
    for wdir in directionResults:
        if(first==1):
            lineStr=str(directionResults[wdir][i].xDist)+", "+str(directionResults[wdir][i].averagePower)+", "+directionResults[wdir][i].id
            first=0
        else:
            lineStr=lineStr+", "+str(directionResults[wdir][i].xDist)+", "+str(directionResults[wdir][i].averagePower)+", "+directionResults[wdir][i].id

    outputCSV.write(lineStr+"\n")
    
    
outputCSV.close()