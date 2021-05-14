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
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib import cm
from scipy import signal
from scipy.stats import norm
import matplotlib.mlab as mlab
import marsPA
import ori3

map01 = { "image" : "contVLA-Q.I.cm.03.regrid.pbcor",}

#map1 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/43GHzmfs.rob-1.cm.pbcor",
#map1 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/43GHzwide.imsub.cm.regrid",

map1 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/43GHz.cont.cm",
        "x0" : -6.05,
        "y0" : 7.92,
        "mincontour" : .00005, 
        "legend" : "43 GHz", 
        "pklfile" : "43GHz.pkl" }

map02 = { "image" : "contALMA-B3-rev.I.cm.03.regrid.pbcor",}

map2 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/97GHz.cont.cm",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .0002, 
         "legend" : "97 GHz", 
         "pklfile" : "97GHz.pkl" }

map3 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/B6.ms0.mfs.cm.pbcor",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .0005, 
         "legend" : "223 GHz",
         "pklfile" : "223GHz.pkl" }

map4 = { "image" : "/o/plambeck/OriALMA/BNpaper/ContImages/X438c.cont.cm.pbcor",
         "x0" : -6.05,
         "y0" : 7.92,
         "mincontour" : .0016,
         "legend" : "340 GHz", 
         "pklfile" : "340GHz.pkl" }

#mapList=[map01,map1,map02,map2,map3,map4]
mapList=[map1,map2,map3,map4]

# ---------------------------------------------------------------------------------- #
# dump out map center and frequency, to make sure all are consistent
# ---------------------------------------------------------------------------------- #
def sanityCheck( mapList ):
    for mp in mapList :
      p = subprocess.Popen( ( shlex.split('imlist in=%s' % mp["image"] ) ), \
         stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
      result = p.communicate()[0]
      ra = ori3.extractParameter( result, "crval1", paramType="String" )
      dec = ori3.extractParameter( result, "crval2", paramType="String" )
      frq = ori3.extractParameter( result, "crval3", paramType="String" )
      print ra,dec,frq,mp["image"] 

#sanityCheck( mapList)

def getKperJy( map ):
    p = subprocess.Popen( ( shlex.split('imlist in=%s options=stat' % map ) ), \
       stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
    result = p.communicate()[0]
    n = result.find("K/Jy:")
    a = result[n:].split()
    KperJy = float(a[1])
    print "K/Jy = ", KperJy
    return KperJy

# ---------------------------------------------------------------------------------- #
# convert image to a numpy array, dump it and synthesized beam to a pickle file that
#    I can use to work on the images on my laptop, without Miriad
# ---------------------------------------------------------------------------------- #

def dumpImages( mapList ) :
    for ipanel in range(0,4) :
      [bmaj, bmin, bpa] = marsPA.getBeam(mapList[ipanel]["image"])
      KperJy = getKperJy( mapList[ipanel]["image"] )
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
      Tbarr = KperJy * numpy.reshape( flx, (ny,nx) )
      print "max Tb = ", Tbarr.max()
      obsImage = { "bmaj" : bmaj, "bmin" : bmin, "bpa" : bpa, "KperJy" : KperJy, \
         "xarr" : xarr, "yarr" : yarr, "Tbarr" : Tbarr }
      fout = open( mapList[ipanel]["pklfile"], 'wb' )
      pickle.dump( obsImage, fout )
      fout.close()

#dumpImages( mapList )

pp = PdfPages("4panel.pdf")
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
    KperJy = getKperJy( mapList[ipanel]["image"] )
    Flx = numpy.reshape( flx, (ny,nx) )
    Tbarr = KperJy * numpy.reshape( flx, (ny,nx) )
  
    # use for Jy/beam contours
    contourList = numpy.power( 1.6, [1,2,3,4,5,6,7,8,9,10,11,12] ) * mapList[ipanel]["mincontour"] 
    im = ax[ipanel].contour( xarr, yarr, Flx, contourList, origin='lower', aspect='equal', colors='black')

    # usedfor Tb contours
    # contourList = numpy.power( 1.6, [1,2,3,4,5,6,7,8,9,10,11,12] ) * 35.
    # im = ax[ipanel].contour( xarr, yarr, Tbarr, contourList, origin='lower', aspect='equal', colors='black')
    
    contourList = -1.*contourList
    im = ax[ipanel].contour( xarr, yarr, Flx, contourList, origin='lower', aspect='equal', \
      linestyles='dotted', colors='black')
    #im = ax[ipanel].contour( xarr, yarr, Tbarr, contourList, origin='lower', aspect='equal', \

    ax[ipanel].set_xlim( x.max(), x.min() )
    ax[ipanel].set_ylim( y.min(), y.max() )
    ax[ipanel].plot( 0., 0., '+' )
    ax[ipanel].text( .95, .95, mapList[ipanel]["legend"], horizontalalignment="right", \
      verticalalignment="top", transform=ax[ipanel].transAxes )
    ell = Ellipse( (.09,-.09), bmaj, bmin, angle=bpa, \
      edgecolor="r", hatch='///', fill=False)
    ax[ipanel].add_patch(ell)

    ax[ipanel].set_xlabel( '$\Delta$RA arcsec' )
    ax[ipanel].set_ylabel( '$\Delta$DEC arcsec' )


pyplot.show()  
pyplot.savefig( pp, format='pdf' )
pp.close()
