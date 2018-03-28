from pylab import * 
from numpy import *
from astropy.io import fits
import os

import Epoch_06_1_14_Normalization
import Epoch_06_12_14_Normalization
import Epoch_06_28_14_Normalization
import Epoch_06_14_15_Normalization


Epoch_num=3
EPOCH_LIST=[Epoch_06_1_14_Normalization,
            Epoch_06_12_14_Normalization,
            Epoch_06_28_14_Normalization,
            Epoch_06_14_15_Normalization]

EPOCH=EPOCH_LIST[Epoch_num]

FILENAME_LIST=['Epoch_06_1_14','Epoch_06_12_14','Epoch_06_28_14','Epoch_06_14_15']
FILENAME=FILENAME_LIST[Epoch_num]

xdata=EPOCH.Final_x_spectrum
ydata=EPOCH.Final_y_spectrum
edata=EPOCH.Final_e_spectrum

col1=fits.Column(name='wavelength',format='D',array=xdata)
col2=fits.Column(name='flux'      ,format='D',array=ydata)
col3=fits.Column(name='error'     ,format='D',array=edata)
cols = fits.ColDefs([col1, col2, col3])
tbhdu = fits.BinTableHDU.from_columns(cols)
tbhdu.writeto(FILENAME+'.fits')