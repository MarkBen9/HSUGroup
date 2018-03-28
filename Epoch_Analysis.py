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

import Epoch_06_1_14_Normalization
import Epoch_06_12_14_Normalization
import Epoch_06_28_14_Normalization
import Epoch_06_14_15_Normalization

EPOCH_LIST=[Epoch_06_1_14_Normalization,
            Epoch_06_12_14_Normalization,
            Epoch_06_28_14_Normalization,
            Epoch_06_14_15_Normalization]

EPOCH=EPOCH_LIST[1]

plt.figure(1)
plt.title(' ')
plt.xlabel(r'Observed Wavelength ($\AA$)')
plt.ylabel('Flux (erg/s/cm^2/$\AA$)')
plt.axhline(y=1,color='grey')

plt.plot(EPOCH.TWL1,EPOCH.Normal_TFS1,zorder=0,c='magenta',linewidth=1)
plt.plot(EPOCH.TWL2,EPOCH.Normal_TFS2,zorder=0,c='blue',linewidth=1)
plt.plot(EPOCH.TWL3,EPOCH.Normal_TFS3,zorder=0,c='red',linewidth=1)

EPOCH=EPOCH_LIST[0]
plt.plot(EPOCH.Final_x_spectrum,EPOCH.Final_y_spectrum,zorder=0,c='red',linewidth=2)
#EPOCH=EPOCH_LIST[1]
#plt.plot(EPOCH.Final_x_spectrum,EPOCH.Final_y_spectrum,zorder=0,c='green',linewidth=2)
#EPOCH=EPOCH_LIST[2]
#plt.plot(EPOCH.Final_x_spectrum,EPOCH.Final_y_spectrum,zorder=0,c='blue',linewidth=2)
#EPOCH=EPOCH_LIST[3]
#plt.plot(EPOCH.Final_x_spectrum,EPOCH.Final_y_spectrum,zorder=0,c='magenta',linewidth=2)

Grating1050=mpatches.Patch(color='magenta', label='Grating 1050')
Grating1319=mpatches.Patch(color='blue', label='Grating 1319')
Grating1572=mpatches.Patch(color='red', label='Grating 1572')
Full_Spectrum=mpatches.Patch(color='green',label='Full Spectrum')
plt.legend(handles=[Grating1050,Grating1319,Grating1572,Full_Spectrum])
plt.axis([1000,1800,0,3])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(13.5, 10.5)



    


    
