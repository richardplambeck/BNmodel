# plotBNflux.py
# work from csv table downloaded from Google Drive

import math
import numpy
import string
import matplotlib
# matplotlib.use('GTKAgg')
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages

# get rough spectral index of our new data
def fitData( fnew ) :
    infile = "BN - FluxTable.csv"
    data = numpy.genfromtxt( infile, dtype=None, delimiter=",", names=True)
    fGHz = []
    flux = []
    w = []
    for n in range(0,len(data)) :
      #if data["color"][n] == "r" :      # use only more recent data
      if data["f_GHz"][n] < 150. and data["unc"][n] > 0. :       # use only continuum data < 150 GHz
        fGHz.append( data["f_GHz"][n] )
        flux.append( data["flux_mJy"][n] )
        w.append( data["flux_mJy"][n]/data["unc"][n] )
           # d(log(S)) = 1/S * ds; W = 1/d(log(S))
        print "%6.2f  %6.2f  %6.2f" % (fGHz[-1],flux[-1],data["unc"][n])
    x = numpy.log(fGHz)
    y = numpy.log(flux)
    deg = 1    # linear fit
    pcoeff,V = numpy.polyfit( x, y, deg, w=w, cov=True)
    beta = pcoeff[0]
    uncBeta = math.sqrt( V[0][0] )
    print "spectral index = %.3f (%.3f)" % (beta,uncBeta)
    print "electron density index = %.3f (%.3f to %.3f)" % \
      (epowlaw(beta), epowlaw(beta-uncBeta), epowlaw(beta+uncBeta))
    x2 = numpy.log(fnew)
    fluxfit = numpy.exp( numpy.polyval( pcoeff, x2 ) )
    return fluxfit

# solve for electron density vs radius given the spectral index beta, given on p. 47 
#   of Wright and Barlow 1975
def epowlaw( beta ):
    return (beta-6.2)/(2.*beta - 4.)

#print epowlaw(1.26) 

def plotFluxes( datafile, modelfile ) :

  # read data from csv file (downloaded from Google Drive)
    # infile = "BN - IntegratedFluxes.csv"
    data = numpy.genfromtxt( datafile, dtype=None, delimiter=",", names=True)

  # open the figure
    pp = PdfPages("BNfluxes.pdf")
    fig = pyplot.figure( figsize=(11,8) )
    #fig = pyplot.figure( figsize=(8,8) )
    ax = fig.add_subplot( 111 )
    ax.set_xlim( 3., 500. )
    # ax.set_xlim( 30., 800. )
    ax.set_ylim( 1., 2000. )
    # ax.set_ylim( 10., 2000. )

  # plot models first so points will lie above them
    #infile = "BNmodel_1.radialModel"
    fGHz,contFlux,lineFlux = numpy.loadtxt( modelfile, usecols=(0,2,4), unpack=True)
    #ax.plot( fGHz, contFlux )
    #ax.plot( fGHz, lineFlux, "--" )
    fnew = numpy.arange(1,1000,100.)
    ax.plot( fnew, fitData( fnew ), color="red" )
    

  # plot points one at a time because errorbar doesn't allow array of symbols or colors
    for n in range(0, len(data)) :
      ax.errorbar( data["f_GHz"][n], data["flux_mJy"][n], yerr=data["unc"][n], 
        marker=data["marker"][n], markersize=data["markersize"][n], color=data["color"][n],
        markeredgecolor='k', elinewidth=1.5, capthick=1.5, alpha=0.7 )

    # annotate recomb lines, indicated by alpha or beta in data["ref"]
      if "alpha" in data["text"][n] or "beta" in data["text"][n]  :
        print data["text"][n]
        ax.annotate( data["text"][n], (data["f_GHz"][n],data["flux_mJy"][n]), \
           xytext=(data["xoff"][n],data["yoff"][n]), textcoords='offset points', 
           color=data["color"][n] )

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel( 'frequency (GHz)', size=14 )
    ax.set_ylabel( 'integrated flux density (mJy)', size=14 )
    ax.tick_params( which='both', length=6, labelsize=14 )
    pyplot.grid(True)

    pyplot.savefig( pp, format='pdf' )
    pp.close()
    pyplot.show()  

    
def getAlpha( f1, S1, f2, S2 ):
    alpha = math.log(S2/S1)/math.log(f2/f1)
    print f1, S1, f2, S2, alpha

plotFluxes( "Users/plambeck/BN/FluxPlot/BN - FluxTable.csv", "Users/plambeck/BN/FluxPlot/BNmodel_1.radialModel" )
#getAlpha( 85.85, 68.42, 97., 75.01 )
#getAlpha( 87.34, 66.71, 99.36, 82.16 )
