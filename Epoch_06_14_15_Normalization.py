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
def badpix(list_name,xmin_indice,xmax_indice,replace_val):
    for i in range(xmin_indice,xmax_indice):
        list_name[i]=replace_val
def smooth(y, box_pts):
    box = ones(box_pts)/box_pts
    y_smooth = convolve(y, box, mode='same')
    return y_smooth
def find_index(your_list,your_value):#this finds the INDEX of the element of the list CLOSEST to what you put in.
    x_1=list(your_list)
    return(x_1.index(min(x_1, key=lambda x:abs(x-your_value))))
def closest_value(your_list,value):# this returns the VALUE of the element of the list CLOSEST to what you put in.
    return(your_list[find_index(your_list,value)])
def make_polyfit_point(xlist,ylist,start,end):#give this function some data and a range and it spits out the average x and y
    x_ave=closest_value(xlist,(start+end)/2)
    start_index=find_index(xlist,closest_value(xlist,start))
    end_index=find_index(xlist,closest_value(xlist,end))
    y_sum=0
    for i in range(start_index,end_index,1):
        y_sum+=ylist[i]
    y_ave=closest_value(ylist,y_sum/(end_index-start_index))       
    return [x_ave,y_ave]
def remove_zero_error(error):
    TME1=[]
    for i in range (0,len(error)):
        if error[i] == 0:
            TME1.append(1)
        else:
            TME1.append(error[i])  
    return TME1
#------------------------------------------------------------------------------
#Fits files Opening
#File says that the date obs was 6/14/15 7:15:17
Data1 = fits.open("../Data/lcn701010_x1dsum.fits")
#File says that the date obs was 6/14/15 7:47:56
Data2 = fits.open("../Data/lcn701020_x1dsum.fits")
#File says that the date obs was 6/14/15 9:12:04
Data3 = fits.open("../Data/lcn701030_x1dsum.fits")
#------------------------------------------------------------------------------
#Data Extraction
#headNa  = DataN[0].header headNb  = DataN[1].header where N is an int; was removed to save space 
#Headers are used to give more information and details about what is in the Fits files

TbData1 = Data1[1].data
Data1.close()
TbData2 = Data2[1].data
Data2.close()
TbData3 = Data3[1].data
Data3.close()

#------------------------------------------------------------------------------
wavelength1=TbData1['wavelength']
flux1=TbData1['flux']
error1=TbData1['error']
#
wavelength2=TbData2['wavelength']
flux2=TbData2['flux']
error2=TbData2['error']
#
wavelength3=TbData3['wavelength']
flux3=TbData3['flux']
error3=TbData3['error']
#------------------------------------------------------------------------------
#1162.9A - 1479.5A
TWL1=concatenate((wavelength1[1],wavelength1[0]),axis=0)
TF1=concatenate((flux1[1],flux1[0]),axis=0)
ER1=concatenate((error1[1],error1[0]),axis=0)
#892.4A-1208A
TWL2=concatenate((wavelength2[1],wavelength2[0]),axis=0)
TF2=concatenate((flux2[1],flux2[0]),axis=0)
ER2=concatenate((error2[1],error2[0]),axis=0)
#1374.4A-1763.1A
TWL3=concatenate((wavelength3[1],wavelength3[0]),axis=0)
TF3=concatenate((flux3[1],flux3[0]),axis=0)
ER3=concatenate((error3[1],error3[0]),axis=0)

TWL1,TWL2=TWL2,TWL1 #SWAPPING VARIBLE NAMES SO IT MAKES SENSE
TF1,TF2=TF2,TF1     #SWAPPING VARIBLE NAMES SO IT MAKES SENSE
ER1,ER2=ER2,ER1     #SWAPPING VARIBLE NAMES SO IT MAKES SENSE
#------------------------------------------------------------------------------
#Observing points of interest
#Search for flat regious with no absorption and emision points for normalization
badpix(TF2,5180,5405,0)
TFS1=smooth(TF1,20)
TFS2=smooth(TF2,20)
TFS3=smooth(TF3,20)
###############################################################################
###############################################################################
Grating_1_polyfitpoints=[
                         make_polyfit_point(TWL1,TFS1,1110,1130),
                         make_polyfit_point(TWL1,TFS1,1150,1190)
                         ]
Grating_2_polyfitpoints=[make_polyfit_point(TWL2,TFS2,1175,1185),
                         make_polyfit_point(TWL2,TFS2,1345,1365),
                         make_polyfit_point(TWL2,TFS2,1395,1402),
                         make_polyfit_point(TWL2,TFS2,1420,1460)
                         ]
Grating_3_polyfitpoints=[make_polyfit_point(TWL3,TFS3,1425,1460),
                         make_polyfit_point(TWL3,TFS3,1500,1525),
                         make_polyfit_point(TWL3,TFS3,1590,1605),
                         make_polyfit_point(TWL3,TFS3,1675,1720)]

# For different epochs, input different ranges that represent the continuum. 
#That should be it.

###############################################################################
###############################################################################
x_poly_1=[item[0]for item in Grating_1_polyfitpoints]
y_poly_1=[item[1]for item in Grating_1_polyfitpoints]
x_poly_2=[item[0]for item in Grating_2_polyfitpoints]
y_poly_2=[item[1]for item in Grating_2_polyfitpoints]
x_poly_3=[item[0]for item in Grating_3_polyfitpoints]
y_poly_3=[item[1]for item in Grating_3_polyfitpoints]
best_fit_poly_1=(polyfit(x_poly_1,y_poly_1,1))
best_fit_poly_2=(polyfit(x_poly_2,y_poly_2,1))
best_fit_poly_3=(polyfit(x_poly_3,y_poly_3,1))
#poly_array_1=polyval(best_fit_poly_1, TWL1) #poly_array contains the polynomial EVALUATED by each x point in the grating.
#poly_array_2=polyval(best_fit_poly_2, TWL2) #It is NOT used anywhere in the code but is useful if one wants to plot the slope.
#poly_array_3=polyval(best_fit_poly_3, TWL3)

Normal_TFS1=[]#grating 1
for i in range(len(TWL1)):
    Normal_TFS1.append(TFS1[i]/(best_fit_poly_1[0]*(TWL1[i])+ best_fit_poly_1[1]))
Normal_TFS2=[]#grating 2
for i in range(len(TWL2)):
    Normal_TFS2.append(TFS2[i]/(best_fit_poly_2[0]*(TWL2[i])+ best_fit_poly_2[1]))
Normal_TFS3=[]#grating 3
for i in range(len(TWL3)):
    Normal_TFS3.append(TFS3[i]/(best_fit_poly_3[0]*(TWL3[i])+ best_fit_poly_3[1]))

TWL1_TWL2= arange(TWL1[0],TWL2[-1],.00997)
TWL1_TWL2_TWL3= arange(TWL1[0],TWL3[-1],0.0122408)

Iflux1=interp(TWL1_TWL2,TWL1,Normal_TFS1,left=0,right=0)
Ierror1=interp(TWL1_TWL2,TWL1,ER1,left=0,right=0)
Iflux2=interp(TWL1_TWL2,TWL2,Normal_TFS2,left=0,right=0)
Ierror2=interp(TWL1_TWL2,TWL2,ER2,left=0,right=0)
Iflux3=interp(TWL1_TWL2_TWL3,TWL3,Normal_TFS3,left=0,right=0)
Ierror3=interp(TWL1_TWL2_TWL3,TWL3,ER3,left=0,right=0)

TME1=remove_zero_error(Ierror1)
TME2=remove_zero_error(Ierror2)
TME3=remove_zero_error(Ierror3)
        
Averaged_TFS1_TFS2=[]
for i in range(0,len(TWL1_TWL2)):
    if (Iflux2[i]==0 and Iflux1[i]==0).all():
            Averaged_TFS1_TFS2.append(0.0)
    else:      
            weight=(1/TME1[i])
            weight2=(1/TME2[i])
            spec=Iflux1[i]
            spec2=Iflux2[i]
            Averaged_TFS1_TFS2.append((weight*spec+weight2*spec2)/(weight+weight2))  

badpix(Averaged_TFS1_TFS2,32323,32550,0)
Iflux_1_2=interp(TWL1_TWL2_TWL3,TWL1_TWL2,Averaged_TFS1_TFS2,left=0,right=0)

Error_TFS1_TFS2=[]
for i in range(len(TWL1_TWL2)):
    if (Ierror1[i]!=0 and Ierror2[i]==0).all():
        Error_TFS1_TFS2.append(Ierror1[i])
    elif (Ierror1[i]==0 and Ierror2[i]!=0).all():
        Error_TFS1_TFS2.append(Ierror2[i])
    elif (Ierror1[i]==0 and Ierror2[i]==0).all():
        Error_TFS1_TFS2.append(0.0)            
    else:#if neither of the error values are zero then take the weighted average of the error values.
        Error_TFS1_TFS2.append(sqrt((Ierror1[i])**2+(Ierror2[i])**2))   

Ierror_1_2=interp(TWL1_TWL2_TWL3,TWL1_TWL2,Error_TFS1_TFS2,left=0,right=0)
TME_1_2=remove_zero_error(Ierror_1_2)

Averaged_TFS1_TFS2_TFS3=[]
for i in range(0,len(TWL1_TWL2_TWL3)):  
    if(Iflux_1_2[i]==0 and Iflux3[i]==0):
        Averaged_TFS1_TFS2_TFS3.append(0.0)
    else:
        weight=(1/TME_1_2[i])
        weight2=(1/TME3[i])
        spec=Iflux_1_2[i]
        spec2=Iflux3[i]
        Averaged_TFS1_TFS2_TFS3.append((weight*spec+weight2*spec2)/(weight+weight2))

Final_x_spectrum=TWL1_TWL2_TWL3
Final_y_spectrum=Averaged_TFS1_TFS2_TFS3