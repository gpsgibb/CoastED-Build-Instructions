#!/usr/bin/python

import sys


inname="turbines-output.csv"
outname="reparsed-output.csv"

if(len(sys.argv)<2):
    print "usage: reparseoutput.py <no. turbines>"
    exit(1)

numturbs=int(sys.argv[1])


infile=open(inname, "r")
outfile=open(outname, "w")



# grab ids
ids=[]
for i in range (1,numturbs+2):
    lineparams=infile.readline().split(",")

    j=0
    for param in lineparams:
        if j==1:
            ids.insert(i, param.rstrip(" ").lstrip(" "))
        j=j+1

infile.seek(0)


inline=infile.readline()
infields=inline.split(",")


outline=""
for i in range (1,numturbs+1):

    for field in infields:
        fieldname = field.rstrip("\n").lstrip()

        if (fieldname == "t"):
            outline = outline + fieldname
        else:
            outline = outline + ids[i] +"." + fieldname
            
        if (field != infields[len(infields)-1] ) \
                or (field == infields[len(infields)-1] \
                        and i<numturbs) :
            outline=outline+", "

outfile.writelines(outline+"\n")


keepreading=1



while(keepreading==1):
    outline = ""

    for i in range (1,numturbs+1):
        inline = infile.readline()

        if(inline==""):
            keepreading=0
        else:
            if(i==1):
                outline = inline.rstrip("\n")
            else:
                outline = outline + ", " + inline.rstrip("\n")


    outfile.writelines(outline+"\n")

infile.close()
outfile.close()



