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


import Epoch_06_1_14_Normalization
import Epoch_06_12_14_Normalization
import Epoch_06_28_14_Normalization
import Epoch_06_14_15_Normalization


plt.figure(1)
plt.title('Normalized Epoch 6/1/14, 6/12/14, 6/28/14 and 6/14/15  ')
plt.xlabel(r'Observed Wavelength ($\AA$)')
plt.ylabel('Flux (erg/s/cm^2/$\AA$)')
plt.axhline(y=1,color='orange')
plt.plot(Epoch_06_1_14_Normalization.Final_x_spectrum,Epoch_06_1_14_Normalization.Final_y_spectrum,zorder=0)
plt.plot(Epoch_06_12_14_Normalization.Final_x_spectrum,Epoch_06_12_14_Normalization.Final_y_spectrum,zorder=0)
plt.plot(Epoch_06_28_14_Normalization.Final_x_spectrum,Epoch_06_28_14_Normalization.Final_y_spectrum,zorder=0)
plt.plot(Epoch_06_14_15_Normalization.Final_x_spectrum,Epoch_06_14_15_Normalization.Final_y_spectrum,zorder=0)
Epoch_06_1_14 = mpatches.Patch(color='blue', label='Epoch_06_1_14')
Epoch_06_12_14=mpatches.Patch(color='orange', label='Epoch_06_12_14')
Epoch_06_28_14=mpatches.Patch(color='green', label='Epoch_06_28_14')
Epoch_06_14_15=mpatches.Patch(color='red', label='Epoch_06_14_15')
plt.legend(handles=[Epoch_06_1_14,Epoch_06_12_14,Epoch_06_28_14,Epoch_06_14_15])
plt.axis([1400,1450,0,3])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(13.5, 10.5)