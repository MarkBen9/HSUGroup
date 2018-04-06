from pylab import * 
from numpy import *
from astropy.io import fits
from PIL import Image
from numpy import concatenate
from numpy import interp
from numpy import set_printoptions
from numpy import arange 
from numpy import nan
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mtick
from numpy import sqrt
from numpy import ones
from numpy import convolve
import matplotlib.patches as mpatches
from numpy import polyfit
from numpy import polyval
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.style as style
from astropy.io import fits
style.use('dark_background')
#------------------------------------------------------------------------------
Epoch_06_1_14=fits.open('../Data/Epoch_06_1_14.fits')
Epoch_06_1_14_DATA=Epoch_06_1_14[1].data
Epoch_06_1_14.close()

Epoch_06_12_14=fits.open('../Data/Epoch_06_12_14.fits')
Epoch_06_12_14_DATA=Epoch_06_12_14[1].data
Epoch_06_12_14.close()

Epoch_06_28_14=fits.open('../Data/Epoch_06_28_14.fits')
Epoch_06_28_14_DATA=Epoch_06_28_14[1].data
Epoch_06_28_14.close()

Epoch_06_14_15=fits.open('../Data/Epoch_06_14_15.fits')
Epoch_06_14_15_DATA=Epoch_06_14_15[1].data
Epoch_06_14_15.close()
#------------------------------------------------------------------------------
Epoch_06_1_14_WAVE=Epoch_06_1_14_DATA['wavelength']
Epoch_06_1_14_FLUX=Epoch_06_1_14_DATA['flux']
Epoch_06_1_14_ERROR=Epoch_06_1_14_DATA['error']

Epoch_06_12_14_WAVE=Epoch_06_12_14_DATA['wavelength']
Epoch_06_12_14_FLUX=Epoch_06_12_14_DATA['flux']
Epoch_06_12_14_ERROR=Epoch_06_12_14_DATA['error']

Epoch_06_28_14_WAVE=Epoch_06_28_14_DATA['wavelength']
Epoch_06_28_14_FLUX=Epoch_06_28_14_DATA['flux']
Epoch_06_28_14_ERROR=Epoch_06_28_14_DATA['error']

Epoch_06_14_15_WAVE=Epoch_06_14_15_DATA['wavelength']
Epoch_06_14_15_FLUX=Epoch_06_14_15_DATA['flux']
Epoch_06_14_15_ERROR=Epoch_06_14_15_DATA['error']
#------------------------------------------------------------------------------
plt.plot(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,zorder=0,c='red',linewidth=1)
plt.plot(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,zorder=0,c='green',linewidth=1)
plt.plot(Epoch_06_28_14_WAVE,Epoch_06_28_14_FLUX,zorder=0,c='blue',linewidth=1)
plt.plot(Epoch_06_14_15_WAVE,Epoch_06_14_15_FLUX,zorder=0,c='white',linewidth=1)