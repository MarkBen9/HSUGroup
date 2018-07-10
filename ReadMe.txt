Explanation of codes used

	All Epoch_MM_DD_YY_Normalization.py was the first part normalizing- (cont)
	Fits_Generator.py Runs all Epoch_MM_DD_YY_Normalization.py to create fits files: Epoch_MM_DD_YY.fits. 
	Epoch_analysis_from_fits.py plots using Epoch_MM_DD_YY.fits generated from Fits_Generator.py
	Epoch_analysis.py plots one epoch overlayed with each grating, Was used to find discontinuity.
	Epoch_MM_DD_YY_Absorption.py Normalizes regions of interest, as well creates fits files. 
	
https://github.com/MarkBen9/HSUGroup.git

Explanation on how to start using the github
	
	
	
	
	When downloading scripts from the github repository, it will generate a file named HSUGroup. Inside the HSUGroup file, all py scripts will be stored. 
	Create a file named “Data” inside the file which houses HSUGroup file and download all fits files. 
		If you just download files from each grating you can create the Epoch_MM_DD_YY.fits files by running Fits_Generator.py
		After running Fits_Generator.py, move all fits files created to Data Folder. 
	Files should be orginzed as such:	
	...\GitHub\HST_XMM_PG1126_041\HSUGroup
		-Code.py
		-ReadMe.txt
	...\GitHub\HST_XMM_PG1126_041\Data
		-Data.fits
