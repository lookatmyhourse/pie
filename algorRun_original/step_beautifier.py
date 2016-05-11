import numpy as np
import os, sys,re

"""
-to analyse the *.ctrl file, organize the steps in correct form 
-to set up the ctrl file for parametrized refinement 
	+ create a txt file with #step par columns


Setting up the control file could be tedious, especially when a series 
of values is desired to be put in step sequence. An automated way of generating 
the ctrl file in needed. Here a small number of methods for this are given. 
These methods have the function to generate an organized sequence of steps where the 
keyword parameters are assigned values following a chosen function. 
The initial and end value limits are needed as well as a function, for example a linear 
range of values from A to B. However this range could be made logarithmic, exponential or any 
other needed. 

"""

class step_generator():
	"""
	Methods:
	-parametrize
		for seting up the ctrl file 
	"""
	def __init__(self):
		pass

	def parameterize(self,
			c1_phase,
			c2_which_parameter,
			c4_ref_code,
			value_limit_lower,
			value_limit_higher,
			number_of_datapoints,
			ctrl_filename):
		#
		"""
		expected input:
		-which_parameter: keyword of the parameter to be investigated
		-value_limit_lower    : starting guess point 
		-value_limit_higher   : starting guess point 
		-number_of_data points : number of refinements/steps in the range
		-function             : the behaviour of the influence quantity 
					example liner change y*k+b, where k and b are given
					by numbers here
		-ctrl_filename        : the filename out the *.ctrl file to be generated 

		=====
		function : this has to be done differently. Turning a string into an equation for python
			does not sound like a good idea to do. The string could be anything "x*2+sin(x)" 
			which would be a nightmare to examine and convert
		>>	instead,
			take the string that is dropped here, and generate a py file with it, as a string
			and execute it
		>>	however the problem remains 
			the formulation (syntax) of the equation must be that of python's.
		>>	consider 
			leaving the user to directly modify this code, let the user type in directly into
			this .py file
			make a default as a linear range and make it clear where to change it and give 
			short declaration about python syntax (basics in a few comment lines)

		example:
		parameterize(1,Zero,0.0,-0.004,0.01,50,ctrl_par_auto)
			which will render to 
			#step_n (where there will be 50 steps)
			c1=1
			c2=Zero
			c3= (values between -0.004 and 0.01)
			c4=0.0 

		"""

		# the range 
		x=np.linspace(value_limit_lower,value_limit_higher,number_of_datapoints)
		#___________________________________________________________
		#		  |>function________________________________|
		function=lambda x : x*1+0	# define your own function  |
		#		  |_________________________________________|
		#___________________________________________________________|
		values=function(x)


		f=open(ctrl_filename+'.ctrl','w')
		g=open(ctrl_filename+'_step_col_val.txt','w')
		g.writelines('#step   '+str(c2_which_parameter)+'\n')
		for i in range(0,len(values)):
			if values[i] < value_limit_higher:
				#write the file
				f.writelines(str('#step_'+str(i+1))+'\n')
				f.writelines(str('c1=')+str(c1_phase)+'\n')
				f.writelines(str('c2=')+str(c2_which_parameter)+'\n')
				f.writelines(str('c3=')+str(values[i])+'\n')
				f.writelines(str('c4=')+str(c4_ref_code)+'\n')
				f.writelines('\n')
				g.writelines(str(i+1)+'\t'+str(values[i])+'\n')
				
		f.close()
		g.close()


class step_beautifier():
	"""
	This class contains methods to check the step sequence correctness and 
	make changes if needed. Example of syntax mistakes, repeating step numbers etc.
	
	"""	
	def step_beautifier():
		#
		pass

#----------------------------------------------------------------------------------------

# for the zero shift test in the Si standard material dataset 
#step_generator().parameterize(1,'Zero',0.0,-0.01,-0.001,50,'ctrl_par_auto_2')



# for the 
# /home/mnost/Public/testt/test_pcrEdit_/test_Mo_Jan_2016/TN1_test/parametrisation_5h/ctrl_6_safe_TN1_600C_5h_3000s00
step_generator().parameterize(1,'SyCos',0.0,-0.03,0.03,50,'TESTTTTT')
