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
#------------------------------------------------------------------------------
#Functions
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
def remove_small(mylist,threshold):
    for i in range(0,len(mylist)):
        if mylist[i]<=threshold:
            mylist[i]=0
    return mylist
def find_index_from_value(mylist, value):
    return find_index(mylist,closest_value(mylist,value))
#------------------------------------------------------------------------------
#Fits files Opening
#File says that the date obs was 6/28/14 11:25:07
Data1 = fits.open("../Data/lcbx03010_x1dsum.fits")
#File says that the date obs was 6/28/14 11:57:22
Data2 = fits.open("../Data/lcbx03020_x1dsum.fits")
#File says that the date obs was 6/28/14 13:21:29
Data3 = fits.open("../Data/lcbx03030_x1dsum.fits")
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
#Extracting data into useable lists
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
#Concatenating data sets
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
#------------------------------------------------------------------------------
#SWAPPING VARIBLE NAMES SO IT MAKES SENSE (Michael)
TWL1,TWL2=TWL2,TWL1
TF1,TF2=TF2,TF1
ER1,ER2=ER2,ER1
#------------------------------------------------------------------------------
#Observing points of interest
#Search for flat regious with no absorption and emision points for normalization
badpix(TF2,5180,5405,0)
TFS1=smooth(TF1,20)
TFS2=smooth(TF2,20)
TFS3=smooth(TF3,20)
#------------------------------------------------------------------------------
# Begining of Normalization
#------------------------------------------------------------------------------
#Creating point selection for first order polynomial
Grating_1_polyfitpoints=[make_polyfit_point(TWL1,TFS1,1118,1121),
                         make_polyfit_point(TWL1,TFS1,1160,1161)]
Grating_2_polyfitpoints=[make_polyfit_point(TWL2,TFS2,1178,1182),
                         make_polyfit_point(TWL2,TFS2,1350,1360),
                         make_polyfit_point(TWL2,TFS2,1395,1402),
                         make_polyfit_point(TWL2,TFS2,1435,1445)]
Grating_3_polyfitpoints=[make_polyfit_point(TWL3,TFS3,1425,1460),
                         make_polyfit_point(TWL3,TFS3,1500,1525),
                         make_polyfit_point(TWL3,TFS3,1590,1605),
                         make_polyfit_point(TWL3,TFS3,1675,1720)]
# For different epochs, input different ranges that represent the continuum. 
#------------------------------------------------------------------------------
#Creates first order polynomial
x_poly_1=[item[0]for item in Grating_1_polyfitpoints]
y_poly_1=[item[1]for item in Grating_1_polyfitpoints]
x_poly_2=[item[0]for item in Grating_2_polyfitpoints]
y_poly_2=[item[1]for item in Grating_2_polyfitpoints]
x_poly_3=[item[0]for item in Grating_3_polyfitpoints]
y_poly_3=[item[1]for item in Grating_3_polyfitpoints]
best_fit_poly_1=(polyfit(x_poly_1,y_poly_1,1))
best_fit_poly_2=(polyfit(x_poly_2,y_poly_2,1))
best_fit_poly_3=(polyfit(x_poly_3,y_poly_3,1))
#------------------------------------------------------------------------------
#Graphical Tool
#Used to create a list of points that represent a normalization curves
"""
xping1=arange(TWL1[0],TWL1[-1],.05)
yping1=[]
for i in range(len(xping1)):
    yping1.append(best_fit_poly_1[0]*(xping1[i])+ best_fit_poly_1[1])

xping2=arange(TWL2[0],TWL2[-1],.05)
yping2=[]
for i in range(len(xping2)):
    yping2.append(best_fit_poly_2[0]*(xping2[i])+ best_fit_poly_2[1])

xping3=arange(TWL3[0],TWL3[-1],.05)
yping3=[]
for i in range(len(xping3)):
    yping3.append(best_fit_poly_3[0]*(xping3[i])+ best_fit_poly_3[1])
"""
#------------------------------------------------------------------------------
#Second Order poly fit point selection
Grating_1_2ndOrderPolyfit_Points=[  make_polyfit_point(TWL1,TFS1,1171.0,1172.4),
                                    make_polyfit_point(TWL1,TFS1,1191.2,1192.4),
                                    make_polyfit_point(TWL1,TFS1,1194.3,1196.0),
                                    make_polyfit_point(TWL1,TFS1,1184.0,1186.0),
                                    make_polyfit_point(TWL1,TFS1,1181.0,1182.0)]
Grating_2_2ndOrderPolyfit_Points=[  make_polyfit_point(TWL2,TFS2,1171.0,1172.4),
                                    make_polyfit_point(TWL2,TFS2,1191.2,1192.4),
                                    make_polyfit_point(TWL2,TFS2,1194.3,1196.0),
                                    make_polyfit_point(TWL2,TFS2,1184.0,1186.0),
                                    make_polyfit_point(TWL2,TFS2,1181.0,1182.0),
                                    make_polyfit_point(TWL2,TFS2,1204.0,1205.0)]
#------------------------------------------------------------------------------
#Creates Second Order Polynomial from seleted points
x_2ndpoly_1=[item[0]for item in Grating_1_2ndOrderPolyfit_Points]
y_2ndpoly_1=[item[1]for item in Grating_1_2ndOrderPolyfit_Points]
x_2ndpoly_2=[item[0]for item in Grating_2_2ndOrderPolyfit_Points]
y_2ndpoly_2=[item[1]for item in Grating_2_2ndOrderPolyfit_Points]
best_fit_2ndpoly_1=(polyfit(x_2ndpoly_1,y_2ndpoly_1,2))
best_fit_2ndpoly_2=(polyfit(x_2ndpoly_2,y_2ndpoly_2,2))
#------------------------------------------------------------------------------
#Normalizes for each Grating, Special care taken for Intersection of Grating 1 and 2
#From mathmatica, the polynomial intersects around 1172.14 and, 1200.85
#Remember to change this every time if point selection changes
#------------------------------------------------------------------------------
#For Grating 1
Normal_TFS1=[]
for i in range(0,find_index(TWL1,closest_value(TWL1,1167.23))):                #First part First order poly
    Normal_TFS1.append(TFS1[i]/(best_fit_poly_1[0]*(TWL1[i])+ best_fit_poly_1[1]))
for i in range(find_index(TWL1,closest_value(TWL1,1167.23)),len(TWL1)):        #Second part, Second order poly
    Normal_TFS1.append(TFS1[i]/(best_fit_2ndpoly_1[0]*(TWL1[i])**2+ best_fit_2ndpoly_1[1]*(TWL1[i])+ best_fit_2ndpoly_1[2]))
#For Grating 2
Normal_TFS2=[]
for i in range(0,find_index(TWL2,closest_value(TWL2,1200.91))):                #First part, Second order polynomial
    Normal_TFS2.append(TFS2[i]/(best_fit_2ndpoly_2[0]*(TWL2[i])**2+ best_fit_2ndpoly_2[1]*(TWL2[i])+ best_fit_2ndpoly_2[2]))
for i in range(find_index(TWL2,closest_value(TWL2,1200.91)),len(TWL2)):        #Second part, First order polynomial
    Normal_TFS2.append(TFS2[i]/(best_fit_poly_2[0]*(TWL2[i])+ best_fit_poly_2[1]))
#For Grating 3
Normal_TFS3=[]
for i in range(len(TWL3)):
    Normal_TFS3.append(TFS3[i]/(best_fit_poly_3[0]*(TWL3[i])+ best_fit_poly_3[1]))
#------------------------------------------------------------------------------
    #Begining of combining Gratings
#------------------------------------------------------------------------------
#all Flux below 2% of the normailzation line is equated to 0
remove_small(Normal_TFS1,0.02)
remove_small(Normal_TFS2,0.02)
remove_small(Normal_TFS3,0.02)
#------------------------------------------------------------------------------
#Finding stepsizes for each Grating, then sets the combined spectrua to the largest stepsize of the two
TWL1_STEPSIZE=TWL1[1]-TWL1[0]
TWL2_STEPSIZE=TWL2[1]-TWL2[0]
TWL3_STEPSIZE=TWL3[1]-TWL3[0]

if(TWL1_STEPSIZE<=TWL2_STEPSIZE):
    TWL_1_2_STEPSIZE=TWL2_STEPSIZE
else:
    TWL_1_2_STEPSIZE=TWL1_STEPSIZE
    
if(TWL_1_2_STEPSIZE<=TWL3_STEPSIZE):
    TWL_1_2_3_STEPSIZE=TWL3_STEPSIZE
else:
    TWL_1_2_3_STEPSIZE=TWL_1_2_STEPSIZE

TWL1_TWL2= arange(TWL1[0],TWL2[-1],TWL_1_2_STEPSIZE)
TWL1_TWL2_TWL3= arange(TWL1[0],TWL3[-1],TWL_1_2_3_STEPSIZE)
#------------------------------------------------------------------------------
#Determination for region of grating to be cut (there has to be a better way...)
CUT_GRATINGS=True
if( CUT_GRATINGS):# Enter the wavelength of the areas you would like to cut off, or "None"(no quotes)
    TWL1_Start_Cut=None#Will cut off all values before this 
    TWL1_End_Cut=None #Will cut off all values after this 
    TWL2_Start_Cut=1171.6
    TWL2_End_Cut=1466.6   
    TWL3_Start_Cut=1390.9
    TWL3_End_Cut=None
#------------------------------------------------------------------------------
#Selecting Index for usage when combining Gratings.
    if not TWL1_Start_Cut==None:TWL1_Start_Cut_index=find_index_from_value(TWL1,TWL1_Start_Cut)
    else:
        TWL1_Start_Cut_index=None
    if not TWL1_End_Cut==None:  TWL1_End_Cut_index=find_index_from_value(TWL1,TWL1_End_Cut)
    else:
        TWL1_End_Cut_index=None
    if not TWL2_Start_Cut==None:TWL2_Start_Cut_index=find_index_from_value(TWL2,TWL2_Start_Cut)
    else:
        TWL2_Start_Cut_index=None
    if not TWL2_End_Cut==None:  TWL2_End_Cut_index=find_index_from_value(TWL2,TWL2_End_Cut)
    else:
        TWL2_End_Cut_index=None
    if not TWL3_Start_Cut==None:TWL3_Start_Cut_index=find_index_from_value(TWL3,TWL3_Start_Cut)
    else:
        TWL3_Start_Cut_index=None
    if not TWL3_End_Cut==None:  TWL3_End_Cut_index=find_index_from_value(TWL3,TWL3_End_Cut)
    else:
        TWL3_End_Cut_index=None
#------------------------------------------------------------------------------
#In this Region Michael is using If and else statements to determing where to cut, from given selection above
    if not TWL1_Start_Cut==None and not TWL1_End_Cut==None :
        for i in range(len(TWL1)):#This Loop removes the cut portion of the flux values you have set, not used in the code but it makes plotting the gratings not show the cut portion
            if  i<=TWL1_Start_Cut_index:
                Normal_TFS1[i]=0
                ER1[i]=1
            if i>TWL1_End_Cut_index:
                Normal_TFS1[i]=0
                ER1[i]=1
    elif not TWL1_Start_Cut==None and TWL1_End_Cut==None:
        for i in range(TWL1_Start_Cut_index):
                Normal_TFS1[i]=0
                ER1[i]=1
    elif TWL1_Start_Cut==None and not TWL1_End_Cut==None:
        for i in range(TWL1_End_Cut_index,len(TWL1)):
                Normal_TFS1[i]=0
                ER1[i]=1
                
    if not TWL2_Start_Cut==None and not TWL2_End_Cut==None :
        for i in range(len(TWL2)):#This Loop removes the cut portion of the flux values you have set, not used in the code but it makes plotting the gratings not show the cut portion
            if  i<=TWL2_Start_Cut_index:
                Normal_TFS2[i]=0
                ER2[i]=1
            if i>TWL2_End_Cut_index:
                Normal_TFS2[i]=0
                ER2[i]=1
    elif not TWL2_Start_Cut==None and TWL2_End_Cut==None:
        for i in range(TWL2_Start_Cut_index):
                Normal_TFS2[i]=0
                ER2[i]=1
    elif TWL2_Start_Cut==None and not TWL2_End_Cut==None:
        for i in range(TWL2_End_Cut_index,len(TWL2)):
                Normal_TFS2[i]=0
                ER2[i]=1
    if not TWL3_Start_Cut==None and not TWL3_End_Cut==None :
        for i in range(len(TWL3)):#This Loop removes the cut portion of the flux values you have set, not used in the code but it makes plotting the gratings not show the cut portion
            if  i<=TWL3_Start_Cut_index:
                Normal_TFS3[i]=0
                ER3[i]=1
            if i>TWL3_End_Cut_index:
                Normal_TFS3[i]=0
                ER3[i]=1
    elif not TWL3_Start_Cut==None and TWL3_End_Cut==None:
        for i in range(TWL3_Start_Cut_index):
                Normal_TFS3[i]=0
                ER3[i]=1
    elif TWL3_Start_Cut==None and not TWL3_End_Cut==None:
        for i in range(TWL3_End_Cut_index,len(TWL3)):
                Normal_TFS3[i]=0
                ER3[i]=1
#------------------------------------------------------------------------------
#Interpolation of flux and error
    Iflux1=interp(TWL1_TWL2,       TWL1[TWL1_Start_Cut_index:TWL1_End_Cut_index],Normal_TFS1[TWL1_Start_Cut_index:TWL1_End_Cut_index],left=0,right=0)
    Ierror1=interp(TWL1_TWL2,      TWL1[TWL1_Start_Cut_index:TWL1_End_Cut_index],ER1[TWL1_Start_Cut_index:TWL1_End_Cut_index],left=0,right=0)
    Iflux2=interp(TWL1_TWL2,       TWL2[TWL2_Start_Cut_index:TWL2_End_Cut_index],Normal_TFS2[TWL2_Start_Cut_index:TWL2_End_Cut_index],left=0,right=0)
    Ierror2=interp(TWL1_TWL2,      TWL2[TWL2_Start_Cut_index:TWL2_End_Cut_index],ER2[TWL2_Start_Cut_index:TWL2_End_Cut_index],left=0,right=0)
    Iflux3=interp(TWL1_TWL2_TWL3,  TWL3[TWL3_Start_Cut_index:TWL3_End_Cut_index],Normal_TFS3[TWL3_Start_Cut_index:TWL3_End_Cut_index],left=0,right=0)
    Ierror3=interp(TWL1_TWL2_TWL3, TWL3[TWL3_Start_Cut_index:TWL3_End_Cut_index],ER3[TWL3_Start_Cut_index:TWL3_End_Cut_index],left=0,right=0)            
else:
    
    Iflux1=interp(TWL1_TWL2,TWL1,Normal_TFS1,left=0,right=0)
    Ierror1=interp(TWL1_TWL2,TWL1,ER1,left=0,right=0)
    Iflux2=interp(TWL1_TWL2,TWL2,Normal_TFS2,left=0,right=0)
    Ierror2=interp(TWL1_TWL2,TWL2,ER2,left=0,right=0)
    Iflux3=interp(TWL1_TWL2_TWL3,TWL3,Normal_TFS3,left=0,right=0)
    Ierror3=interp(TWL1_TWL2_TWL3,TWL3,ER3,left=0,right=0)

Iflux1=interp(TWL1_TWL2,TWL1,Normal_TFS1,left=0,right=0)
Ierror1=interp(TWL1_TWL2,TWL1,ER1,left=0,right=0)
Iflux2=interp(TWL1_TWL2,TWL2,Normal_TFS2,left=0,right=0)
Ierror2=interp(TWL1_TWL2,TWL2,ER2,left=0,right=0)
Iflux3=interp(TWL1_TWL2_TWL3,TWL3,Normal_TFS3,left=0,right=0)
Ierror3=interp(TWL1_TWL2_TWL3,TWL3,ER3,left=0,right=0)
#------------------------------------------------------------------------------
#Remove Zero Error
TME1=remove_zero_error(Ierror1)
TME2=remove_zero_error(Ierror2)
TME3=remove_zero_error(Ierror3)
#------------------------------------------------------------------------------
#Reconstructing Continuum using data and error         
Averaged_TFS1_TFS2=[]
for i in range(0,len(TWL1_TWL2)):
    if (Iflux1[i]==0 and Iflux2[i]==0).all():
            Averaged_TFS1_TFS2.append(0.0)
    elif(Iflux1[i]==0 and Iflux2[i]!=0):
        Averaged_TFS1_TFS2.append(Iflux2[i])
    elif(Iflux1[i]!=0 and Iflux2[i]==0):
        Averaged_TFS1_TFS2.append(Iflux1[i])
        
    elif(TME1[i]==1 and TME2[i]!=1):
            Averaged_TFS1_TFS2.append(Iflux2[i])
    elif(TME1[i]!=1 and TME2[i]==1):
            Averaged_TFS1_TFS2.append(Iflux1[i])
    elif(TME1[i]==1 and TME2[i]==1):
            Averaged_TFS1_TFS2.append(0.0)
    else:      
            weight=(1/TME1[i])
            weight2=(1/TME2[i])
            spec=Iflux1[i]
            spec2=Iflux2[i]
            Averaged_TFS1_TFS2.append((weight*spec+weight2*spec2)/(weight+weight2))
            
#Wait why did we add this twice??
badpix(Averaged_TFS1_TFS2,32323,32550,0) 
Iflux_1_2=interp(TWL1_TWL2_TWL3,TWL1_TWL2,Averaged_TFS1_TFS2,left=0,right=0)

Error_TFS1_TFS2=[]
for i in range(len(TWL1_TWL2)):
    if (Ierror1[i]!=1 and Ierror2[i]==1).all():
        Error_TFS1_TFS2.append(Ierror1[i])
    elif (Ierror1[i]==1 and Ierror2[i]!=1).all():
        Error_TFS1_TFS2.append(Ierror2[i])
    elif (Ierror1[i]==1 and Ierror2[i]==1).all():
        Error_TFS1_TFS2.append(1)            
    else:#if neither of the error values are one then take the weighted average of the error values.
        Error_TFS1_TFS2.append(sqrt((Ierror1[i])**2+(Ierror2[i])**2))   

Ierror_1_2=interp(TWL1_TWL2_TWL3,TWL1_TWL2,Error_TFS1_TFS2,left=0,right=0)
TME_1_2=remove_zero_error(Ierror_1_2)

Averaged_TFS1_TFS2_TFS3=[]
for i in range(0,len(TWL1_TWL2_TWL3)):  
    if(Iflux_1_2[i]==0 and Iflux3[i]==0):
        Averaged_TFS1_TFS2_TFS3.append(0.0)
    elif(Iflux_1_2[i]==0 and Iflux3[i]!=0):
        Averaged_TFS1_TFS2_TFS3.append(Iflux3[i])
    elif(Iflux_1_2[i]!=0 and Iflux3[i]==0):
        Averaged_TFS1_TFS2_TFS3.append(Iflux_1_2[i])
        
    elif(TME_1_2[i]==1 and TME3[i]!=1):
            Averaged_TFS1_TFS2_TFS3.append(Iflux3[i])
    elif(TME_1_2[i]!=1 and TME3[i]==1):
            Averaged_TFS1_TFS2_TFS3.append(Iflux_1_2[i])
    elif(TME_1_2[i]==1 and TME3[i]==1):
            Averaged_TFS1_TFS2_TFS3.append(0.0)
    
    else:
        weight=(1/TME_1_2[i])
        weight2=(1/TME3[i])
        spec=Iflux_1_2[i]
        spec2=Iflux3[i]
        Averaged_TFS1_TFS2_TFS3.append((weight*spec+weight2*spec2)/(weight+weight2))
        
Error_TFS1_TFS2_TFS3=[]
for i in range(len(TWL1_TWL2)):
    if (Ierror_1_2[i]!=1 and Ierror3[i]==1).all():
        Error_TFS1_TFS2_TFS3.append(Ierror_1_2[i])
    elif (Ierror_1_2[i]==1 and Ierror3[i]!=1).all():
        Error_TFS1_TFS2_TFS3.append(Ierror3[i])
    elif (Ierror_1_2[i]==1 and Ierror3[i]==1).all():
        Error_TFS1_TFS2_TFS3.append(1)            
    else:#if neither of the error values are one then take the weighted average of the error values.
        Error_TFS1_TFS2_TFS3.append(sqrt((Ierror_1_2[i])**2+(Ierror3[i])**2))  
#------------------------------------------------------------------------------
    #Name change for final normalized and combined data set
#------------------------------------------------------------------------------
Final_e_spectrum=Error_TFS1_TFS2_TFS3
Final_x_spectrum=TWL1_TWL2_TWL3
Final_y_spectrum=Averaged_TFS1_TFS2_TFS3