"""
Created on Tue Mar 28 10:03:11 2017
@author: Marcus
Shorten/Cleaned Version
This Code is basically the first three steps: 
Data Extractions and Plot
Normalization and Plot
Inturpolation and Plot
"""

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

#------------------------------------------------------------------------------
#from Michael's code)
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
def closest_value_wave(value):
    return(TWL3[find_index(TWL3,value)])
def closest_value_flux(value):
# this returns the FLUX VALUE of the element of the list 'arrayn' CLOSEST to what you put in.
    return(TFS3[find_index(TWL3,value)])
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
#Headers are to give one more information and details about what is in the Fits files

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
#------------------------------------------------------------------------------
#Observing points of interest

badpix(TF1,5180,5405,0)
TFS1=smooth(TF1,20)
TFS3=smooth(TF3,20)
TFS2=smooth(TF2,20)
    
#------------------------------------------------------------------------------

x_poly_anc=[closest_value_wave(1392.5),closest_value_wave(1407),closest_value_wave(1411)]
y_poly_anc=[closest_value_flux(1392.5),closest_value_flux(1407),closest_value_flux(1411)]
                  
x_poly_1425to1455=[closest_value_wave(1426.5),closest_value_wave(1427),closest_value_wave(1430),closest_value_wave(1434),
                   closest_value_wave(1436),closest_value_wave(1437),closest_value_wave(1438),closest_value_wave(1440),
                   closest_value_wave(1441),closest_value_wave(1444),closest_value_wave(1445),closest_value_wave(1448),
                   closest_value_wave(1454)]
y_poly_1425to1455=[closest_value_flux(1426.5),closest_value_flux(1427),closest_value_flux(1430),closest_value_flux(1434),
                   closest_value_flux(1436),closest_value_flux(1437),closest_value_flux(1438),closest_value_flux(1440),
                   closest_value_flux(1441),closest_value_flux(1444),closest_value_flux(1445),closest_value_flux(1448),
                   closest_value_flux(1454)]
                   
x_poly_1500to1545=[closest_value_wave(1501),closest_value_wave(1505),closest_value_wave(1511),closest_value_wave(1517),
                   closest_value_wave(1523),closest_value_wave(1524),closest_value_wave(1529.5),closest_value_wave(1532),
                   closest_value_wave(1533),closest_value_wave(1534),closest_value_wave(1535),closest_value_wave(1536.2),
                   closest_value_wave(1537),closest_value_wave(1540.5),closest_value_wave(1543.5),closest_value_wave(1545)]

y_poly_1500to1545=[closest_value_flux(1501),closest_value_flux(1505),closest_value_flux(1511),closest_value_flux(1517),
                   closest_value_flux(1523),closest_value_flux(1524),closest_value_flux(1529.5),closest_value_flux(1532),
                   closest_value_flux(1533),closest_value_flux(1534),closest_value_flux(1535),closest_value_flux(1536.2),
                   closest_value_flux(1537),closest_value_flux(1540.5),closest_value_flux(1543.5),closest_value_flux(1545)]

x_poly_1680to1745=[closest_value_wave(1680),closest_value_wave(1690),closest_value_wave(1703),closest_value_wave(1707),closest_value_wave(1720),closest_value_wave(1725),closest_value_wave(1735)]
                    
                 
y_poly_1680to1745=[closest_value_flux(1680),closest_value_flux(1690),closest_value_flux(1703),closest_value_flux(1707),closest_value_flux(1720),closest_value_flux(1725),closest_value_flux(1735)]

x_poly_total_3 = x_poly_anc + x_poly_1425to1455 + x_poly_1500to1545 + x_poly_1680to1745
y_poly_total_3 = y_poly_anc + y_poly_1425to1455 + y_poly_1500to1545 + y_poly_1680to1745
poly_array_3=(polyfit(x_poly_total_3,y_poly_total_3,1))

Normal_TFS3=[]
for i in range(len(TWL3)):
  Normal_TFS3.append(TFS3[i]/(poly_array_3[0]*(TWL3[i])+ poly_array_3[1]))

"""
slope_flux=[]

for i in range(len(TWL3)):
    #calculating the flux if every point was along the slope
    sf=TWL3[i]*poly_array[0]+poly_array[1]
    slope_flux.append(sf)
n_flux=[]
for i in range(len(TWL3)):
#Diving the actual flux by the slope flux to get the normalized flux
    nf=TFS3[i]/slope_flux[i]
    n_flux.append(nf)
"""

plt.figure(1)
plt.title('Epoch 6/14/15 G3 with point selection')
plt.xlabel(r'Observed Wavelength ($\AA$)')
plt.ylabel('Flux (erg/s/cm^2/$\AA$)')
plt.plot(x_poly_total_3,y_poly_total_3)
plt.plot(TWL3,TFS3)

plt.axis([1350,1780,0,7*10**-14])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(13.5, 10.5)

plt.figure(2)
plt.title('Epoch 6/14/15 G3 with point selection')
plt.xlabel(r'Observed Wavelength ($\AA$)')
plt.ylabel('Flux (erg/s/cm^2/$\AA$)')
plt.plot(TWL3,Normal_TFS3)

plt.axis([1350,1780,0,2])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(13.5, 10.5)

savefig("/Users/micha/Google Drive/Documents/Python Scripts/PG1126_041/HSUGroup/figure.png")


"""
plt.figure(3)
plt.title('Point selection')
plt.plot(x_poly_total_3,y_poly_total_3)
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(20.5, 10.5)"""

print(poly_array_3)
#------------------------------------------------------------------------------
#Interpolation setup for 1 & 2 from Michael's code

#set_printoptions(threshold=nan) #Prints out entire array if you chose to print an array
"""
begin=TWL2[0] #Beginning of the first grating
end=TWL1[-1]#End of the second grating
array= arange(begin,end,.00997)#This is the array that we are interpolating to.

Iflux2=interp(array,TWL2,TF2,left=0,right=0)#This is the flux interpolation for the first grating, we want zero for the left and right because if a point is outside of the wavelength range we are looking at we do not want to create data.
Ierror2=interp(array,TWL2,ER2,left=0,right=0)#This is the error interpolation for the first grating

Iflux1=interp(array,TWL1,TF1,left=0,right=0)#This is the flux interpolation for the second grating
Ierror1=interp(array,TWL1,ER1,left=0,right=0)#This is the error interpolation for the second grating

#------------------------------------------------------------------------------
#This is Marcus Method to remove 0 from error sample
TME1=[]
TME2=[]
for i in range (0,len(Ierror1)):
    if Ierror1[i] == 0:
        TME1.append(1)
    else:
        TME1.append(Ierror1[i])
        
for i in range (0,len(Ierror2)):
    if Ierror2[i] == 0:
        TME2.append(1)
    else:
        TME2.append(Ierror2[i])
print(len(array))
#------------------------------------------------------------------------------
#Truncated form Michael's code
#3/28 2-3?)

output_array=[]    #Empty array to store the new list of flux values. 
for i in range(0,len(array)):
    if (Iflux2[i]==0 and Iflux1[i]==0).all(): #if both of the values are zero then return zero
            output_array.append(0.0)#stores value in array
    else:      
            weight=(1/TME2[i])
            weight2=(1/TME1[i])
            spec=Iflux2[i]
            spec2=Iflux1[i]
            output_array.append((weight*spec+weight2*spec2)/(weight+weight2))
            
#------------------------------------------------------------------------------
badpix(output_array,32323,32550,0)
PGflux_1and2=output_array

#plt.plot(PGflux_1and2)

#------------------------------------------------------------------------------
#Interpolation of set 3
#From Michael's code 
#4-6-17 2h)

begin2=TWL2[0]#Beginning of the first grating
end2=TWL3[-1]#End of the *THIRD* grating
arrayn= arange(begin2,end2,.0122408)#This is the array that we are interpolating to.NEW STEP SIZE, NEW ARRAY NAME.

Iflux3=interp(arrayn,TWL3,TF3,left=0,right=0)#This is the flux interpolation for the THIRD grating
Ierror3=interp(arrayn,TWL3,ER3,left=0,right=0)#This is the error interpolation for the THIRD grating

PGflux_1and2n=interp(arrayn,array,PGflux_1and2,left=0,right=0)


#------------------------------------------------------------------------------
#combining error sets for 1 and 2
Cerror1and2=[]
for i in range(len(array)):
    if (Ierror2[i]==0 and Ierror1[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
        Cerror1and2.append(Ierror1[i])
    elif (Ierror1[i]==0 and Ierror2[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
        Cerror1and2.append(Ierror2[i])
    elif (Ierror1[i]==0 and Ierror2[i]==0).all():#if both error values are zero then dont weight the flux values
        Cerror1and2.append(0.0)            
    else:#if neither of the error values are zero then take the weighted average of the flux values.
        Cerror1and2.append(sqrt((Ierror1[i])**2+(Ierror2[i])**2))#stores value in array   
ICerror1and2=interp(arrayn,array,Cerror1and2,left=0,right=0)

#------------------------------------------------------------------------------
#remove 0 from error

TME1and2=[]
TME3=[]

for i in range (0,len(ICerror1and2)):
    if ICerror1and2[i] == 0:
        TME1and2.append(1)
    else:
        TME1and2.append(ICerror1and2[i])
 
for i in range (0,len(Ierror3)):
    if Ierror3[i] == 0:
        TME3.append(1)
    else:
        TME3.append(Ierror3[i])

#------------------------------------------------------------------------------
#1h
TFS=[]
for i in range(0,len(arrayn)):
    if (PGflux_1and2n[i]==0 and Iflux3[i]==0).all(): #if both of the values are zero then return zero
            TFS.append(0.0)#stores value in array
    else:      
            weight=(1/TME1and2[i])
            weight2=(1/TME3[i])
            spec=PGflux_1and2n[i]
            spec2=Iflux3[i]
            TFS.append((weight*spec+weight2*spec2)/(weight+weight2))
            
TFSC=smooth(TFS,20)        
TFS1=smooth(TF1,20)   
TFS2=smooth(TF2,20) 
badpix(TFS1,5180,5405,0)
        
plt.figure(1)
plt.title('Epoch 6/14/15')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL1,TFS1)
plt.plot(TWL2,TFS2)
plt.plot(arrayn,TFSC)
plt.axis([1160,1210,0,4*10**-14])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)

plt.figure(2)
plt.title('Epoch 6/14/15')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL1,TFS1)
plt.axis([1160,1260,0,4*10**-14])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)

plt.figure(3)
plt.title('Epoch 6/14/15')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL1,TFS1)
plt.axis([1260,1360,0,15*10**-14])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)

plt.figure(4)
plt.title('Epoch 6/14/15')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL1,TFS1)
plt.axis([1360,1460,0,4*10**-14])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
"""