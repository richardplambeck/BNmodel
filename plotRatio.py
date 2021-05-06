import math
import numpy
import string
import matplotlib
# matplotlib.use('GTKAgg')
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
from matplotlib.backends.backend_pdf import PdfPages

def plotRatio() :
    infile = "BN_SrcI_ratio.dat"

  # open the figure
    pp = PdfPages("Fluxratio.pdf")
    fig = pyplot.figure( figsize=(11,8) )
    ax = fig.add_subplot( 111 )
    # ax.set_xlim( 3., 500. )
    ax.set_ylim( 0., 3. )

    frange = [ [40.,45.], [80,100], [200,250] ]
    color = [ 'b','g','r' ]
    epoch,fGHz,BNflx,Iflx = numpy.loadtxt( infile, unpack=True)
    for fr, col in zip( frange, color ) :
      yr = []
      ratio = []
      for y,f,B,I in zip( epoch, fGHz, BNflx, Iflx ) :
        if f > fr[0] and f< fr[1] :
          yr.append(y)
          ratio.append( B/I )
      print f, numpy.average(ratio)
      ax.plot( yr, ratio/numpy.average(ratio), 'o--', markersize=14, color=col )

    # ax.errorbar( data["f_GHz"][n], data["flux_mJy"][n], yerr=data["unc"][n], 
    #   marker=data["marker"][n], markersize=data["markersize"][n], color=data["color"][n],
    #   markeredgecolor='k', elinewidth=1.5, capthick=1.5, alpha=0.7 )

    ax.set_xlabel( 'epoch', size=14 )
    ax.set_ylabel( 'S(BN)/S(SrcI)', size=14 )
    ax.tick_params( which='both', length=6, labelsize=14 )
    pyplot.grid(True)

    pyplot.savefig( pp, format='pdf' )
    pp.close()
    pyplot.show()  

plotRatio()
