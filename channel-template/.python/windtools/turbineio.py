# Only works for new turbines.dat format
import os

class Turbine():
    def __init__(self, id, coords, radius, length, orientation, hubFraction, type ):
        self.id = id
        self.coords = coords
        self.radius = radius
        self.length = length
        self.orientation = orientation
        self.hubFraction = hubFraction
        self.hubRadius = hubFraction * radius 
        self.type = type


def readTurbines(filename):
    turbArray=[]
    previx=-1
    
    fileExists = os.path.exists(filename)
    if not (fileExists):
        print "Turbine file '" + filename + "' does not exist"
        return None
        
    turbfile = open( filename, "r" )
    line = turbfile.readline().strip()

    # This is the 'turbine' label 
    while(line):
        if(line != "turbine"):
            print "Error: expected 'turbine' keyword; got '" + line + "' instead"
            exit(1)
            
        # Read in first line of section
        line = turbfile.readline().strip()
        
        id=None
        hubFraction=None
        radius=None
        coords=None
        length=None
        orientation=None
        modelType=None
        clone=""
        
        # parsing keywords
        while(line and line != "end turbine"):
            keyValPair = line.split("=")
            key = keyValPair[0].strip()

            if(len(keyValPair)>1):
                value = keyValPair[1].strip()
            else:
                value = ""
            
            key = key.strip()
            value = value.strip()
            
            if(key=="id"):
                id = value    

            if(key=="clone"):
                clone="previous"
            
            if(key=="coords"):
                coords=map(float, map(float, value.split()))
            
            if(key=="radius"):
                radius = float(value)    
                
            if(key=="length"):
                length = float(value)

            if(key=="orientation"):
                orientation = float(value)

            if(key=="type"):
                modelType = value
                
            if(key=="hub fraction"):
                hubFraction = float(value)

            line = turbfile.readline().strip()

        # Found 'end turbine'. 
        
        if(clone=="previous"):
            if(previx < 0):
                errMsg = "Can't clone turbine - no previous turbine has been defined"
                exit(ErrMsg)
                
            if(hubFraction is None):
                hubFraction = turbArray[previx].hubFraction
            if(radius is None):
                radius = turbArray[previx].radius
            if(length is None):
                length = turbArray[previx].length
            if(orientation is None):
                orientation = turbArray[previx].orientation
            if(coords is None):
                coords = turbArray[previx].coords
            if(modelType is None):
                modelType = turbArray[previx].type
        else:
            if(radius is None or length is None or orientation is None or coords is None or modelType is None or hubFraction is None):
                print "Error: can't find radius, length, coords or type for turbine"
                exit(1)
            
        turbArray.append(Turbine(id, coords, radius, length, orientation, hubFraction, modelType))
        previx = previx + 1
        
        line = turbfile.readline().strip()
        
    return turbArray




def csvColumnList(csvFile):
    columnList=[]
    
    line=csvFile.readline().strip()
    
    colwords=line.split(",")
    
    for colword in colwords:
        dictword=colword.strip()
        columnList.append(dictword)
        
    return columnList



def csvReadLineDiagnostics(csvFile, colNames):
    
    lineProperties={}
    
    ix=0
    
    line=csvFile.readline().strip()
      
    if(line):
        colValues=line.split(",")
        for val in colValues:
            colName=colNames[ix]
            sval=val.strip()
            
            if(colName=="id"):
                lineProperties[colName]=sval
            else:
                lineProperties[colName]=float(sval)
                
            ix=ix+1
            
        return lineProperties
        
    else:
        return None
    
