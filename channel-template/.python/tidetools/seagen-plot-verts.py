#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pylab as pb
import math
import sys
import seagenaverageu as uprof

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

if len(sys.argv)<2:
    print "usage: seagen-plot-verts.py <csv file> [out file.jpg|.png|.ps|.pdf]"
    exit(1)

if len(sys.argv)<3:
    outname=""
else:
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


fig, axarr = plt.subplots(nrows=1, ncols=6, sharey=True)
plt.subplots_adjust(left=0.05, right=0.975, hspace=0.5, wspace=None )

fig.set_figwidth(16)
fig.set_figheight(9)

yarr=[87, 100, 113]

# Each y is one row of plots

dias= [ -5, -2, -1, 0, 1, 2, 3, 5, 10, 20, 40 ]

uGraphs=[]
tiGraphs=[]

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

			depth=30.0
			dz=depth/(1.0*(len(uprof.z)-1))
			u0 = uprof.u[int(z/dz)]

			
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



fct=0

for j in range(0,3):

	uGraph = uGraphs[j]

	for i in range(0,len(dias)):
		uPlot = uGraph.linePlots[i]
		axarr[fct].plot( uPlot.xdata, uPlot.ydata, \
                              label=uPlot.name )

	axarr[fct].set_title(uGraph.title)
	axarr[fct].set_xlim([0,2.5])
	axarr[fct].set_ylim([0,30])
	axarr[fct].grid(True)

	axarr[fct].legend(loc=0, prop={'size':10})

	axarr[fct].set_xlabel("u_av (m/s)")
	axarr[fct].set_ylabel("z (m)")


	fct=fct+1


for j in range(0,3):

	tiGraph = tiGraphs[j]

	for i in range(0,len(dias)):
		tiPlot = tiGraph.linePlots[i]
		axarr[fct].plot( tiPlot.xdata, tiPlot.ydata, \
                              label=tiPlot.name )

	axarr[fct].set_title(tiGraph.title)
	axarr[fct].set_xlim(left=0)
	axarr[fct].set_ylim([0,30])
	axarr[fct].grid(True)

	axarr[fct].legend(loc=0, prop={'size':10})

	axarr[fct].set_xlabel("TI")
	axarr[fct].set_ylabel("z (m)")

	xstart, xend = axarr[fct].get_xlim()

	if(xend>0.3):
		interval=0.1
	elif(xend <= 0.3):
		interval=0.05
	elif(xend <=0.15):
		interval=0.02

	axarr[fct].set_xticks(np.arange(0, xend, interval))

	fct=fct+1


if(outname==""):
	plt.show()
else:
	plt.savefig(outname, dpi=150)

	print "Written to "+outname



