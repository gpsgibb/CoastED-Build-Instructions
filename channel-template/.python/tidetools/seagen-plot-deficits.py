#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pylab as pb
import math
import sys
from operator import itemgetter
import seagenaverageu as uprof

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
    print "usage: seagen-plot-deficits.py <csv file> [out file.jpg|.png|.ps|.pdf]"
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


fig, axarr = plt.subplots(nrows=3, ncols=2)
plt.subplots_adjust(left=0.05, right=0.975, hspace=0.5, wspace=None )

fig.set_figwidth(14)
fig.set_figheight(8)


yarr=[87, 100, 113]
zarr=[8, 16, 24]

# Each y is one row of plots

uGraphs=[]
tiGraphs=[]

for ytarg in yarr:
	
	uPlots=[]
	tiPlots=[]
	
	# collect line plot data for this row
	for ztarg in zarr:

		dData = []
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
			if(abs(y-ytarg) < verySmall and abs(z-ztarg) < verySmall):
				dData.append(D)
				uData.append(umag)
				tiData.append(ti)
			
	
		dData, uData, tiData= reorderToX(dData, uData, tiData)
		plotLegend = "z="+`ztarg`

		uPlot  = LinePlot(plotLegend, dData,  uData)
		tiPlot = LinePlot(plotLegend, dData, tiData)

		uPlots.append(uPlot)
		tiPlots.append(tiPlot)

	
	# We now have ordered data for this pair of plots on a row. 
	# Shove into graph data structures
	
	uGraphTitle = "u at y="+`ytarg`+" m"
	uGraph = GraphPlot(uPlots, uGraphTitle)
	
	tiGraphTitle =  "TI at y="+`ytarg`+" m"
	tiGraph = GraphPlot(tiPlots, tiGraphTitle)

	uGraphs.append(uGraph)
	tiGraphs.append(tiGraph)


for j in range(0,3):

    uGraph=uGraphs[j]
    tiGraph=tiGraphs[j]

    for i in range(0,3):
        uPlot = uGraph.linePlots[i]

        p1, = axarr[j][0].plot(uPlot.xdata, uPlot.ydata, label=uPlot.name)


    axarr[j][0].set_title(uGraph.title)
    axarr[j][0].set_xlim([-2,40])
    axarr[j][0].set_ylim([0,2.5])
    axarr[j][0].grid(True)

    axarr[j][0].legend(loc=0, prop={'size':10})

    axarr[j][0].set_xlabel("x (D)")
    axarr[j][0].set_ylabel("u_av (m/s)")


    for i in range(0,3):
        tiPlot = tiGraph.linePlots[i]

        p1, = axarr[j][1].plot(tiPlot.xdata, tiPlot.ydata, label=tiPlot.name)


    axarr[j][1].set_title(tiGraph.title)
    axarr[j][1].set_xlim([-2,40])
#    axarr[j][1].set_ylim([0,0.15])
    axarr[j][1].set_ylim(bottom=0)
    axarr[j][1].set_xlabel("x (D)")
    axarr[j][1].set_ylabel("T.I.")

    axarr[j][1].legend(loc=0, prop={'size':10})
    axarr[j][1].grid(True)



if(outname==""):
    plt.show()
else:
    plt.savefig(outname, dpi=150)

    print "Written to "+outname


