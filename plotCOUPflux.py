# plotCOUPflux.py
# simple version of plotBNflux

import math
import numpy
import string
import matplotlib
# matplotlib.use('GTKAgg')
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages

def fitData( fGHz, flux, err, fnew ) :
    x = numpy.log(fGHz)
    y = numpy.log(flux)
    deg = 1    # linear fit
    pcoeff = numpy.polyfit( x, y, deg )
    print pcoeff
    x2 = numpy.log(fnew)
    fluxfit = numpy.exp( numpy.polyval( pcoeff, x2 ) )
    return fluxfit

def plotFluxes() :
  # read data from csv file (downloaded from Google Drive)
    infile = "COUPflux.dat"
    fGHz,contFlux,err = numpy.genfromtxt( infile, unpack=True )
    print fGHz
    print contFlux
    print err
  # fit the data
    f = numpy.arange( 30.,500.,10.)
    fluxfit = fitData( fGHz[1:], contFlux[1:], err, f )

  # open the figure
    pp = PdfPages("COUPflux.pdf")
    #fig = pyplot.figure( figsize=(11,8) )
    fig = pyplot.figure( figsize=(8,8) )
    ax = fig.add_subplot( 111 )
    ax.set_xlim( 30, 500. )
    ax.set_ylim( 0.01, 100. )

    ax.plot( fGHz, contFlux, 'o' )
    for n in range(0,len(fGHz)):
      ax.errorbar( fGHz[n], contFlux[n], yerr=err[n], marker='o', \
         markersize=14, color='red', elinewidth=2)
    ax.plot( f, fluxfit, '--', linewidth=2, color='blue' )
    pyplot.text( 36.,40., 'COUP 0599a', fontsize=22)
    pyplot.text( 160.,1.2, r'S$\sim\nu^3$', fontsize=26, color='blue')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel( 'frequency (GHz)', size=18 )
    ax.set_ylabel( 'integrated flux density (mJy)', size=18 )
    ax.tick_params( which='both', length=6, labelsize=18 )
    pyplot.grid(True)

    pyplot.savefig( pp, format='pdf' )
    pp.close()
    pyplot.show()  

plotFluxes()
    
