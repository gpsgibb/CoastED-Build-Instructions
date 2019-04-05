#!/usr/bin/python
#
# Quick program to read in columns from turbine SCADA data,  
# calculate stats, etc.
#

import sys
import time


class Criterion():
     def __init__(self, fieldName, type, format, min, max, value ):
         self.field = fieldName
         self.type = type
         self.format = format
         self.min = min
         self.max = max
         self.value = value


allowedFormatTypes = ["string", "float", "time"]
UTCFormatString="%Y-%m-%d %H:%M:%S"


def printConfigurationFormat():
    print ""
    print "Configuration file format:"
    print ""
    
    print "begin criteria"
    print "  field = field_name"
    print "  type = <equals | min max>"
    print "  format = <string | float | time>"
    print "  value = equals_value (type=equals) OR value = min, max (type=min max)"
    print "  field = ..."
    print "  ..."
    print "end criteria"
    print "begin output fields"
    print "  field_name 1, field_name 2,"
    print "  field_name 3, field_name 4, field_name 5"
    print "  ..."
    print "  (spacing and new lines between commas are arbitrary)"
    print "end output fields"
    print ""
    
    
    
def parseArguments(argv):
    nargs = len(argv)
    
    if nargs < 3:
        print "*** usage: scadagrabber.py <csv file> <config file> [output file]"
        exit(1)
        
    if nargs < 4:
        outputFile = ""
    else:
        outputFile = argv[3]
    return(argv[1], argv[2], outputFile)



def initColumnDictionary(csvColumns):
    colDict = {}
    
    count = 0
    for column in csvColumns:
        colDict[column] = count
        count = count+1

    return colDict



def readCSVColumnNames(csvfile):
    csvFields = []
    headerline =  csvfile.readline()
    headers = headerline.strip().split(",")
    for fieldName in headers:
        fieldName = fieldName.strip().strip('"')
        csvFields.append(fieldName)

    return csvFields



def getKeywordPair(thisFile):
    (key, val) = thisFile.readline().strip().split("=")
    key = key.strip()
    val = val.strip()
    
    return (key, val)
    


def makeSecondsFromDateString(dateString):

    dateString = dateString.rstrip("Z")
    timeTuple = time.strptime(dateString, UTCFormatString)
    secondsEpoch = time.mktime(timeTuple)
    
    return secondsEpoch
    
    

def readSingleCriterion(cfgfile, firstline):
    # We've already read in the first line, so we'll just strip that manually.
    (fieldkey, fieldval) = firstline.strip().split("=")
    fieldkey = fieldkey.strip()
    fieldval = fieldval.strip()
    
    (typekey, typeval) = getKeywordPair(cfgfile)
    (formatkey, formatval) = getKeywordPair(cfgfile)

    if(fieldkey != "field" or typekey != "type" or formatkey != "format"):
        print "*** field, type, or format keywords non-existent or in wrong order."
        printConfigurationFormat()
        exit(1)
    
    if(formatval not in allowedFormatTypes):
        print "*** Criteria allowed data formats are:", allowedFormatTypes
        exit(1)

    (key, val) = getKeywordPair(cfgfile)    
    if(key!="value"):
        print "*** You need to specify value=<min, max | equals_value> in the config file."
        printConfigurationFormat()
        exit(1)
    
    if(typeval=="min max"):
        substrs = ()
        substrs = val.strip().split(",")
        
        if(len(substrs)<2):
            print "*** Must specified min and max values for field criterion type 'min max', eg:"
            print "*** value = minumum, maximum"
            printConfigurationFormat()
            exit(1)
            
        minstr=substrs[0].strip() 
        maxstr=substrs[1].strip() 
            
        if(formatval=="float"):
            minval = float(minstr)
            maxval = float(maxstr)
        elif(formatval=="time"):
            minval = makeSecondsFromDateString(minstr)
            maxval = makeSecondsFromDateString(maxstr)
        elif(formatval=="string"):
            print "*** For 'min max' criteria, the format 'string' currently has no meaning."
            exit(1)
            
        return Criterion(fieldval, typeval, formatval, minval, maxval, 0)
            
    elif(typeval=="equals"):
        if(formatval=="float"):
            eqval = float(val)
        elif(formatval=="time"):
            eqval = makeSecondsFromDateString(val)
        elif(formatval=="string"):
            eqval = val
        
        return Criterion(fieldval, typeval, formatval, 0, 0, eqval)
        

    # If we get here, something's gone wrong.
    print "*** unknown criteria type '"+typeval+"'"
    exit(1)
            
    


def parseConfigurationFile(filename):
    
    criteria = []
    
    cfgfile = open(filename, "r")
    if (not cfgfile):
        print "Can't open configuration file '" + filename + "'."
        exit(1)
    
    linestr = cfgfile.readline().strip()
    
    if(linestr != "begin criteria"):
        printConfigurationFormat()
        exit(1)
        
    linestr = cfgfile.readline().strip()
    while(linestr != "end criteria"):
        thisCriterion = readSingleCriterion(cfgfile, linestr) 
        criteria.append(thisCriterion)

        linestr = cfgfile.readline().strip()
        
    
    linestr = cfgfile.readline().strip()
    if(linestr != "begin output fields"):
        print "Section after criteria must be 'output fields'."
        printConfigurationFormat()
        exit(1)

    outputFields = []
    linestr = cfgfile.readline().strip()
    while(linestr and linestr != "end output fields"):
        words = linestr.strip().split(",")
        
        for fieldWord in words:
            if(fieldWord != ""):
                outputFields.append(fieldWord.strip())
        
        linestr = cfgfile.readline().strip()
        
    return (criteria, outputFields)
        


def checkCriteriaAndOutputFields(csvFields, criteria, outputFields):
    for crit in criteria:
        if(crit.field not in csvFields):
            print "*** criteria field", crit.field, "not in csv file."
            exit(1)

        if(crit.type=="min max"):
            if(crit.min > crit.max):
                print "*** criteria field", crit.field, "has min > max."
                exit(1)
                
    missingFields = []
    for outfield in outputFields:
        if(outfield not in csvFields):
            missingFields.append(outfield)
            
    if(len(missingFields)>0):
        print "*** The following output fields are not in the CSV data file:"
        for miss in missingFields:
            print "  " + miss
        exit(1)
        


def splitCSVString(inString):
    csvCols= []
    valwords = inString.split(",")
    
    for val in valwords:
        csvCols.append(val.strip())
        
    return csvCols
        
     
     
def filterCSVData(csvFile, colDict, criteria, outputFields, outputName):
    
    if(outputName != ""):
        outputFile = open(outputName, "w")
    else:
        outputFile = sys.stdout

    # Write out the output CSV header first
    writestr = ""
    for outfield in outputFields:
        if(writestr==""):
            writestr=outfield
        else:
            writestr=writestr+", "+outfield
    outputFile.writelines(writestr+"\n")       

    # Now we just sift through the input CSV file, writing out anything
    # that fits our criteria
    
    readstr = csvFile.readline().rstrip()


    while(readstr):
        dataCols = splitCSVString(readstr)
        
        # Now check if this row doesn't match specified criteria
        isMatch = True
        for crit in criteria:
            rawval = dataCols[colDict[crit.field]]

            # You can't compare times/floats with the string 'NA', so reject.
            if( ( (crit.format == "time" or crit.format == "float") \
                and rawval == "NA" ) or rawval == "" ):
                isMatch=False
            else:
                if(crit.format=="time"):
                    colval = makeSecondsFromDateString(rawval)
                elif(crit.format=="float"):
                    colval = float(rawval)
                elif(crit.format=="string"):
                    colval = rawval
                
                if(crit.type=="min max"):
                    if(crit.format=="string"):
                        isMatch = False
                    else:
                        if(colval < crit.min or colval > crit.max):
                            isMatch = False
                
                if(crit.type=="equals" and crit.value != colval):
                    isMatch = False
        

        # If we have a match, output the columns specified in 'output fields'
        if(isMatch):
            outputStr = ""
            
            for field in outputFields:
                outval = dataCols[colDict[field]]
                strval = str(outval)
                if(strval.endswith("Z")):
                    strval = strval.rstrip("Z")
                
                if(outputStr==""):
                    outputStr=strval
                else:
                    outputStr = outputStr + ", " + strval
                    
            outputFile.writelines(outputStr+"\n")
                
        
        readstr = csvFile.readline().rstrip()
    

    outputFile.close()
        
        
# ----------- Main program

def main(argv):
    (csvName, configName, outputName) = parseArguments(argv)

    csvFile = open( csvName, "r" )
    csvFields = readCSVColumnNames(csvFile)

    columnDict = initColumnDictionary(csvFields)

    (criteria, outputFields) = parseConfigurationFile(configName)

    checkCriteriaAndOutputFields(csvFields, criteria, outputFields)    
    filterCSVData(csvFile, columnDict, criteria, outputFields, outputName)

    csvFile.close()

    print "scadagrabber: written to", outputName
    print ""
    
    
# Entry point for program.
main(sys.argv)
