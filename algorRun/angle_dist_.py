import numpy as np
import pandas as pa
import sys

# the filename of the *.dat in the folder is forwarded 
# it is used to generate the row names of the json file 
# as well as the name of the pandas dataframe at the save

ab=sys.argv[1]
f=open(ab)
d=f.readlines()
f.close()

#[i.split()[1].split('(')[0].split(')')[0] for i in d]

def check_decimal(d):
	"""
	Practically impossible to do it this way, 
	1.530 will be indistinwichable from 1.533
	round(mod()) combination is also unfluitful 
	Insted treat the standard deviation notation 
	as a string, like in the :

	check_decimal_as_string()

	"""	
	std=[]
	dd=lambda x: 10**x
	for m in d:
		for t in range(1,len(m.split())):
			for k in map(dd,range(0,20)):
				if mod(mod(float(m.split()[t].split('(')[0].split(')')[0])*k,k),1)==0:
					break
#				if mod(float(m.split()[t].split('(')[0].split(')')[0]) *k,10) >0:
#					if mod(float(m.split()[t].split('(')[0].split(')')[0]) *k,1)==0:
#						break
			std.append(float(m.split()[t].split('(')[1].split(')')[0])/k)
	return std

def check_decimal_as_string(d):
	"""
	The argument is the whole file as a list 
	read using readline 
	Transform a notation as:
	1.530(3) 
	1.533(4) into 
	a value and a standard deviation 
	1.53 and 0.003 
	1.533 and 0.004
		
	"""
	std=[]
	dd=lambda x: 10**x
	for m in d:
		for t in range(1,len(m.split())):
			a=len(m.split()[t].split('(')[0].split(')')[0].split('.')[1])
			std.append(float(m.split()[t].split('(')[1].split(')')[0])/10**a)
	return std


def clean_std_formatting(element):
	"""
	takes a string formatted value and std as:
	1.530(4) 
	and returns a list of floats 
	[1.53,0.004]
	"""	
	d=len(element.split('(')[0].split('.')[1])
	a=float(element.split('(')[0])	
	s=float(element.split('(')[1].split(')')[0])/10**d
	return list([a,s])

#---------------

#indx=[i.split()[0] for i in d]	
#create the dataframe
#df=pa.DataFrame(index=indx)
df=pa.DataFrame()
row_name=f.name
json_fname=f.name+'.json'
for m in range(0,len(d)):
	#print d
	#print d[m]
	#print m
	
	# put the 'angle' into the DataFrame

	col_name_0     = d[0].split()[0].split('-')[0] + '-' +d[m].split()[0].split('-')[2]+' angle'	
	col_name_0_err = col_name_0+'err'
	val_err_0      = clean_std_formatting(d[m].split()[1])
	df.loc[row_name,col_name_0]=val_err_0[0]
	df.loc[row_name,col_name_0]=val_err_0[1]	

	# put there 'distances' into the DataFrame

	col_name_1 = d[m].split()[0].split('-')[0]+ '-' +d[m].split()[0].split('-')[1]
	col_name_1_err = col_name_1+'_err'
	val_err_1 = clean_std_formatting(d[m].split()[2])
	df.loc[row_name,col_name_1]=val_err_1[0]
	df.loc[row_name,col_name_1_err]=val_err_1[1]
	
	col_name_2 = d[m].split()[0].split('-')[1]+ '-' +d[m].split()[0].split('-')[2]
	col_name_2_err = col_name_2+'_err'
	val_err_2 = clean_std_formatting(d[m].split()[3])
	df.loc[row_name,col_name_2]=val_err_2[0]
	df.loc[row_name,col_name_2_err]=val_err_2[1]

	col_name_3 = d[m].split()[0].split('-')[0]+ '-' +d[m].split()[0].split('-')[2]
	col_name_3_err = col_name_3+'_err'
	val_err_3 = clean_std_formatting(d[m].split()[4])
	df.loc[row_name,col_name_3]=val_err_3[0]
	df.loc[row_name,col_name_3_err]=val_err_3[1]

df.to_json(json_fname)



		
