# -*- coding: utf8 -*-
import sys
import os
from pylab import *
from window import *

from decimal import *

#from scipy import interpolate
from scipy.interpolate import splrep #interpolate
from scipy.interpolate import splev
from time import sleep

from operator import sub
from scipy.optimize import curve_fit

def dependencies_for_myprogram():
    from scipy.sparse.csgraph import _validation

class GUIForm(QtGui.QMainWindow):
		
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.pushButton1.clicked.connect(self.showDialog)
		self.ui.pushButton2.clicked.connect(self.nja2dat)
		self.ui.password.clicked.connect(self.password)
		self.ui.pushButton4.clicked.connect(self.plotter)
		#self.ui.pushButton5.clicked.connect(self.autoindex)
		
		#check for the existance of the setup file
		if os.path.exists('setup.txt'):
			A_B=loadtxt('setup.txt')
			self.ui.labelAnum.setText(str(A_B[0]))
			self.ui.labelBnum.setText(str(A_B[1]))
		else:
			self.ui.labelAnum.setText('value not set')
			self.ui.labelBnum.setText('please set value')
			
	def password(self):
		whatever, okl = QtGui.QInputDialog.getText(self, 'Password Required', 'Enter password:')
			
		if whatever=='RayfleX':
			numA, ok2 = QtGui.QInputDialog.getDouble(self, 'A out of (A,B)', 'Enter A :',decimals=5)
			self.AA=numA
			numB, ok2 = QtGui.QInputDialog.getDouble(self, 'B out of (A,B)', 'Enter B :',decimals=5)
			self.BB=numB
			fsett=open('setup.txt','w')			#save the values to a file for permanent stay
			fsett.write(str(self.AA))
			fsett.write('\n')
			fsett.write(str(self.BB))
			fsett.close()
			self.ui.labelAnum.setText(str(self.AA))
			self.ui.labelBnum.setText(str(self.BB))
		
	
	def showDialog(self):
		self.fname=QtGui.QFileDialog.getOpenFileName(self, 'Open file','/host/GDrive/_Showroom/nja2dat')
		self.ui.le.setText(self.fname)
		f = open(self.fname, 'r')
		data = f.read()
		f.close()
		self.ui.textEdit.setText(data)
	def nja2dat(self):
		f = open(self.fname, 'r')
		lines=f.readlines()[3:]
		f.close()
		
		self.twotheta=[]
		self.intensity=[]
		self.twotheta_corr=[]
		self.twotheta_corr_list=[]
		self.twotheta_dat=[]
		
		#the values for the calculation are read 
		A_B=loadtxt('setup.txt')
		a1=Decimal(A_B[0])
		a2=Decimal(A_B[1])
		
		getcontext().prec = 5
		for i in range(0,len(lines)):
			self.twotheta.append(Decimal(lines[i][0:10]))
			self.intensity.append(int(lines[i][11:]))
			while self.twotheta[i]<Decimal('60.0000'):
				self.twotheta_corr.append(Decimal(self.twotheta[i]-(a1-a2*self.twotheta[i])))
				self.twotheta_dat.append(Decimal(self.twotheta[i]))
				self.twotheta_corr_list.append(self.twotheta_corr[i])
				break
			else:
				self.twotheta_corr=self.twotheta
				self.twotheta_dat.append(Decimal(self.twotheta[i]))
				self.twotheta_corr_list.append(self.twotheta_corr[i])
	
		print 'finished...'

		self.first_point=float(min(self.twotheta_corr_list))
		self.last_point=float(max(self.twotheta_corr_list))
		self.lent=len(self.twotheta_corr_list)
		#self.xnew=linspace(self.first_point,self.last_point,self.lent)  #IMPORTANT USE ARANGE to get eq pointdistances
		stepsize=0.01
		self.xnew=arange(self.first_point,self.last_point,stepsize)
		self.twotheta_corr_list_floats=[]
		for i in range(0,self.lent):
			ss=Decimal(self.twotheta_corr_list[i])
			ss2=float(ss)
			self.twotheta_corr_list_floats.append(ss2)
		
		#SPLINE interpolation / cubic spline
		# tck=interpolate.splrep(self.twotheta_corr_list_floats, self.intensity,s=0)
		# self.fl_spline=interpolate.splev(self.xnew,tck,der=0)
		
		tck=splrep(self.twotheta_corr_list_floats, self.intensity,s=0)
		self.fl_spline=splev(self.xnew,tck,der=0)
		print "Interpolation successful!"
		
	#creating the file of the interpolation 
		self.newfilename2=self.fname[0:-4]+'_corr_interp_spline.dat'
		f1=open(self.newfilename2,'w')
		for i in range(0,self.lent):
			f1.write('   ')
			f1.write(str(round(self.xnew[i],4)))
			f1.write('         ')
			f1.write(str(round(self.fl_spline[i],0)))
			f1.write('\n')
		f1.close()

		print 'A file with interpolations has been generated and saved with _corr_interp_spline.dat next to your file!'
		f3=open(self.newfilename2,'r')
		data3=f3.read()
		f3.close()
		self.ui.textEdit2.setText(data3)
		self.ui.msgBox3.exec_()
		
	def plotter(self):
		fig1=figure('All')
		font = {'family' : 'serif','color'  : 'darkred','weight' : 'normal','size': 16}
		
		plot(self.twotheta, self.intensity,'ro-',ms=8)
		plot(self.twotheta_corr_list, self.intensity, 'bo-',ms=6)
		plot(self.xnew,self.fl_spline,'k^:')

		xlabel('2theta',fontdict=font)
		ylabel('intensity (relative units)',fontdict=font)
		legend(['uncorrected', 'corrected','Spline'], loc='upper right')
		
		plt.show()
		#self.ui.lepic.setPixmap(QtGui.QPixmap("pepper_icon2.png"))
		
		
	# def autoindex(self):
		# nist_standard=[21.3578,
               # 30.3847,
               # 37.4417,
               # 43.5064,
               # 48.9573,
               # 53.9886,
               # 63.2182,
               # 67.5474,
               # 71.7452,
               # 75.8438,
               # 79.8695,
               # 83.8452,
               # 87.7914,
               # 95.6707,
               # 99.6418,
              # 103.6602,
              # 107.7485,
              # 111.9325,
              # 116.2437]	
		# peak_pos=[]	
		
		# #turning the filename variable to string to work with loadtxt
		# self.localname=str(self.newfilename2)
		
		# data6=loadtxt(self.localname)
		
		# getcontext().prec = 6
		# theta			=[]
		# intensity		=[]
		# each_peak		=[]
		# each_peak_peak	=[]
		# x				=[]
		# yn				=[]
		
		# for i in range (0,len(data6)):
		    # theta.append(data6[i][0])
		    # a=data6[i][1]
		    # intensity.append(int(a))
		
		# intensity_orig=intensity
		# for r in range(0,19):
		    # each_peak=[]
		    # each_peak_peak=[]
		    # x=[]
		    # yn=[]
		    
		    # c1_index=intensity.index(max(intensity))
		    # c2_value=float(theta[c1_index])
		    # c3=c1_index-30
		    # c4=c1_index+30
		    
		    # #peak_pos.append(c2_value)
		    
		    # theta_of_peak=[]
		    # peak=[]
		    # theta_of_peak_zeroed_intensity=[]
		
		    # for ii in range(c3,c4):
		        # theta_of_peak.append(theta[ii])
		        # peak.append(intensity[ii])
		        
		        # theta_of_peak_zeroed_intensity.append(0)
		    # iix=ii-len(peak)
		    # intensity=intensity[0:iix]+theta_of_peak_zeroed_intensity+intensity[ii:]
		    
		    # #if r==0:    #saving the first peak data6
		    # each_peak=[theta_of_peak,peak]
		    # each_peak_peak.append(each_peak)
		    # mittel=c2_value
		        
		    # for oo in range(0,len(each_peak[0])):
		        # x.append(float(each_peak[0][oo]))
		        # yn.append(float(each_peak[1][oo]))
		    # x=asarray(x)
		    # yn=asarray(yn)
		    # def funk(x,A,mu,sigma):
		        # #print A,mu,sigma
		        # return A*exp(-(x-mu)**2/(2.*sigma**2))
		    # a=max(each_peak[1])        
		    # p0=[a,mittel,0.7]
		    # popt, pcov=curve_fit(funk,x,yn,p0=p0)
		
		    # x1=linspace(mittel-0.3,mittel+0.3,1000)
		    # fitted_curve=funk(x1,popt[0],popt[1],popt[2])
		
		    
		    
		# #show individually in each window one peak 
		# #   fig1=figure(str(c2_value))
		# #   #plot (theta_of_peak,peak,'ro:')
		# #   plot(each_peak[0],each_peak[1],'ro:')
		# #   plot(x1,fitted_curve,'k^:')
		# #   #legend([popt[1]])
		# #   legend([str(c2_value),popt[1]])
		# #   plt.show()

		    # peak_pos.append(popt[1])
		    # del(x)
		    # del(yn)
		    # del(each_peak)
		
		# peak_pos=sorted(peak_pos,key=int)
		# differens=map(sub,nist_standard,peak_pos)
		# difference=[]
		# for iii in range(0,len(peak_pos)):
		    # difference.append(float(format(differens[iii],'.3f')))
		
		# #show all together
		# #fig2=figure('all')
		# #plot (theta,intensity_orig,'bo:')
		# #plot (theta_of_peak,peak,'ro:')
		# #plot (theta, intensity,'g^:')
		
		# fig3=figure('difference')
		# bar(peak_pos,difference,width=1)
		# #plot(peak_pos,difference,'ro:')
		
		# #fig4=figure('first peak')
		# #plot(each_peak[0],each_peak[1],'ro:')
		# #plot(x1,fitted_curve,'k^:')
		# #legend([popt[1]])
		
		# plt.show()
		# self.ui.lepic.setPixmap(QtGui.QPixmap("Chicken_small2.png"))
	
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = GUIForm()
    myapp.show()
    sys.exit(app.exec_())
