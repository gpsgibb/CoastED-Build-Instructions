#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pylab as pb
import math
import sys
from operator import itemgetter

class LinePlot():
	def __init__(self, name, xdata, ydata):
		self.name = name
		self.xdata = xdata
		self.ydata = ydata
		
class GraphPlot():
	def __init__(self, linePlots, graphtitle):
		self.linePlots = linePlots
		self.title = graphtitle

	

def reorderToX(xvals, yvals1, yvals2):
	newx, newy1, newy2 = (list(x) for x in zip(*sorted(zip(xvals, yvals1, yvals2),key=itemgetter(0))))

	return newx, newy1, newy2



verySmall=10e-5

turbx=247
turbD=16

if len(sys.argv)<3:
    print "usage: seagen-plot-verts.py <csv file> <u profile.csv>"
    exit(1)

outname=sys.argv[2]
csvname=sys.argv[1]

# Ridiculous hack because genfromtxt doesn't allow ":# ..." in file names

# Grab labels
cfile = open(csvname, "r")
labels=cfile.readline().split(",")
cfile.close()

for i in range(0,len(labels)):
	lab = labels[i].strip('"\n')
	labels[i]=lab

	
# get data

data = np.genfromtxt(csvname, delimiter=',', skip_header=0, \
                         names=True)
# replace labels with original (forbidden) labels
data.dtype.names=labels

# end ridiculous hack


yarr=[87, 100, 113]

# Each y is one row of plots

dias= [ -5, -2, -1, 0, 1, 2, 3, 5, 10, 20, 40 ]

uGraphs=[]
tiGraphs=[]

print "Calculating averaged profiles..."

for ytarg in yarr:

	uPlots=[]
	tiPlots=[]
	
	# collect line plot data for this row
	for dtarg in dias:

		zData = []
		uData = []
		tiData = []
		
		for n in range(0,len(data)):
			x = data['Points:0'][n]
			y = data['Points:1'][n]
			z = data['Points:2'][n]
			
			u = data['Velocity_average:0'][n]
			v = data['Velocity_average:1'][n]
			w = data['Velocity_average:2'][n]
			umag=math.sqrt(u**2.+v**2.+w**2.)

			ht=16.0
			zR=0.05
			uTau = 2.0  /( (1.0/0.41) * math.log(16/zR) + 8.5 )
			u0 = (uTau / 0.41) * math.log((z+zR)/zR) + 8.5 * uTau

			
			Ruu = data['Velocity_stddev:0'][n]
			Rvv = data['Velocity_stddev:1'][n]
			Rww = data['Velocity_stddev:2'][n]
			
			if( abs(u0)<verySmall):
				ti=0.0
			else:
				ti=math.sqrt( (Ruu+Rvv+Rww)/3.0 ) / u0

			D = (x-turbx)/turbD

			# Is this the point we are looking for?
			if(abs(D-dtarg) < verySmall and abs(y-ytarg) < verySmall):
				zData.append(z)
				uData.append(umag)
				tiData.append(ti)
			
	
		zData, uData, tiData= reorderToX(zData, uData, tiData)
		plotLegend = "x="+`dtarg`

		uPlot  = LinePlot(plotLegend, uData,  zData)
		tiPlot = LinePlot(plotLegend, tiData, zData)
		
		uPlots.append(uPlot)
		tiPlots.append(tiPlot)

	
	# We now have ordered data for this pair of plots on a row. 
	# Shove into graph data structures
	
	uGraphTitle = "u / y="+`ytarg`+"m"
	uGraph = GraphPlot(uPlots, uGraphTitle)
	
	tiGraphTitle =  "TI / y="+`ytarg`+"m"
	tiGraph = GraphPlot(tiPlots, tiGraphTitle)

	uGraphs.append(uGraph)
	tiGraphs.append(tiGraph)



zarr=np.arange(0, 30.5, 0.5)
uarr=np.zeros(len(zarr))

for uGraph in uGraphs:
	for uPlot in uGraph.linePlots:
		for i in range(0, len(zarr)):
			if( abs(zarr[i]-uPlot.ydata[i]) < verySmall):
				    uarr[i] += uPlot.xdata[i]


ofile = open(outname, "w")

for i in range(0,len(zarr)):
        uarr[i] = uarr[i] / (len(dias)*3)

	ofile.write(`uarr[i]`+", "+`zarr[i]`+"\n")

ofile.close()


print "Written to "+outname



