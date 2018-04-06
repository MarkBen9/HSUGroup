import os
from pylab import * 
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline
from astropy.io import fits
from PIL import Image
from numpy import *
from numpy import concatenate
from numpy import interp
from numpy import set_printoptions
from numpy import arange 
from numpy import nan
from numpy import polyval
from numpy import polyfit
from numpy import sqrt
from numpy import ones
from numpy import convolve
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('dark_background')
#------------------------------------------------------------------------------
#Initializing
Epoch_06_1_14=fits.open('../Data/Epoch_06_1_14.fits')
Epoch_06_1_14_DATA=Epoch_06_1_14[1].data
Epoch_06_1_14.close()

Epoch_06_1_14_WAVE=Epoch_06_1_14_DATA['wavelength']
Epoch_06_1_14_FLUX=Epoch_06_1_14_DATA['flux']
Epoch_06_1_14_ERROR=Epoch_06_1_14_DATA['error']
#------------------------------------------------------------------------------
#Functions and operations
#give this function some data and a range and it spits out the average x and y
def make_polyfit_point(xlist,ylist,start,end):
    x_ave=closest_value(xlist,(start+end)/2)
    start_index=find_index(xlist,closest_value(xlist,start))
    end_index=find_index(xlist,closest_value(xlist,end))
    y_sum=0
    for i in range(start_index,end_index,1):
        y_sum+=ylist[i]
    y_ave=closest_value(ylist,y_sum/(end_index-start_index))       
    return [x_ave,y_ave]
#this finds the INDEX of the element of the list CLOSEST to what you put in.
def find_index(your_list,your_value):
    x_1=list(your_list)
    return(x_1.index(min(x_1, key=lambda x:abs(x-your_value))))
# this returns the VALUE of the element of the list CLOSEST to what you put in.
def closest_value(your_list,value):
    return(your_list[find_index(your_list,value)])
#------------------------------------------------------------------------------
#Si
PreNormalizedSI_FX=Epoch_06_1_14_FLUX[find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1450)):find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1490))]
Si_Spect_WL=arange(1450,1490,0.012234810431436927)

Sil_Polyfit_Point1=[make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1467.5,1469),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1474,1475),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1478.3,1480),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1483,1484),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1486,1487)]
x_poly_1=[item[0]for item in Sil_Polyfit_Point1]
y_poly_1=[item[1]for item in Sil_Polyfit_Point1]
best_fit_poly_1=(polyfit(x_poly_1,y_poly_1,2))

Sil_Polyfit_Point2=[make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1461,1462),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1462.8,1463.2),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1464.5,1465.5)]
x_poly_2=[item[0]for item in Sil_Polyfit_Point2]
y_poly_2=[item[1]for item in Sil_Polyfit_Point2]
best_fit_poly_2=(polyfit(x_poly_2,y_poly_2,2))
#------------------------------------------------------------------------------
"""
#for ploting example
xping=arange(Epoch_06_1_14_WAVE[0],Epoch_06_1_14_WAVE[-1],.05)
yping=[]
for i in range(len(xping)):
   yping.append(best_fit_poly_1[0]*(xping[i])**2+best_fit_poly_1[1]*(xping[i])+ best_fit_poly_1[2])
   #for ploting example
yping2=[]
for i in range(len(xping)):
   yping2.append(best_fit_poly_2[0]*(xping[i])**2+best_fit_poly_2[1]*(xping[i])+ best_fit_poly_2[2])
"""

Si_Spect_FX=[]
Si_Spect_WL=arange(1450,1490,0.012234810431436927)
for i in range(0,find_index(Si_Spect_WL,closest_value(Si_Spect_WL,1461.8038))):
    #First part First order poly
    Si_Spect_FX.append(PreNormalizedSI_FX[i])
for i in range(find_index(Si_Spect_WL,closest_value(Si_Spect_WL,1461.8038)),find_index(Si_Spect_WL,closest_value(Si_Spect_WL,1464.2742))):
    #First part First order poly
    Si_Spect_FX.append((PreNormalizedSI_FX[i])/(best_fit_poly_2[0]*(Si_Spect_WL[i])**2+ best_fit_poly_2[1]*(Si_Spect_WL[i])+best_fit_poly_2[2]))
for i in range(find_index(Si_Spect_WL,closest_value(Si_Spect_WL,1464.2742)),find_index(Si_Spect_WL,closest_value(Si_Spect_WL,1467.6059))):
    #First part First order poly
    Si_Spect_FX.append(PreNormalizedSI_FX[i])
for i in range(find_index(Si_Spect_WL,closest_value(Si_Spect_WL,1467.6059)),len(Si_Spect_WL)):
    #First part First order poly
    Si_Spect_FX.append((PreNormalizedSI_FX[i])/(best_fit_poly_1[0]*(Si_Spect_WL[i])**2+ best_fit_poly_1[1]*(Si_Spect_WL[i])+best_fit_poly_1[2]))
#------------------------------------------------------------------------------
    #Carbon
    
PreNormalizedCIV_FX=Epoch_06_1_14_FLUX[find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1600)):find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1680))]
CIV_Spect_WL=arange(1600,1680,0.012234810431436927)

#nEED to create more points
CIV_Polyfit_Points=[make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1637.6,1637.9),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1639.6,1640.1),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1643.7,1643.9),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1648,1649)]

x_poly_1=[item[0]for item in CIV_Polyfit_Points]
y_poly_1=[item[1]for item in CIV_Polyfit_Points]
#splinesInt is a function i.e. f(x_wavelength)
splinesInt=interp1d(x_poly_1,y_poly_1,kind = 'cubic', bounds_error = False)

#for Graphical purposes, and plotting only, Has no coding
xping=arange(Epoch_06_1_14_WAVE[0],Epoch_06_1_14_WAVE[-1],.05)


CIV_Spect_FX=[]
CIV_Spect_WL=arange(1615,1650,0.012234810431436927)
#Will be changed soon to spline method
"""
for i in range(0,find_index(CIV_Spect_WL,closest_value(CIV_Spect_WL,1636.23))):
    #First part First order poly
    CIV_Spect_FX.append(Epoch_06_1_14_FLUX[find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1615))+i])
for i in range(find_index(CIV_Spect_WL,closest_value(CIV_Spect_WL,1636.23)),len(CIV_Spect_WL)):
    #First part First order poly
    CIV_Spect_FX.append((Epoch_06_1_14_FLUX[find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1615))+i])/(best_fit_poly_1[0]*(CIV_Spect_WL[i])**2+ best_fit_poly_1[1]*(CIV_Spect_WL[i])+best_fit_poly_1[2]))
    """