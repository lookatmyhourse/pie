# -*- coding: utf8 -*-
import os,sys
from numpy import arange
#from pylab import *
from decimal import *
from scipy.interpolate import splrep
from scipy.interpolate import splev
from operator import sub
from scipy.optimize import curve_fit

#def dependencies_for_myprogram():
#    from scipy.sparse.csgraph import _validation
#
	
def nja2dat(fname):
	#fixed values for the calculation
	a1=Decimal(0.0484)
	a2=Decimal(0.00084)
	#stepsize
	stepsize=0.013
	#-------------------------
	twotheta=[]
	intensity=[]
	twotheta_corr=[]
	twotheta_corr_list=[]
	twotheta_dat=[]
	
	f = open(fname, 'r')
	lines=f.readlines()
	f.close()

	getcontext().prec = 5
	for i in range(0,len(lines)):
		twotheta.append(Decimal(lines[i].split()[0]))
		intensity.append(int(lines[i].split()[1])) 			 
		while twotheta[i]<Decimal('60.0000'):
			twotheta_corr.append(Decimal(twotheta[i]-(a1-a2*twotheta[i])))
			twotheta_dat.append(Decimal(twotheta[i]))
			twotheta_corr_list.append(twotheta_corr[i])
			break
		else:
			twotheta_corr=twotheta
			twotheta_dat.append(Decimal(twotheta[i]))
			twotheta_corr_list.append(twotheta_corr[i])

	first_point=float(min(twotheta_corr_list))
	last_point=float(max(twotheta_corr_list))
	lent=len(twotheta_corr_list)
	
	xnew=arange(first_point,last_point,stepsize)
	twotheta_corr_list_floats=[]
	for i in range(0,lent):
		ss=Decimal(twotheta_corr_list[i])
		ss2=float(ss)
		twotheta_corr_list_floats.append(ss2)
	
	#SPLINE interpolation / cubic spline
	# tck=interpolate.splrep(self.twotheta_corr_list_floats, self.intensity,s=0)
	# self.fl_spline=interpolate.splev(self.xnew,tck,der=0)
	
	tck=splrep(twotheta_corr_list_floats, intensity,s=0)
	fl_spline=splev(xnew,tck,der=0)
	
	#creating the file of the interpolation 
	newfilename2=fname[0:-4]+'_corr.dat'
	f1=open(newfilename2,'w')
	for i in range(0,lent):
		f1.write('   ')
		f1.write(str(round(xnew[i],4)))
		f1.write('         ')
		f1.write(str(round(fl_spline[i],0)))
		f1.write('\n')
	f1.close()

#read uncorrected datafiles from the _data_files folder and work them through
def apply_peak_pos_correction():
	"""
	Applies the peak shift correction for all the files in the _data_files 
	folder. 
	Execute at the current folder where the '_data_files' is a subfolder
	"""
	mother_folder=os.getcwd()
	#list out the content of the data_files folder 
	dat=os.listdir('./_data_files/')
	#change the working folder to the _data_files
	os.chdir('_data_files')
	[nja2dat(i) for i in dat]
#	for i in dat:
#		nja2dat(i)

	#get back to the mother folder
	os.chdir(mother_folder)


if __name__ == "__main__":
	apply_peak_pos_correction()	
#    sys.exit(app.exec_())
