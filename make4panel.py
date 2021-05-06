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
from matplotlib_toolkits.axes_grid1 import ImageGrid
from matplotlib import cm
from scipy import signal
from scipy.stats import norm
import matplotlib.mlab as mlab
import marsPA


#map1 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/contVLA-Q.I.cm.03.regrid.pbcor",
map1 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/43GHz.cont.cm",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .00005, 
         "legend" : "43 GHz", }
#map2 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/contALMA-B3-rev.I.cm.03.regrid.pbcor",
map2 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/97GHz.cont.cm",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .0002, 
         "legend" : "97 GHz", }
map3 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/B6.ms0.mfs.cm.pbcor",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .0005, 
         "legend" : "224 GHz" }
map4 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/X438c.cont.cm.pbcor",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .0016,
         "legend" : "340 GHz", }

def plotBeam( imageFile ):
    [bmaj, bmin, bpa] = marsPA.getBeam( imageFile )
    #p = subprocess.Popen( ( shlex.split('imlist in=%s units=absolute' % imageFile ) ), \
    #   stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
    #result = p.communicate()[0]
    #tmp = ori3.extractParameter( result, "bmaj", paramType="String" )
    #bmaj = float( tmp[ string.rfind(tmp, ":")+1 : ] )
    #tmp = ori3.extractParameter( result, "bmin", paramType="String" )
    #bmin = float( tmp[ string.rfind(tmp, ":")+1 : ] )
    #bpa = ori3.extractParameter( result, "bpa" )
    print "bmaj = %.4f, bmin = %.4f, bpa = %.2f" % (bmaj,bmin,bpa)
    #ell = Ellipse( (-.75*arcsecBox,-.75*arcsecBox), bmaj, bmin, angle=bpa+90., \
    #  edgecolor="m", label="beam", hatch="/", fill=False)
    #p.add_patch(ell)




mapList=[map1,map2,map3,map4]

pp = PdfPages("4panelv0.pdf")
fig = pyplot.figure( figsize=(8,11) )
ax = ImageGrid( fig, 111, nrows_ncols=(2,2), share_all=True, axes_pad=0.1)

for ipanel in range(0,4) :
    [bmaj, bmin, bpa] = marsPA.getBeam(mapList[ipanel]["image"])
    x0 = mapList[ipanel]["x0"]
    y0 = mapList[ipanel]["y0"]
    p = subprocess.Popen( ( shlex.split("imtab in=%s region=arcsec,box(%.3f,%.3f,%.3f,%.3f) \
       log=imtablog format=(3F12.5)" % (mapList[ipanel]["image"], x0+.12, y0-.12, x0-.12, y0+.12))),\
       stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
    result = p.communicate()[0]
    x,y,flx = numpy.loadtxt("imtablog", unpack=True )
    nx = len( numpy.unique( x ) )
    ny = len( numpy.unique( y ) )
    print "nx,ny = ",nx,ny
    x = x - x0
    y = y - y0
    xarr = numpy.reshape( x, (ny,nx) )
    yarr = numpy.reshape( y, (ny,nx) )
    Flx = numpy.reshape( flx, (ny,nx) )
  
    contourList = numpy.power( 1.6, [1,2,3,4,5,6,7,8,9,10,11,12] ) * mapList[ipanel]["mincontour"] 
    im = ax[ipanel].contour( xarr, yarr, Flx, contourList, origin='lower', aspect='equal', colors='black')
    contourList = -1.*contourList
    im = ax[ipanel].contour( xarr, yarr, Flx, contourList, origin='lower', aspect='equal', \
      linestyles='dotted', colors='black')
    ax[ipanel].set_xlim( x.max(), x.min() )
    ax[ipanel].set_ylim( y.min(), y.max() )
    ax[ipanel].plot( 0., 0., '+' )
    ax[ipanel].text( .95, .95, mapList[ipanel]["legend"], horizontalalignment="right", \
      verticalalignment="top", transform=ax[ipanel].transAxes )
    ell = Ellipse( (.09,-.09), bmaj, bmin, angle=bpa, \
      edgecolor="r", hatch='///', fill=False)
    ax[ipanel].add_patch(ell)

    ax[ipanel].set_xlabel( 'arcsec' )
    ax[ipanel].set_ylabel( 'arcsec' )


pyplot.savefig( pp, format='pdf' )
pp.close()
pyplot.show()  
