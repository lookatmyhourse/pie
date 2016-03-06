#from pylab import *
import numpy as np
import sympy as sp
from sympy.utilities import lambdify
import matplotlib.pyplot as plt

"""
finding the extreme value of an analitcal function 
through first derivative 
"""
						#DONE -># need more the global minimum (i.e. to 
							# 	finish to go through the whole 
							#	arange) 
							
"""
interesting functions 
--------------------------------------------------------------------------------------------
NEW 
functions tested 23.07.2014
f_min(1/3.*x**3-2*x**2-5*x,-10,10,0.001)

from the site about basinhopping in scipy.optimize 
f_min(sp.cos(14.5*x-0.3)+(x+0.2)*x,-2,2,0.0001)


				REMARK!
				keep the near_zero value to 0.01 and explore with stp instead!
				near_zero == area where dy=0 
				// -near_zero < dy==0 < +near_zero //

f_min(sp.sin(x**2)+x**2,-3,1,0.01)  - it has a local and global minima in this region

f_min(sp.sin(x)*x,-15,15,0.01)  VERY INTERESTING 
				when set the stp to 0.001 it finds more extreme points 
				f_min(sp.sin(x)*x,-15,15,0.001)
				VERY IMPORTANT keep the near_zero value 0.01 so that the step 
				size (stp) can go to 0.001 
				(with stp=0.0001 and near_zero of 0.001 -> it crashes)
also 
f_min(1-(sp.sin(x)/x,-15,15,0.1)
and 				when to value of near_zero is 0.01 is better then 0.001
f_min(1-(sp.sin(x)/x,-15,15,0.01)

f_min(x**2+x,-1,1,0.1)
f_min(x**2+x*3,-10,10,0.01)

f_min(1-sp.sin(x)/x,-15,15,0.01)

f_min(sp.sin(x)/x,-15,15,0.01) also with stp=0.001  ! 
--------------------------------------------------------------------------------------------
"""

x=sp.Symbol('x')
def f_min(y,mi,mx,stp):
	"""
	y  - form of analytical function 
	mi - plot and analyze in interval starting from this value 
	mx - plot and alalyze in interval ending with this value 
	stp- stepsize on the x axis. (with a little imagination it can be 
		considered as resolution 
	"""
	fd=[];d={}
	t=np.arange(mi,mx,stp)
	ly=lambdify(x,y)
	dy=y.diff()
	ldy=lambdify(x,dy)
	
	print 'Analitical function:    ',y
	print 'first derivative:       ',dy
	
	for i in np.arange(mi,mx,stp):
		# searhing where the first derivative is zero OR NEAR ZERO! 
		# /technically the same way can be done with lambdify 
		if -0.01 < dy.subs(x,i).evalf() < 0.01:
			yy=y.subs(x,i).evalf()
			print 'local extreme at (x,y):  (%s,  %s)' %(i,yy)
			d[yy]=i
	ix=max(d.keys())
	ixmin=min(d.keys())
	iy=d.get(ix)
	iymin=d.get(ixmin)
	print ' '	
	print 'Global minimum at (x,y): (%s,  %s) ' %(iymin,ixmin)
	print 'Global maximum at (x,y): (%s,  %s) ' %(iy,ix)
	
	plt.figure('minimi')
	o1=[];o2=[]
	for ii in np.arange(mi,mx,stp):
		o1.append(ly(ii))
		o2.append(ldy(ii))   # the plot option below 
#	plt.plot(t,ly(np.arange(mi,mx,stp)))
	plt.plot(t,o1)
#	plt.plot(t,ldy(np.arange(mi,mx,stp)))
	plt.plot(t,o2)
	plt.plot(iy,ix,'ro',iymin,ixmin,'bo')
	plt.legend(['y= %s'%y,'dy= %s' %dy, 'extreme point global max','extreme point global min'])
	plt.show()

