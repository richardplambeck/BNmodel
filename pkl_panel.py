# pkl_panel.py
# reads pkl files with map info, makes 4 panel figure from them
# for use on my laptop without miriad

import math
import time
import datetime
import dateutil.parser
import cmath
import numpy
import sys
import pickle
import subprocess
import shlex
import string
import random
import matplotlib
import os
#matplotlib.use('GTKAgg')
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle
# from matplotlib_toolkits.axes_grid1 import ImageGrid
from matplotlib import cm
from scipy import signal
from scipy.stats import norm
import matplotlib.mlab as mlab
# import marsPA


pickleFileList = ["43GHz.pkl","97GHz.pkl","224GHz.pkl","340GHz.pkl"]
pp = PdfPages("4panel.pdf")
#fig = pyplot.figure( figsize=(8,11) )
#ax = ImageGrid( fig, 111, nrows_ncols=(2,2), share_all=True, axes_pad=0.1)
fig,ax = pyplot.subplots(2,2)
contourList = numpy.arange(200.,10000.,200.)
contourList = numpy.array( (10., 50., 100., 1000., 3000., 5000., 7000.))

for ipanel in range(0,2) :
  for jpanel in range(0,2) :
    pickleFile = pickleFileList[2*ipanel+jpanel]
    fin = open( "../ContImages/"+pickleFile, "r" )
    obsImage = pickle.load( fin )
    im = ax[ipanel,jpanel].contour( obsImage["xarr"], obsImage["yarr"], obsImage["Tbarr"], \
       contourList, origin='lower', aspect='equal', colors='black')
    contourList = -1.*contourList
    im = ax[ipanel,jpanel].contour( obsImage["xarr"], obsImage["yarr"], obsImage["Tbarr"], \
       contourList, origin='lower', aspect='equal', linestyles='dotted', colors='black')
    contourList = -1.*contourList
    ax[ipanel,jpanel].set_xlim( obsImage["xarr"].max(), obsImage["xarr"].min() )
    ax[ipanel,jpanel].set_ylim( obsImage["yarr"].min(), obsImage["yarr"].max() )
    ax[ipanel,jpanel].plot( 0., 0., '+' )
    ax[ipanel,jpanel].text( .95, .95, pickleFile, horizontalalignment="right", \
      verticalalignment="top", transform=ax[ipanel,jpanel].transAxes )
    ell = Ellipse( (.09,-.09), obsImage["bmaj"], obsImage["bmin"], angle=obsImage["bpa"], \
      edgecolor="r", hatch='///', fill=False)
    ax[ipanel,jpanel].add_patch(ell)

    ax[ipanel,jpanel].set_xlabel( 'arcsec' )
    ax[ipanel,jpanel].set_ylabel( 'arcsec' )

#pyplot.savefig( pp, format='pdf' )
#pp.close()
pyplot.show()  
