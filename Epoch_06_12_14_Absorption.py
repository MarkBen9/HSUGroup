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
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('dark_background')
#------------------------------------------------------------------------------
#Initializing
#------------------------------------------------------------------------------
Epoch_06_12_14=fits.open('../Data/Epoch_06_12_14.fits')
Epoch_06_12_14_DATA=Epoch_06_12_14[1].data
Epoch_06_12_14.close()
Epoch_06_12_14_WAVE=Epoch_06_12_14_DATA['wavelength']
Epoch_06_12_14_FLUX=Epoch_06_12_14_DATA['flux']
Epoch_06_12_14_ERROR=Epoch_06_12_14_DATA['error']
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
#PV Section
#------------------------------------------------------------------------------
PV_Spect_FX_2=  Epoch_06_12_14_FLUX[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1140)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1200))]
PV_Spect_ER_2= Epoch_06_12_14_ERROR[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1140)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1200))]
PV_Spect_WL_2=  Epoch_06_12_14_WAVE[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1140)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1200))]
#------------------------------------------------------------------------------
#To Create Fits files for PV
"""
col1=fits.Column(name='wavelength',format='D',array=PV_Spect_WL_2)
col2=fits.Column(name='flux'      ,format='D',array=PV_Spect_FX_2)
col3=fits.Column(name='error'     ,format='D',array=PV_Spect_ER_2)
cols = fits.ColDefs([col1, col2, col3])
tbhdu = fits.BinTableHDU.from_columns(cols)
tbhdu.writeto('PV_Epoch_06_12_14.fits')
#"""
#------------------------------------------------------------------------------
#SiIV Section
#------------------------------------------------------------------------------
    #Point selection
Sil_Polyfit_Point1=[make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1445,1447),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1452.9,1453.8),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1461,1462),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1474,1475),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1478.3,1480),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1486,1487),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1497,1499)]
#------------------------------------------------------------------------------
#points for splines cubic
x_poly_SiIV=[item[0]for item in Sil_Polyfit_Point1]
y_poly_SiIV=[item[1]for item in Sil_Polyfit_Point1]
#------------------------------------------------------------------------------
#Splines Function
splinesSiIV=interp1d(x_poly_SiIV,y_poly_SiIV, kind = 'cubic', bounds_error= False)
PreNormalizedSI_FX=Epoch_06_12_14_FLUX[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1450)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1490))]
#------------------------------------------------------------------------------
#Creates list for SiIV region.
SiIV_Spect_FX_2=[]
SiIV_Spect_WL_2=Epoch_06_12_14_WAVE[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1450)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1490))]
SiIV_Spect_ER_2=Epoch_06_12_14_ERROR[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1450)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1490))]
#------------------------------------------------------------------------------
#Splines method
for i in range(0,len(SiIV_Spect_WL_2)):
    #Second part Second order poly
    SiIV_Spect_FX_2.append((PreNormalizedSI_FX[i])/(splinesSiIV(SiIV_Spect_WL_2[i])))
#------------------------------------------------------------------------------
#To Create Fits files for SiIV
"""
col1=fits.Column(name='wavelength',format='D',array=SiIV_Spect_WL_2)
col2=fits.Column(name='flux'      ,format='D',array=SiIV_Spect_FX_2)
col3=fits.Column(name='error'     ,format='D',array=SiIV_Spect_ER_2)
cols = fits.ColDefs([col1, col2, col3])
tbhdu = fits.BinTableHDU.from_columns(cols)
tbhdu.writeto('SiIV_Epoch_06_12_14.fits')
"""
#------------------------------------------------------------------------------
#CIV
#------------------------------------------------------------------------------
#Creating points for splines
CIV_Polyfit_Points=[make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1601.4,1603.4),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1613.4,1613.8),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1622.4,1623.4),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1626.6,1627.3),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1633.4,1633.5),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1635.2,1635.4),
                    #make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1638.1,1638.2),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1639.6,1640.1),
                    #make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1640.9,1641.1),
                    #make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1642.7,1643),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1643.7,1643.9),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1648.0,1649.0),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1651.0,1652.0),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1654.2,1656.2),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1661.4,1662.2),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1673.4,1674.2),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1679.2,1681.2)]
#------------------------------------------------------------------------------
x_poly_CIV=[item[0]for item in CIV_Polyfit_Points]
y_poly_CIV=[item[1]for item in CIV_Polyfit_Points]
#------------------------------------------------------------------------------
#splinesInt is a function i.e. f(x_wavelength)
splinesCIV=interp1d(x_poly_CIV,y_poly_CIV,kind = 'cubic', bounds_error = False)
PreNormalizedCIV_FX=Epoch_06_12_14_FLUX[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1605)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1675))]
#------------------------------------------------------------------------------
#Normalized
CIV_Spect_ER_2=Epoch_06_12_14_ERROR[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1605)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1675))]
CIV_Spect_WL_2=arange(Epoch_06_12_14_WAVE[find_index(Epoch_06_12_14_WAVE,1605)],Epoch_06_12_14_WAVE[find_index(Epoch_06_12_14_WAVE,1675)],0.012234810431436927)
CIV_Spect_FX_2=[]

for i in range(0,len(CIV_Spect_WL_2)):
    #First part First order poly
    CIV_Spect_FX_2.append(PreNormalizedCIV_FX[i]/splinesCIV(CIV_Spect_WL_2[i]))
#------------------------------------------------------------------------------
"""
col1=fits.Column(name='wavelength',format='D',array=CIV_Spect_WL_2)
col2=fits.Column(name='flux'      ,format='D',array=CIV_Spect_FX_2)
col3=fits.Column(name='error'     ,format='D',array=CIV_Spect_ER_2)
cols = fits.ColDefs([col1, col2, col3])
tbhdu = fits.BinTableHDU.from_columns(cols)
tbhdu.writeto('CIV_Epoch_06_12_14.fits')
"""
#------------------------------------------------------------------------------
        #NV
#------------------------------------------------------------------------------
NV_Polyfit_Points =[make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1257,1258),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1265,1266),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1273,1274),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1277.5,1278),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1282,1283),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1286,1286.1),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1287.6,1287.8),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1289.5,1290),
                    #make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1301.7,1301.85),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1310.8,1311),
                    make_polyfit_point(Epoch_06_12_14_WAVE,Epoch_06_12_14_FLUX,1327,1328)]        
#------------------------------------------------------------------------------
x_poly_NV=[item[0]for item in NV_Polyfit_Points]
y_poly_NV=[item[1]for item in NV_Polyfit_Points]
#------------------------------------------------------------------------------
#splinesInt is a function i.e. f(x_wavelength)
splinesNV=interp1d(x_poly_NV,y_poly_NV,kind = 'cubic', bounds_error = False)
PreNormalizedNV_FX=Epoch_06_12_14_FLUX[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1260)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1320))]
#------------------------------------------------------------------------------
#Normalized
NV_Spect_ER_2=Epoch_06_12_14_ERROR[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1260)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1320))]
NV_Spect_WL_2= Epoch_06_12_14_WAVE[find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1260)):find_index(Epoch_06_12_14_WAVE,closest_value(Epoch_06_12_14_WAVE,1320))]
NV_Spect_FX_2=[]
for i in range(0,len(NV_Spect_WL_2)):
    #First part First order poly
    NV_Spect_FX_2.append(PreNormalizedNV_FX[i]/splinesNV(NV_Spect_WL_2[i]))
#------------------------------------------------------------------------------
#Fits Files for NV Region
    """
col1=fits.Column(name='wavelength',format='D',array=NV_Spect_WL_2)
col2=fits.Column(name='flux'      ,format='D',array=NV_Spect_FX_2)
col3=fits.Column(name='error'     ,format='D',array=NV_Spect_ER_2)
cols = fits.ColDefs([col1, col2, col3])
tbhdu = fits.BinTableHDU.from_columns(cols)
tbhdu.writeto('NV_Epoch_06_12_14.fits')
"""