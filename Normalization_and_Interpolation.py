# -*- coding: utf-8 -*-

"""
Created on Fri Feb 2 2017
Please leave comments on progress here, for others to use
Currently do to computer crash trying to replicate what was completed SP 17
@author: Marcus
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

#from Peak import *

def badpix(list_name,xmin_indice,xmax_indice,replace_val):
    for i in range(xmin_indice,xmax_indice):
        list_name[i]=replace_val
        
#Fits files Opens
#UT date of start of observation
#------------------------------------------------------------------------------
"""--Epoch one--"""
#File says that the date obs was 6/14/15 7:15:17
Data1 = fits.open("../Data/lcn701010_x1dsum.fits")
#File says that the date obs was 6/14/15 7:47:56
Data2 = fits.open("../Data/lcn701020_x1dsum.fits")
#File says that the date obs was 6/14/15 9:12:04
Data3 = fits.open("../Data/lcn701030_x1dsum.fits")
"""--Epoch two--"""

#File says that the date obs was 6/1/14 3:05:15
Data4 = fits.open("../Data/lcbx01010_x1dsum.fits")
#File says that the date obs was 6/1/14 3:37:30
Data5 = fits.open("../Data/lcbx01020_x1dsum.fits")
#File says that the date obs was 6/1/14 5:01:22
Data6 = fits.open("../Data/lcbx01030_x1dsum.fits")
"""-Epoch three-"""
#File says that the date obs was 6/12/14 16:19:16
Data7 = fits.open("../Data/lcbx02010_x1dsum.fits")
#File says that the date obs was 6/12/14 16:51:31
Data8 = fits.open("../Data/lcbx02020_x1dsum.fits")
#File says that the date obs was 6/12/14 18:14:30
Data9 = fits.open("../Data/lcbx02030_x1dsum.fits")
"""-Epoch four-"""
#File says that the date obs was 6/28/14 11:25:07
Data10 = fits.open("../Data/lcbx03010_x1dsum.fits")
#File says that the date obs was 6/28/14 11:57:22
Data11 = fits.open("../Data/lcbx03020_x1dsum.fits")
#File says that the date obs was 6/28/14 13:21:29
Data12 = fits.open("../Data/lcbx03030_x1dsum.fits")
#------------------------------------------------------------------------------

#Data Extraction Epoch 1
#------------------------------------------------------------------------------
#Grating type G130M for this file *CAN CHANGE WITH DIFFERENT Source FILE*
#G130M has low Resolving power with wavelengths below 1130 Angstroms
#Range 900A-1450A
"""CENTRWV = 1327"""
head1a  = Data1[0].header
head1b  = Data1[1].header
TbData1 = Data1[1].data
Data1.close()
"""CENTRWV = 1050"""
head2a  = Data2[0].header
head2b  = Data2[1].header
TbData2 = Data2[1].data
Data2.close()
"""CENTRWV = 1564"""
head3a  = Data3[0].header
head3b  = Data3[1].header
TbData3 = Data3[1].data
Data3.close()
#------------------------------------------------------------------------------

#Data Extraction Epoch 2
#------------------------------------------------------------------------------
#G130M 
"""CENTRWV = 1319"""
head4a  = Data4[0].header
head4b  = Data4[1].header
TbData4 = Data4[1].data
Data4.close()
"""CENTRWV = 1050"""
head5a  = Data5[0].header
head5b  = Data5[1].header
TbData5 = Data5[1].data
Data5.close()
"""CENTRWV = 1572"""
head6a  = Data6[0].header
head6b  = Data6[1].header
TbData6 = Data6[1].data
Data6.close()
#------------------------------------------------------------------------------

#Data Extraction Epoch 3
#------------------------------------------------------------------------------
"""CENTRWV = 1319"""
head7a  = Data7[0].header
head7b  = Data7[1].header
TbData7 = Data7[1].data
Data7.close()
"""CENTRWV = 1050"""
head8a  = Data8[0].header
head8b  = Data8[1].header
TbData8 = Data8[1].data
Data8.close()
"""CENTRWV = 1572"""
head9a  = Data9[0].header
head9b  = Data9[1].header
TbData9 = Data9[1].data
Data9.close()
#------------------------------------------------------------------------------

#Data Extraction Epoch 4
#------------------------------------------------------------------------------
"""CENTRWV = 1319"""
head10a  = Data10[0].header
head10b  = Data10[1].header
TbData10 = Data10[1].data
Data10.close()
"""CENTRWV = 1050"""
head11a  = Data11[0].header
head11b  = Data11[1].header
TbData11 = Data11[1].data
Data11.close()
"""CENTRWV = 1572"""
head12a  = Data12[0].header
head12b  = Data12[1].header
TbData12 = Data12[1].data
Data12.close()
#------------------------------------------------------------------------------

#Printing Headers to learn more about file

#print(head12a)
"""
print(head11a)
print(head12a)
"""
#print(head2a)
"""
print(head11b)
print(head12b)
"""

#Data Set Epoch 1 Concatenated 
#------------------------------------------------------------------------------
"""--Set one--"""
wavelength1=TbData1['wavelength']
flux1=TbData1['flux']
error1=TbData1['error']
"""--Set two--"""
wavelength2=TbData2['wavelength']
flux2=TbData2['flux']
error2=TbData2['error']
"""--Set three--"""
wavelength3=TbData3['wavelength']
flux3=TbData3['flux']
error3=TbData3['error']

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

#Data Set Epoch 2 Concatenated 
#------------------------------------------------------------------------------
"""--Set two--"""
wavelength4=TbData4['wavelength']
flux4=TbData4['flux']
error4=TbData4['error']
"""--Set two--"""
wavelength5=TbData5['wavelength']
flux5=TbData5['flux']
error5=TbData5['error']
"""--Set three--"""
wavelength6=TbData6['wavelength']
flux6=TbData6['flux']
error6=TbData6['error']

#1162.9A - 1479.5A
TWL4=concatenate((wavelength4[1],wavelength4[0]),axis=0)
TF4=concatenate((flux4[1],flux4[0]),axis=0)
#892.4A-1208.1A
TWL5=concatenate((wavelength5[1],wavelength5[0]),axis=0)
TF5=concatenate((flux5[1],flux5[0]),axis=0)
#1374.4A-1763.1A
TWL6=concatenate((wavelength6[1],wavelength6[0]),axis=0)
TF6=concatenate((flux6[1],flux6[0]),axis=0)
#------------------------------------------------------------------------------

#Data Set Epoch 3 Concatenated 
#------------------------------------------------------------------------------
"""--Set one--"""
wavelength7=TbData7['wavelength']
flux7=TbData7['flux']
error7=TbData7['error']
"""--Set two--"""
wavelength8=TbData8['wavelength']
flux8=TbData8['flux']
error8=TbData8['error']
"""--Set three--"""
wavelength9=TbData9['wavelength']
flux9=TbData9['flux']
error9=TbData9['error']

#1162.9A-1479.5A
TWL7=concatenate((wavelength7[1],wavelength7[0]),axis=0)
TF7=concatenate((flux7[1],flux7[0]),axis=0)
#892.4A-1208.0A
TWL8=concatenate((wavelength8[1],wavelength8[0]),axis=0)
TF8=concatenate((flux8[1],flux8[0]),axis=0)
#1374.4A-1763.1A
TWL9=concatenate((wavelength9[1],wavelength9[0]),axis=0)
TF9=concatenate((flux9[1],flux9[0]),axis=0)
#------------------------------------------------------------------------------

#Data Set Epoch 4 Concatenated 
#------------------------------------------------------------------------------
"""--Set one--"""
wavelength10=TbData10['wavelength']
flux10=TbData10['flux']
error10=TbData10['error']
"""--Set two--"""
wavelength11=TbData11['wavelength']
flux11=TbData11['flux']
error11=TbData11['error']
"""--Set three--"""
wavelength12=TbData12['wavelength']
flux12=TbData12['flux']
error12=TbData12['error']

#1162.9A-1479.5A
TWL10=concatenate((wavelength10[1],wavelength10[0]),axis=0)
TF10=concatenate((flux10[1],flux10[0]),axis=0)
#892.4A-1208.0A
TWL11=concatenate((wavelength11[1],wavelength11[0]),axis=0)
TF11=concatenate((flux11[1],flux11[0]),axis=0)
#1374.4A-1763.1A
TWL12=concatenate((wavelength12[1],wavelength12[0]),axis=0)
TF12=concatenate((flux12[1],flux12[0]),axis=0)
#------------------------------------------------------------------------------

#print(TWL10)
#print(TWL11)
#print(TWL12)

"""
#AN Should be fixing this- (scaling plots)
#Graph Epoch One (Pre Norm)
#------------------------------------------------------------------------------
plt.figure(1)
plt.title('Epoch 6/14/15')
plt.xlabel('Wavelength(A)')
plt.ylabel('Flux')
plt.plot(TWL1,TF1)
plt.plot(TWL2,TF2)
plt.plot(TWL3,TF3)
plt.axis([880,1780,0,1*10**-13])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
#fig.savefig('June-14-2015.png', dpi=100)
#------------------------------------------------------------------------------

#Graph Epoch Two (Pre Norm)
#------------------------------------------------------------------------------
plt.figure(2)
plt.title('Epoch 6/01/14')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL4,TF4)
plt.plot(TWL5,TF5)
plt.plot(TWL6,TF6)
plt.axis([880,1780,0,1*10**-13])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
#fig.savefig('June-1-2014.png', dpi=100)
#------------------------------------------------------------------------------

#Graph Epoch Three (Pre Norm)
#------------------------------------------------------------------------------
plt.figure(3)
plt.title('Epoch 6/12/14')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL7,TF7)
plt.plot(TWL8,TF8)
plt.plot(TWL9,TF9)
plt.axis([880,1780,0,1*10**-13])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
#fig.savefig('June-12-2014.png', dpi=100)
#------------------------------------------------------------------------------

#Graph Epoch four (Pre Norm)
#------------------------------------------------------------------------------
plt.figure(4)
plt.title('Epoch 6/28/14')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.plot(TWL10,TF10)
plt.plot(TWL11,TF11)
plt.plot(TWL12,TF12)
plt.axis([880,1780,0,1*10**-13])
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5)
#fig.savefig('June-28-2014.png', dpi=100)
#------------------------------------------------------------------------------
"""

#------------------------------------------------------------------------------
#Interpolation setup from Mich code

#set_printoptions(threshold=nan) #Prints out entire array if you chose to print an array

begin=TWL2[0] #Beginning of the first grating
end=TWL1[-1]#End of the second grating
array= arange(begin,end,.00997)#This is the array that we are interpolating to.

Iflux2=interp(array,TWL2,TF2,left=0,right=0)#This is the flux interpolation for the first grating, we want zero for the left and right because if a point is outside of the wavelength range we are looking at we do not want to create data.
Ierror2=interp(array,TWL2,ER2,left=0,right=0)#This is the error interpolation for the first grating

Iflux1=interp(array,TWL1,TF1,left=0,right=0)#This is the flux interpolation for the second grating
Ierror1=interp(array,TWL1,ER1,left=0,right=0)#This is the error interpolation for the second grating

output_array=[]#Empty array to store the new list of flux values.
TME1=[]
TME2=[]
#print(Ierror1)

#------------------------------------------------------------------------------
"""This is Marcus Method to remove 0 from error sample"""
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
#------------------------------------------------------------------------------
#Truncated form Mich code
#3/38 2-3?)
        
for i in range(0,len(array)):
    if (Iflux1[i]==0 and Iflux2[i]!=0).all():
            weight=(1/TME2[i])
            weight2=(1/TME1[i])
            spec=Iflux2[i]
            spec2=Iflux1[i]
            output_array.append((weight*spec+weight2*spec2)/(weight+weight2))#stores value in array
    elif (Iflux2[i]==0 and Iflux1 !=0).all():
            weight=(1/TME2[i])
            weight2=(1/TME1[i])
            spec=Iflux2[i]
            spec2=Iflux1[i]
            output_array.append((weight*spec+weight2*spec2)/(weight+weight2))
    elif (Iflux2[i]==0 and Iflux1[i]==0).all():#if both of the values are zero then return zero
            output_array.append(0.0)
    else:      
            weight=(1/TME2[i])
            weight2=(1/TME1[i])
            spec=Iflux2[i]
            spec2=Iflux1[i]
            output_array.append((weight*spec+weight2*spec2)/(weight+weight2))
            
#------------------------------------------------------------------------------
badpix(output_array,32323,32550,0)
PGflux_1and2=output_array
#------------------------------------------------------------------------------
#Interpolation
#From Mich's code 
#4-6-17 1h)
"""
begin2=TWL2[0]#Beginning of the first grating
end2=TWL3[-1]#End of the *THIRD* grating
arrayn= arange(begin2,end2,.0122408)#This is the array that we are interpolating to.NEW STEP SIZE, NEW ARRAY NAME.

Iflux3=interp(arrayn,TWL3,TF3,left=0,right=0)#This is the flux interpolation for the THIRD grating
Ierror3=interp(arrayn,TWL3,ER3,left=0,right=0)#This is the error interpolation for the THIRD grating

PGflux_1and2n=interp(arrayn,array,PGflux_1and2,left=0,right=0)

#plt.plot(PGflux_1and2n)

PGerror_1and2=[]
for i in range(len(array)):
    if (PGerror_1n[i]==0 and PGerror_2n[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
        PGerror_1and2.append(PGerror_2n[i])
    elif (PGerror_2n[i]==0 and PGerror_1n[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
        PGerror_1and2.append(PGerror_1n[i])
    elif (PGerror_2n[i]==0 and PGerror_1n[i]==0).all():#if both error values are zero then dont weight the flux values
        PGerror_1and2.append(0.0)            
    else:#if neither of the error values are zero then take the weighted average of the flux values.
        PGerror_1and2.append(sqrt((PGerror_1n[i])**2+(PGerror_2n[i])**2))#stores value in array      
PGerror_1and2n=interp(arrayn,array,PGerror_1and2,left=0,right=0)

#############AVERAGING NON ZERO POINTS#########################################

noutput_array=[]#Empty array to store the new list of flux values.
for i in range(0,len(arrayn)):#This is the for loop to calculate the weighted average for the points that overlap in the first and second grating.
    if (PGflux_1and2n[i]==0 and PGflux_3n[i] !=0).all() :#If the flux value for the first grating is zero then use the data from the second grating
        if (PGerror_1and2n[i]==0 and PGerror_3n[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
            weight=(1)#Weight of 1=no weight
            weight2=(1/PGerror_3n[i])
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))
        elif (PGerror_3n[i]==0 and PGerror_1and2n[i]==0).all():#if both error values are zero then dont weight the flux values
            noutput_array.append(0.0) 
        else:#if neither of the error values are zero then take the weighted average of the flux values.
            weight=(1/PGerror_1and2n[i])
            weight2=(1/PGerror_3n[i])
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))#stores value in array
    elif (PGflux_3n[i]==0 and PGflux_1and2n !=0).all() :#if the flux value for the second grating is zero then use the data from the first grating
        if (PGerror_3n[i]==0 and PGerror_1and2n[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
            weight=(1/PGerror_1and2n[i])
            weight2=(1)#Weight of 1=no weight
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))
        elif (PGerror_3n[i]==0 and PGerror_1and2n[i]==0).all():#if both error values are zero then dont weight the flux values
            noutput_array.append(0.0)            
        else:#if neither of the error values are zero then take the weighted average of the flux values.
            weight=(1/PGerror_1and2n[i])
            weight2=(1/PGerror_3n[i])
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))#stores value in array
    elif (PGflux_1and2n[i]==0 and PGflux_3n[i]==0).all():#if both of the values are zero then return zero
        noutput_array.append(0.0)
    else:#if neither of the flux values are zero then take the weighted average of the two flux values by using the error values.
        if (PGerror_1and2n[i]==0 and PGerror_3n[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
            weight=(1)#Weight of 1=no weight
            weight2=(1/PGerror_3n[i])
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))
        elif (PGerror_3n[i]==0 and PGerror_1and2n[i]!=0).all():#If the error value for the first grating is zero dont weight the corresponding flux value
            weight=(1/PGerror_1and2n[i])
            weight2=(1)#Weight of 1=no weight
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))
        elif (PGerror_3n[i]==0 and PGerror_1and2n[i]==0).all():#if both error values are zero then dont weight the flux values
            noutput_array.append(0.0)            
        else:#if neither of the error values are zero then take the weighted average of the flux values.
            weight=(1/PGerror_1and2n[i])
            weight2=(1/PGerror_3n[i])
            spec=PGflux_1and2n[i]
            spec2=PGflux_3n[i]
            noutput_array.append((weight*spec+weight2*spec2)/(weight+weight2))#stores value in arrray

"""
