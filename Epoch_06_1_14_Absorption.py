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
#PV SECTION
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#SiIV SECTION
#------------------------------------------------------------------------------
Sil_Polyfit_Point1=[make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1470.6,1471.1),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1474,1475),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1478.3,1480),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1483,1484),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1486,1487),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1488,1488.5)]

Sil_Polyfit_Point2=[make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1452.9,1453.8),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1461,1462)
                    ,make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1464.9,1465.2)]
#------------------------------------------------------------------------------
x_poly_1_SiIV=[item[0]for item in Sil_Polyfit_Point1]
y_poly_1_SiIV=[item[1]for item in Sil_Polyfit_Point1]
x_poly_2_SiIV=[item[0]for item in Sil_Polyfit_Point2]
y_poly_2_SiIV=[item[1]for item in Sil_Polyfit_Point2]

best_fit_poly_1=(polyfit(x_poly_1_SiIV,y_poly_1_SiIV,2))
best_fit_poly_2=(polyfit(x_poly_2_SiIV,y_poly_2_SiIV,1))
#------------------------------------------------------------------------------
PreNormalizedSI_FX=Epoch_06_1_14_FLUX[find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1450)):1+find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1490))]
Si_Spect_FX_1=[]
Si_Spect_WL_1=arange(1450,1490,0.012234810431436927)
#------------------------------------------------------------------------------
for i in range(0,find_index(Si_Spect_WL_1,closest_value(Si_Spect_WL_1,1465.5))):
    #First part First order poly
    Si_Spect_FX_1.append(PreNormalizedSI_FX[i]/(best_fit_poly_2[0]*(Si_Spect_WL_1[i])+best_fit_poly_2[1]))
for i in range(find_index(Si_Spect_WL_1,closest_value(Si_Spect_WL_1,1465.5)),len(Si_Spect_WL_1)):
    #Second part Second order poly
    Si_Spect_FX_1.append((PreNormalizedSI_FX[i])/(best_fit_poly_1[0]*(Si_Spect_WL_1[i])**2+ best_fit_poly_1[1]*(Si_Spect_WL_1[i])+best_fit_poly_1[2]))

#------------------------------------------------------------------------------
"""
xping=arange(Si_Spect_WL_1[0],Si_Spect_WL_1[-1],.05)
yping=[]
for i in range(len(xping)):
   yping.append(best_fit_poly_2[0]*(xping[i])+ best_fit_poly_2[1])
y2ping=[]
for i in range(len(xping)):
   y2ping.append(best_fit_poly_1[0]*(xping[i])**2+ best_fit_poly_1[1]*(xping[i])+best_fit_poly_1[2])
"""
#------------------------------------------------------------------------------
#To Create Fits files for SiIV
#------------------------------------------------------------------------------
#CIV
#------------------------------------------------------------------------------
#Creating points for splines
CIV_Polyfit_Points=[make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1601.4,1603.4),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1615.2,1616.2),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1622.4,1623.4),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1626.6,1627.3),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1633.3,1633.5),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1635.2,1635.4),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1637.6,1637.9),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1639.6,1640.1),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1640.9,1641.1),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1642.1,1642.4),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1643.7,1643.9),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1648.0,1649.0),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1654.2,1656.2),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1661.4,1662.2),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1673.4,1674.2),
                    make_polyfit_point(Epoch_06_1_14_WAVE,Epoch_06_1_14_FLUX,1679.2,1681.2)]
#------------------------------------------------------------------------------
x_poly_1_CIV=[item[0]for item in CIV_Polyfit_Points]
y_poly_1_CIV=[item[1]for item in CIV_Polyfit_Points]
#------------------------------------------------------------------------------
#splinesInt is a function i.e. f(x_wavelength)
splinesCIV=interp1d(x_poly_1_CIV,y_poly_1_CIV,kind = 'cubic', bounds_error = False)
#------------------------------------------------------------------------------
#for Graphical purposes, and plotting only, Has no coding
xpingCIV=arange(1605,1675,.05)

PreNormalizedCIV_FX=Epoch_06_1_14_FLUX[find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1605)):find_index(Epoch_06_1_14_WAVE,closest_value(Epoch_06_1_14_WAVE,1675))]
CIV_Spect_WL=arange(Epoch_06_1_14_WAVE[find_index(Epoch_06_1_14_WAVE,1605)],Epoch_06_1_14_WAVE[find_index(Epoch_06_1_14_WAVE,1675)],0.012234810431436927)
CIV_Spect_FX=[]
#------------------------------------------------------------------------------
#Will be changed soon to spline method
for i in range(0,len(CIV_Spect_WL)):
    #First part First order poly
    CIV_Spect_FX.append(PreNormalizedCIV_FX[i]/splinesCIV(CIV_Spect_WL[i]))

#------------------------------------------------------------------------------