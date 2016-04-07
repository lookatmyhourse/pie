#! /usr/bin/env python

import re, os, sys, shutil, subprocess, time
import numpy as np
#------------------------------------------------------------------------------

class search_tools():
	"""
	General search tools 
	"""
	def findall(self,x,y):
		s=[]
		for i in range(0,len(y)):
			xx=[m.start for m in re.finditer(x,y[i])]
			if len(xx)>0:
				s.append(y[i].replace('\n',''))
		return s
	def findall_with_index(self,x,y):
		s=[]
		for i in range(0,len(y)):
			xx=[m.start for m in re.finditer(x,y[i])]
			if len(xx)>0:
				s.append((i,y[i].replace('\n','')))
		return s
	def grep_AB(self,what,from_where,how_many_lines):
		s=from_where
		n=how_many_lines
		return s[(s.index(self.findall(what,s)[-1]+'\n')+0):(s.index(self.findall(what,s)[-1]+'\n')+n)]
		
	def grep_index(self,what,from_where,how_many_lines):
		s=from_where
		n=how_many_lines
		return s[self.findall_with_index(what,s)[-1][0]:self.findall_with_index(what,s)[-1][0]+n]

	def find_index_only(self,what,from_where):
		"""
		returns only the index of the occurance of "what" in the whole readline generated array of string lists 
		"""
		s=[]
		for i in range(0,len(from_where)):
				xx=[m.start() for m in re.finditer(what,from_where[i])]
				if len(xx)>0:
					s.append(i)
		return s


	def find_exact_word(self,what,where):
		"""
		matches the exact keyword remaining case sencitive 
		also returns of the index of the first character of the 'what' word 
		
		"""
		ss='\\b'+str(what)+'\\b' # the \\b are bounderies
		#print re.findall(ss,where)
		# return the index of the exact match 
		xx=[m.start() for m in re.finditer(ss,where)]
		#print "%s and it's index is starts at : %s" %( re.findall(ss,where), xx)
		return xx

	def find_file_with_extension(self,what):
		"""
		finds a file by it's extension in the cwd
		if t>0:
			#there is a *.ext name file in the cwd
		"""
		t=0
		for i in os.listdir(os.getcwd()):
			if search_tools().find_exact_word(what,i.split('.')[-1]) != []:
				t+=1
		return t

#d[findall_with_index('RELIABILITY FACTORS FOR',d)[-1][0]:findall_with_index('RELIABILITY FACTORS FOR',d)[-1][0]+8]
#------------------------------------------------------------------------------

class analyze():
	"""
	"""
	
	def create_result_files(self):
		ahead_1='%-11.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s\n' % ('step#','a','a_err','c','c_err','vol','vol_err','w','w_err')
		ahead_2='%-11.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s %-10.7s\n' % ('step#','Rp','Rwp','Re','Chi2','Deviance','Dev_star','Gof','Npar','Bragg_R_factor_ph1','Rf_factor_ph1')
		f=file('results_1_lattice.txt','w')
		#f=file('results_1_lattice.csv','w')
		f.write(ahead_1)
		f.close()
		f=file('results_2_Rs.txt','w')
		f.write(ahead_2)
		f.close()

	def results_to_file(self,c1,c2):
		def findall(x,y):
			s=[]
			for i in range(0,len(y)):
				xx=[m.start for m in re.finditer(x,y[i])]
				if len(xx)>0:
					s.append(y[i].replace('\n',''))
			return s
		match_cell_a=' :      Cell_A_ph1_pat1'
		match_cell_a_pcr='!-------> Profile Parameters for Pattern #  1\n'
		match_cell_c=' :      Cell_C_ph1_pat1'
		match_vol='BRAGG.*R-Factor.*and.*weight.*fractions.*for.*Pattern' #needs '\n'; re.findite removes \n
		
		#generate the *.out filename from the *.pcr 
		out=c1.split('.')[0]+'.out'
		f=open(out)
		d=f.readlines(); f.close()

		f=open(c1)
		p=f.readlines();f.close()

		#lattice
		if findall(match_cell_a,d)==[]:
			# the a parameter was not refined 
			# take value of a from *.pcr
			ppp=p[p.index((findall(' a ',p)[0]+'\n'))].split()
			cell_a=float(p[p.index((findall(' a ',p)[0]+'\n'))+1].split()[ppp.index('a')-1])
			cell_a_err=1e-16
		else:
			#take refined parameter from *.out file
			cell_a=float(findall(match_cell_a,d)[0].split(match_cell_a)[1].split('( +/-')[0])
			cell_a_err=float(findall(match_cell_a,d)[0].split(match_cell_a)[1].split('( +/-')[1].split(')')[0])

		if findall(match_cell_c,d)==[]:
			# the c parameter was not refined 
			# take value of c from *.pcr
			ppp=p[p.index((findall(' c ',p)[0]+'\n'))].split()
			cell_c=float(p[p.index((findall(' c ',p)[0]+'\n'))+1].split()[ppp.index('c')-1])
			cell_c_err=1e-16
		else:
			# take refined parameter from *.out file 
			cell_c=float(findall(match_cell_c,d)[0].split(match_cell_c)[1].split('( +/-')[0])
			cell_c_err=float(findall(match_cell_c,d)[0].split(match_cell_c)[1].split('( +/-')[1].split(')')[0])

		#volume
		vol_indx=d.index('     BRAGG R-Factors and weight fractions for Pattern #  1\n')
		vol=float(findall('Vol',d[vol_indx:vol_indx+6])[0].split('Vol:')[1].split('(')[0])
		vol_err=float(findall('Vol',d[vol_indx:vol_indx+6])[0].split('Vol:')[1].split('(')[1].split(')')[0])
		weight_fract_ph1=float(findall('Vol',d[vol_indx:vol_indx+6])[0].split('Vol:')[1].split('(')[2].split(':')[1])
		weight_fract_ph1_err=float(findall('Vol',d[vol_indx:vol_indx+6])[0].split('Vol:')[1].split('(')[3].split(')')[0])

		#a=np.array([[cell_a,cell_a_err,cell_c,cell_c_err,vol,vol_err,weight_fract_ph1,weight_fract_ph1_err]])
		a=np.array([[float(c2+1),cell_a,cell_a_err,cell_c,cell_c_err,vol,vol_err,weight_fract_ph1,weight_fract_ph1_err]])
		f=file('results_1_lattice.txt','a')
		np.savetxt(f,a,fmt='%10.7f')
		#np.savetxt(f,a,fmt='%10.7f',header=ahead)
		f.close()
#	def results_to_file_R_Chi_Bragg_Rf():
		#global reliability of the whole fit 
		r1=search_tools().grep_index('=> Conventional Rietveld',d,1)
		r2=search_tools().grep_index('RELIABILITY FACTORS FOR',d,6)
		Rp=float(r1[0].split()[6])
		Rwp=float(r1[0].split()[7])
		Re=float(r1[0].split()[8])
		Chi2=float(r1[0].split()[9])

		Deviance=float(r2[4].split()[3])
		Dev_star=float(r2[4].split()[5])
		GoF=float(r2[5].split()[2])
		
		# NUMBER OF PHASES
		# NUMBER OF PARAMETERS 
		Npar=float(search_tools().grep_AB('Number of Least-Squares parameters',d,1)[0].split()[-1])

		# structure R-factors 
		r3=search_tools().grep_index(' BRAGG R-Factors and weight fractions for Pattern #  1',d,10)
		r33=search_tools().grep_index('Phase:  1',r3,3)
		Bragg_R_factor_ph1=float(r33[1].split()[3])
		Rf_factor_ph1=float(r33[2].split()[2])
		
		#storing to a file 
		a=np.array([[float(c2+1),Rp,Rwp,Re,Chi2,Deviance,Dev_star,GoF,Npar,Bragg_R_factor_ph1,Rf_factor_ph1]])
		f=file('results_2_Rs.txt','a')
		np.savetxt(f,a,fmt='%10.4f')
		f.close()	



class atomic_parameters():
	"""
	Methods for changing the atomic parameter values and codes
		a_middle[10].split()[0]
	values			[0] : Atom name 
				[1] : atom type
				[2] : x pos
				[3] : y pos
				[4] : z pos
				[5] : Biso
				[6] : occ
	codes
		a_middle[10+1].split()[0] : code for x pos
				      [1] : code for y pos
				      [2] : code for z pos
				      [3] : code for Biso
				      [4] : code for Occ
	"""
	def change_Biso(self,pcr_filename,codeword,val,code):
		"""
		Biso(pcr_filename,codeword,val,code)

		"""
		f=open(pcr_filename)
		a=f.readlines()
		f.close()
		a_index=search_tools().find_index_only('Atom',a)
		
		a_end_index=search_tools().find_index_only('Profile Parameters',a)
		
		pre_a=a[:a_index[0]+1]
		post_a=a[a_end_index[0]:]
		
		a_middle=a[a_index[0]+1:a_end_index[0]]

		#=======

		#values change

		cw=codeword.split('Biso')[0] # split the codeword 
		cwp=search_tools().find_index_only(cw,a_middle)  #search for the index where the atom type is Ca1
		a_middle_ch=a_middle[cwp[0]].split()
		a_middle_ch_code=a_middle[cwp[0]+1].split()

		if val != '!':
			a_middle_ch[5] = str(val)  				# the 6th [5] element is the Biso values 
			changed_line='  '.join(a_middle_ch)+'\n'
		else:
			changed_line=a_middle[cwp[0]]
		if code !='!':
			a_middle_ch_code[3] =str(code)				# the 4th [3] element is the Biso code 
			changed_line_codeline='      '+'  '.join(a_middle_ch_code)+'\n'
		else:
			changed_line_codeline=a_middle[cwp[0]+1]
	
		#return a_middle

		# building back up the section
		f=open(pcr_filename,'w')
		f.writelines(pre_a)
		f.writelines(a_middle[:cwp[0]])
		f.writelines(changed_line)
		f.writelines(changed_line_codeline)
		f.writelines(a_middle[cwp[0]+2:])
		f.writelines(post_a)
		f.close()


	def change_occ(self,pcr_filename,codeword,val,code):
		"""
		occ(pcr_filename,codeword,val,code)

		"""
		f=open(pcr_filename)
		a=f.readlines()
		f.close()
		a_index=search_tools().find_index_only('Atom',a)

		a_end_index=search_tools().find_index_only('Profile Parameters',a)
		
		pre_a=a[:a_index[0]+1]
		post_a=a[a_end_index[0]:]
		
		a_middle=a[a_index[0]+1:a_end_index[0]]

		#=======

		#values change

		cw=codeword.split('Occ')[0] # split the codeword 
		cwp=search_tools().find_index_only(cw,a_middle)  #search for the index where the atom type is Ca1
		a_middle_ch=a_middle[cwp[0]].split()
		a_middle_ch_code=a_middle[cwp[0]+1].split()

		if val != '!':
			a_middle_ch[6] = str(val)     			 # the 7th [6] element is the Occ values 
			changed_line='  '.join(a_middle_ch)+'\n'
		else:
			changed_line=a_middle[cwp[0]]
		if code !='!':
			a_middle_ch_code[4] =str(code) 			 # the 5th [4] element is the Occ code
			changed_line_codeline='      '+'  '.join(a_middle_ch_code)+'\n'
		else:
			changed_line_codeline=a_middle[cwp[0]+1]
	
		#return a_middle

		# building back up the section
		f=open(pcr_filename,'w')
		f.writelines(pre_a)
		f.writelines(a_middle[:cwp[0]])
		f.writelines(changed_line)
		f.writelines(changed_line_codeline)
		f.writelines(a_middle[cwp[0]+2:])
		f.writelines(post_a)
		f.close()

	def change_Xpos(self,pcr_filename,codeword,val,code):
		"""
		Xpos(pcr_filename,codeword,val,code)

		"""
		f=open(pcr_filename)
		a=f.readlines()
		f.close()
		a_index=search_tools().find_index_only('Atom',a)
		
		a_end_index=search_tools().find_index_only('Profile Parameters',a)
		
		pre_a=a[:a_index[0]+1]
		post_a=a[a_end_index[0]:]
		
		a_middle=a[a_index[0]+1:a_end_index[0]]

		#=======

		#values change

		cw=codeword.split('X')[0] # split the codeword 
		cwp=search_tools().find_index_only(cw,a_middle)  #search for the index where the atom type is Ca1
		a_middle_ch=a_middle[cwp[0]].split()
		a_middle_ch_code=a_middle[cwp[0]+1].split()

		if val != '!':
			a_middle_ch[2] = str(val)  				# the 3th [2] element is the Biso values 
			changed_line='  '.join(a_middle_ch)+'\n'
		else:
			changed_line=a_middle[cwp[0]]
		if code !='!':
			a_middle_ch_code[0] =str(code)				# the 1th [0] element is the Biso code 
			changed_line_codeline='      '+'  '.join(a_middle_ch_code)+'\n'
		else:
			changed_line_codeline=a_middle[cwp[0]+1]
	
		#return a_middle

		# building back up the section
		f=open(pcr_filename,'w')
		f.writelines(pre_a)
		f.writelines(a_middle[:cwp[0]])
		f.writelines(changed_line)
		f.writelines(changed_line_codeline)
		f.writelines(a_middle[cwp[0]+2:])
		f.writelines(post_a)
		f.close()


	def change_Ypos(self,pcr_filename,codeword,val,code):
		"""
		Ypos(pcr_filename,codeword,val,code)

		"""
		f=open(pcr_filename)
		a=f.readlines()
		f.close()
		a_index=search_tools().find_index_only('Atom',a)
		
		#nat=search_tools().find_index_only('Nat',a)+1 #the line below the Nat
		#nat=int(b[search_tools().find_index_only('Nat',b)[0]+1].split()[0])  #integer number of the atoms to 
										     #determine the length of the 
		a_end_index=search_tools().find_index_only('Profile Parameters',a)
		
		pre_a=a[:a_index[0]+1]
		post_a=a[a_end_index[0]:]
		
		a_middle=a[a_index[0]+1:a_end_index[0]]

		#=======

		#values change

		cw=codeword.split('Y')[0] # split the codeword 
		cwp=search_tools().find_index_only(cw,a_middle)  #search for the index where the atom type is Ca1
		a_middle_ch=a_middle[cwp[0]].split()
		a_middle_ch_code=a_middle[cwp[0]+1].split()

		if val != '!':
			a_middle_ch[3] = str(val)  				# the 4th [3] element is the Biso values 
			changed_line='  '.join(a_middle_ch)+'\n'
		else:
			changed_line=a_middle[cwp[0]]
		if code !='!':
			a_middle_ch_code[1] =str(code)				# the 2th [1] element is the Biso code 
			changed_line_codeline='      '+'  '.join(a_middle_ch_code)+'\n'
		else:
			changed_line_codeline=a_middle[cwp[0]+1]
	
		#return a_middle

		# building back up the section
		f=open(pcr_filename,'w')
		f.writelines(pre_a)
		f.writelines(a_middle[:cwp[0]])
		f.writelines(changed_line)
		f.writelines(changed_line_codeline)
		f.writelines(a_middle[cwp[0]+2:])
		f.writelines(post_a)
		f.close()


	def change_Zpos(self,pcr_filename,codeword,val,code):
		"""
		Zpospcr_filename,codeword,val,code)

		"""
		f=open(pcr_filename)
		a=f.readlines()
		f.close()
		a_index=search_tools().find_index_only('Atom',a)
		
		#nat=search_tools().find_index_only('Nat',a)+1 #the line below the Nat
		#nat=int(b[search_tools().find_index_only('Nat',b)[0]+1].split()[0])  #integer number of the atoms to 
										     #determine the length of the 
		a_end_index=search_tools().find_index_only('Profile Parameters',a)
		
		pre_a=a[:a_index[0]+1]
		post_a=a[a_end_index[0]:]
		
		a_middle=a[a_index[0]+1:a_end_index[0]]

		#=======

		#values change

		cw=codeword.split('Z')[0] # split the codeword 
		cwp=search_tools().find_index_only(cw,a_middle)  #search for the index where the atom type is Ca1
		a_middle_ch=a_middle[cwp[0]].split()
		a_middle_ch_code=a_middle[cwp[0]+1].split()

		if val != '!':
			a_middle_ch[4] = str(val)  				# the 5th [4] element is the Biso values 
			changed_line='  '.join(a_middle_ch)+'\n'
		else:
			changed_line=a_middle[cwp[0]]
		if code !='!':
			a_middle_ch_code[2] =str(code)				# the 3th [2] element is the Biso code 
			changed_line_codeline='      '+'  '.join(a_middle_ch_code)+'\n'
		else:
			changed_line_codeline=a_middle[cwp[0]+1]
	
		#return a_middle

		# building back up the section
		f=open(pcr_filename,'w')
		f.writelines(pre_a)
		f.writelines(a_middle[:cwp[0]])
		f.writelines(changed_line)
		f.writelines(changed_line_codeline)
		f.writelines(a_middle[cwp[0]+2:])
		f.writelines(post_a)
		f.close()



class displacement_parameters():
	"""
	zero shift 
	Sycos
	SySin

	"""
	def displacement(self,pcr_filename,codeword,val,code):
		"""
		Zero(pcr_filename,codeword,val,code)

		"""
		f=open(pcr_filename)
		d=f.readlines()
		f.close()
		d_index=search_tools().find_index_only('Zero',d)
			
		pre_d=d[:d_index[0]+1]
		post_d=d[d_index[0]+2:]
		
		d_middle=d[d_index[0]+1]
		d_middle_ch=d_middle.split() # divide the string to the list by the whitespace 
		#=======

		#search for the displacement codeword 'Zero'
		if codeword.find('Zero') >=0:
			# value 
			if val != '!':
				d_middle_ch[0]=str(val)
				changed_line='  '.join(d_middle_ch)+'\n'
			else: 
				changed_line=d_middle
			changed_line_code=changed_line.split()
			#	
			#this renaming is needed since the same sigle line is modified by the val and by the code 
			# they operate one after another on the same line 
			#
			# code
			if code != '!':
				changed_line_code[1]=str(code)
				changed_line='  '.join(changed_line_code)+'\n'
			else:
				changed_line=changed_line_code
		
		#search for the displacement codeword 'SyCos'
		if codeword.find('SyCos') >=0:
			# value 
			if val != '!':
				d_middle_ch[2]=str(val)
				changed_line='  '.join(d_middle_ch)+'\n'
			else: 
				changed_line=d_middle
			changed_line_code=changed_line.split()
			# code
			if code != '!':
				changed_line_code[3]=str(code)
				changed_line='  '.join(changed_line_code)+'\n'
			else:
				changed_line=changed_line_code

		#search for the displacement codeword 'SySin'
		if codeword.find('SySin') >=0:
			# value 
			if val != '!':
				d_middle_ch[4]=str(val)
				changed_line='  '.join(d_middle_ch)+'\n'
			else: 
				changed_line=d_middle
			changed_line_code=changed_line.split()
			# code
			if code != '!':
				changed_line_code[5]=str(code)
				changed_line='  '.join(changed_line_code)+'\n'
			else:
				changed_line=changed_line_code


		# building back up the section
		f=open(pcr_filename,'w')
		f.writelines(pre_d)
		f.writelines(changed_line)
		f.writelines(post_d)
		f.close()





#------------------------------------------------------------------------------

def fill_arr(r):
	a=analyse_each_step_array(r)
	for i in range(1,len(r)):
		a[i-1][:]=r[i].strip()[3:].split(',')
	return a



#get the folders and files in the path and selects only the files without the folders 
# this would be 'ignore'-ed when using the shutil.copytree 
#def copytree_files_in_cwd(step):
#	def ig_f(dir, files):
#		return [f for f in files if os.path.isdir(os.path.join(dir, f))]
#	shutil.copytree(os.getcwd(),step,ignore=ig_f)
def copy_file_no_dirs_to_dir(xxx):
	def ig_f(dir,files):
		return [f for f in files if os.path.isdir(os.path.join(dir,f))]
	shutil.copytree(os.getcwd(),xxx,ignore=ig_f)


#this function takes the r[0]..r[5] - the step and return the step name " step n "
def get_stepname(r_step):	
	step=r_step[0].strip()[1:]
	return step

def findall(x,y):
	s=[]
	for i in range(0,len(y)):
		xx=[m.start for m in re.finditer(x,y[i])]
		if len(xx)>0:
			s.append(y[i].replace('\n',''))
	return s

# for r[0] or any step individual from all r steps
# THIS IS WHAT I NEED - each step separated 
def analyse_each_step_array(r):
	a=[]
	for i in r:
		if i.find(';')>0:
			if i.find(',')>0:
				#print i.count(',')
				a.append(i.count(',')+2)
				#print "; and ,"
			else:
				#print i.count(';')
				a.append(i.count(';')+1)
				#print "code;val"
		else:
			if i.find(',')>0:
				#print i.count(',')
				a.append(i.count(',')+1)
				#print "no ; but , present"
			else:
				#print "double NO"
				a.append(1)
	a=max(a)
	#arr=np.tile('0',(4,a))  # defines a string type array (dtype='|S2')
	arr=np.full((4,a),'0',dtype='|S64')  # defines a string type array (dtype='|S2')
	return arr


def read_step_and_separate(d):
	ns=len(findall("step",d))
	r=[]
	for ii in range(1,ns+1):
		stepstring='step.*'+str(ii)
		for i in d:
		    m=re.search(stepstring,i)
		    if m:
			m.string
			break
		mm=m.string
		d.index(mm)
		#take the c2 - c5 for each step
		r.append(d[d.index(mm):d.index(mm)+5])
	return r

def scale_it_up(c0):
	chi2_line='! Current global Chi2 '    
	# the aboe line has problems when the string contains parentesis or dot 
	# it causes problems for the search_tools().find_index_only method!
	f=open(c0)
	lines=f.readlines()  #*.pcr
	f.close()

	i=search_tools().find_index_only(chi2_line,lines)

	pre=lines[ : i[0]] 
	new_chi2_line='! Current global Chi2 (Bragg contrib.) =      1000000000 \n'
	post=lines[i[0]+1: ]

	f1= open(c0,'w')
	f1.writelines(pre)
	f1.writelines(new_chi2_line)
	f1.writelines(post)
	f1.close()
	

#-------------------
#the pcrEdit for conttrol_file_scheme_2.ctrl
def profile_parameters(c0,c1,c2,c2c,c3):
	"""
	c0 - pcr filename 
	c1-phase	c1=1
	c2-codeword	c2=__a
	c2c-value 	c3=! or 9.9999
	c3-code		c4=! or 9.9999

		edited on 4th.Feb.2016
	the previous state of the code was just hovering above cathastrofic, there were serious bugs
	inside 
	Now the old code is fixed, but this section could use a total rewriteing and reduction
	new name for the method  profile_parameters 		
	
	the lines section should be previously cut for the section inbetween the possible multiple 
	phases 

	"""
#1	if c2.find('_')==0:
#1		c2=c2.replace('_',' ')	
	f=open(c0)
	lines=f.readlines()  #*.pcr
	f.close()

	#ph='!-------> Profile Parameters for Pattern #  '+c1
	#ph_next='!-------> Profile Parameters for Pattern #  '+str(int(c1)+1)

	ph='!  Data for PHASE number:   '+c1
	ph_next='!  Data for PHASE number:   '+str(int(c1)+1)
	ph_section_end='!  2Th1/TOF1    2Th2/TOF2  Pattern to plot'
	ph_end=[]
	
	profil_parameters='!-------> Profile Parameters for Pattern #  '
	#print ph
	#print ph_next
	#print ph_section_end

	if search_tools().find_index_only(ph_next,lines) == []:
		#there is no second phase, or another phase after the phase c1
		ph_end=ph_section_end
	else:
		ph_end=ph_next

	#print ph_end
	#print search_tools().find_index_only(ph,lines)
	#print search_tools().find_index_only(ph_end,lines)

	#line=lines[search_tools().find_index_only(ph,lines)[0] : search_tools().find_index_only(ph_end,lines)[0]+2]
	phase_section=lines[search_tools().find_index_only(ph,lines)[0] : search_tools().find_index_only(ph_end,lines)[0]+2]

	line=phase_section[search_tools().find_index_only(profil_parameters,phase_section)[0] : ]
	

	#---------
	#_1__find all the lines that contain the codeword ($c2)
	#---------
#1	ln=[]
#1	for i in range(0,len(line)):
#1		xx=[m.start() for m in re.finditer(c2,line[i])]
#1		if len(xx)>0:
#1			ln.append(i)

	line_of_interest=[(search_tools().find_exact_word(c2,line[i]),i) for i in range(0,len(line)) if search_tools().find_exact_word(c2,line[i]) != [] ] # returns a list where the first element the position of the kewword, the second element is the line index where the keyword is 
	o=line_of_interest[0][0][0] # the starting index of the keyword
	sel=line_of_interest[0][1]  # the index of the line where the keyword resides 

	#---------
	#_2__focus only on the phase of interest ($c1)
	#    sel is the line number for the phase 1 or 2 
	#---------
#1	if c1=='1':
#1		sel=ln[0]
#1	if c1=='2':
#1		sel=ln[1]      
#1	sel=ln[int(c1)-1]
	#---------
	#_3__match the line below using 'sel', and count till the 
	#    whitespaces 
	#    a,b are the indexes in the string for the first occurance
	#    of the whitespace; they are found separatelly, since they
	#    are not nessesarelly the same character away from the codeword
	#    in one line above 
	#    when a(b) is found 'break'-out from the loop, don't seek further
	#---------
#1	o=line[sel].find(c2)
#2	o=[search_tools().find_exact_word(c2,i) for i in line if search_tools().find_exact_word(c2,i)!=[]] #finds the keyword in the line and returns it's initial index
#2	o=o[0][0]
	print o
	# CASE OF VALUE
	for i in range(1,10):
		a=o-i
		if line[sel+1][a]==' ':
			#print a
			break
	for i in range(1,10):
		b=o+i
		if line[sel+1][b]==' ':
			#print b
			break
	#---------
	#_4__ change the line "$c3" and put the new pcr together
	#     save it in a '___new.pcr' file 
	#---------
#	# CASE OF VALUE CHANGE
#	if c2c=='val':
#		beforeLine=line[0:sel+1]
#		afterLine=line[sel+2:]
#		beforeLine.append(line[sel+1][0:a+1]+c3+line[sel+1][b:])
#		#beforeLine.append(chh)                     # to append a str to a list 
#		newline=beforeLine+afterLine                # to concatenate two lists
#
#	# CASE OF CODE CHANGE
#	if c2c=='code':
#		beforeLine=line[0:sel+2]
#		afterLine=line[sel+3:]
#		beforeLine.append(line[sel+2][0:a+3]+c3+line[sel+2][b:])
#		#beforeLine.append(chh)                     # to append a str to a list 
#		newline=beforeLine+afterLine                # to concatenate two lists

#--------control file scheme with "!" for unchanged parameter (value/code)
	# if c2c of c3 contain the ! then leave parameter unchanged
	# else change the c2c to the value that c2c has 
	# and change the c3 to the values that c3 has 
	orig_val_len=len(line[sel+1][a+1:b])
	# CASE OF VALUE CHANGE
	if c2c=='!':
		beforeLine=line[0:sel+1]
		afterLine=line[sel+2:]
		beforeLine.append(line[sel+1][:])
		newline=beforeLine+afterLine                # to concatenate two lists
	else:
		beforeLine=line[0:sel+1]
		afterLine=line[sel+2:]
		#--
		if len(c2c)<orig_val_len:
			nn=orig_val_len-len(c2c)
			c2c=c2c+nn*' '
		else:
			c2c=c2c.strip()[:orig_val_len]
		print c2c
		beforeLine.append(line[sel+1][0:a+1]+c2c+line[sel+1][b:])
		newline=beforeLine+afterLine                # to concatenate two lists


	line=newline 
#	print line[sel]
	



#1	o=line[sel].find(c2)	 # finds the string of the codeword and looks two lines below
	if line[sel+2][o]==' ':
#		print o
		o=o+2		 # in case the refinement code is shifted, start to look for it 
	else:
		pass
	
	# CASE OF CODE
	for i in range(1,10):
		ac=o-i
		if line[sel+2][ac]==' ':
			#print a
			break
	for i in range(1,10):
		bc=o+i
		if line[sel+2][bc]==' ':
			#print b
			break
		elif line[sel+2][bc]=='\n':	# case when the code word is at the end of the line 
			break  			# case of LorSiz code '0.000\n' 	
	
#	orig_code_len=len(line[sel+2][ac+1:bc])
	orig_code_len=bc-ac
	# CASE OF CODE CHANGE
	if c3=='!':
		beforeLine=line[0:sel+2]
		afterLine=line[sel+3:]
		beforeLine.append(line[sel+2][:])
		newline=beforeLine+afterLine                # to concatenate two lists
	else:
		beforeLine=line[0:sel+2]
		afterLine=line[sel+3:]
		#p1=orig_code_len.find('.')
		p1=line[sel+2][ac+1:bc].find('.')
		p2=c3.find('.')
		if len(c3)>orig_code_len:
#			ac=(ac+1)+(p2-p1)	# and not (ac+1)+(p2-p1)
			nn=len(c3)-orig_code_len
			#print ac,bc
			ac=ac-nn
			#bc=bc-nn
#			print orig_code_len
#			print len(c3)
#			print ac
		else:
#			ac=(ac+1)-(p2-p1)	# and not (ac+1)-(p2+p1)
			nn=orig_code_len-len(c3)
			c3=nn*' '+c3
		
		beforeLine.append(line[sel+2][0:ac]+c3+line[sel+2][bc:])    # [0:a+3] 
		newline=beforeLine+afterLine                # to concatenate two lists
#	print line[sel]
#	print line[sel+1]
#	print line[sel+2][0:ac]+c3+line[sel+2][bc:]
#		print ac,bc,p1,p2
	# the new pcr is saved with the same filename ! 

	#pre_line=lines[:search_tools().find_index_only(ph,lines)[0]]

	#phase_section=lines[search_tools().find_index_only(ph,lines)[0] : search_tools().find_index_only(ph_end,lines)[0]+2]

	#line=phase_section[search_tools().find_index_only(profil_parameters,phase_section)[0] : search_tools().find_index_only(ph_end,phase_section)[0]+2]
	
	pre_phase=lines[ : search_tools().find_index_only(ph,lines)[0]]	
	post_phase=lines[search_tools().find_index_only(ph_end,lines)[0]+2 : ]

	pre_line=phase_section[:search_tools().find_index_only(profil_parameters,phase_section)[0]]
	post_line=phase_section[search_tools().find_index_only(ph_end,phase_section)[0]+2:]
#	pre_line=lines[:search_tools().find_index_only(profil_parameters,lines)[0]]
#	post_line=lines[search_tools().find_index_only(ph_end,lines)[0]+2:]
	
	f1= open(c0,'w')
	f1.writelines(pre_phase)
	f1.writelines(pre_line)
	f1.writelines(newline)
	f1.writelines(post_line)
	f1.writelines(post_phase)
	f1.close()
#	f1= open(c0,'w')
#	f1.writelines(pre_line)
#	f1.writelines(newline)
#	f1.writelines(post_line)
#	f1.close()

#------------------------------------------------
# run_fp2k
#def run_fp2k(run_what_pcr,run_what_dat):
#	"""
#	"""
#	#run_this="fp2k "+str(run_what_pcr)+" "+str(run_what_dat)
#	run_this="fp2k "+str(run_what_pcr)+" "+str(run_what_dat)+" >> log"
##	run_this="fp2k "+str(run_what_pcr)+" "+str(run_what_dat)
##	run_this="fp2k "+str(run_what_pcr)+" "+str(run_what_dat)#+" "+"log"
#	a=subprocess.Popen(run_this, shell=True,stdout=None)
#	
#	
#	a.wait()
#	#print 'done!'


def run_fp2k(pcr,dat):
	process=subprocess.Popen(['fp2k',pcr,dat,'log'],stdout=subprocess.PIPE)
	#time.sleep(1) #wait(1s)
	"""
	the above time.sleep is chosen insted of process.wait() for the reason of 
	considering the case of a stuck process, where a wait command would simply 
	wait till eternity.
	a frequent process.poll() would tell if the command is still running or it
	is finished. Evaluating the poll()'s output can hint for how to deal with 
	the stuck process. fortunatelly fullrpof does write the *.new file before 
	it stuckes to this could be used as a cue for a process.kill() call, which 
	terminated the process and allows the code to continue or the retrun a 
	propriate error message for the user, or just simply exit the code 
	"""
	marker=0
	for i in range(0,60):
		time.sleep(1)  #wait(1s)
		if process.poll()==int or process.poll()==0:
			#True : it's done 
			print "Refinement done under %s seconds!" %i
			#process.kill()
			break
		else:
			#false : it's still running
			#if [i for i in os.listdir(os.getcwd()) if i.split('.')[-1].find('new')>=0 ] >=0:  # is there *.new in dir
			if search_tools().find_file_with_extension('new') > 0 :  # is there *.new in dir
				#True
				print 'Subprocess stuck here but *.new found!'
				print 'Program will terminate here. Check log for the type of warning occured!'
				process.kill()
				#marker=0
				sys.exit()
				break
			else:
				# case of runnig(stuck) program but no *.new file 
				print 'Subprocess running, but there is no *.new file!'
				marker=1
				pass
	if process.poll()==int or process.poll()==0 or marker==0:
		#True
		if search_tools().find_file_with_extension('new') > 0 :  # is there *.new in dir
			#True: mvvv
			print 'Refinement generated a *.new file. pcr file overwriten by *.new'
			os.rename(pcr.split('.')[0]+'.new',pcr)
		else:
			#pass
			print 'Refinement ended normally.'
	else:
		#false : the process is still running
		print """
		The program is not responding, check log file for warnings!
		"""


# end of run_fp2k
#==========================================================

# rename the *.new to *.pcr to continue with analysis 
def rename_new_to_pcr(c1):
	new=c1.split('.')[0]+'.new'
	while True:
		try:
			os.rename(new,c1)
			print "overwritten"
			break
		except OSError:
			print "No *.new found!"
			break

#def new_not_new(c1):
#	is_there_new_file=[i for i in os.listdir(os.getcwd()) if i[-5:].find('.new')>0]
#	print is_there_new_file
#	if len(is_there_new_file)>0:
#		print """
#		Fullprof generate a .new file
#		The refinement encountered a ' W A R N I N G '
#		Possible errors:
#			Singular matrix occured
#			NaN value occured
#			Negative Gaussian or Lorentzian 
#			Chi2 is bigger then the initial 
#
#		Press any key to terminate this program.
#
#		Press 'r' to rename the .new to .pcr and try to continue this refinement.
#		
#		"""
#		a=raw_input()
#		if a=='r':
#			new_renamed=c1.split('.')[0]+'.pcr'
#			os.rename(c1,new_renamed)
#		else:
#			sys.exit()
#	else:
#		pass

#- januar 28. 2016 - need to add possibility to change the bgg and atomics
# problem: bgg is a grid:
#	!   Background coefficients/codes  for Pattern#  1  (Chebychev polynomials, up to 24 coefficients)
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00        0.00        0.00        0.00
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00        0.00        0.00        0.00
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00        0.00        0.00        0.00
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00        0.00        0.00        0.00
#	!-------------------------------------------------------------------------------
#
#needs to be transfomred into something like this: 
#	!   Background coefficients/codes  for Pattern#  1  (Chebychev polynomials, up to 24 coefficients)
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		bgg1        bgg2        bgg3       bgg4        0.00        0.00
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00       bgg10        0.00        0.00
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00        0.00        0.00        0.00
#	       0.000       0.000       0.000       0.000       0.000       0.000
#		0.00        0.00        0.00        0.00        0.00        0.00
#	!-------------------------------------------------------------------------------




#as well as the atomics:

# common_line   !Atom   Typ       X        Y        Z     Biso       Occ     In Fin N_t Spc /Codes
#		P1     P       0.39000  0.36300  0.25000  0.00000   0.50000   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		O1     O       0.32300  0.47400  0.25000  0.00000   0.50000   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		O2     O       0.58600  0.48000  0.25000  0.00000   0.50000   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		O3     O       0.34300  0.25500  0.06900  0.00000   1.00000   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		Ca1    Ca      0.33330  0.66670  0.00140  0.00000   0.32667   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		Ca2    Ca      0.24800 -0.00650  0.25000  0.00000   0.48500   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		O4     O       0.00000  0.00000  0.18000  0.00000   0.17333   0   0   0    0  
#				  0.00     0.00     0.00     0.00      0.00
#		!-------> Profile Parameters for Pattern #  1
#

def bgg_section(pcr_filename,bggx,bgg_val,bgg_code):
	"""
	bggx will be the number, 2, or 3 or 1
	bgg_val is the value or '!' for no change 
	bgg_code is the code's codeword 1.00, 991.00 or 0.00	

	"""
	bggx=int(bggx.split('bgg')[-1])-1
	#b=fopen(pcr_filename,1)
		
	f=open(pcr_filename)
	b=f.readlines()
	f.close()


	bgg_index=search_tools().find_index_only('Background',b)
	
	pre_a=b[:bgg_index[0]]
	post_a=b[bgg_index[0]+9:]

	bgg=np.genfromtxt(pcr_filename,skip_header=bgg_index[0]+1,skip_footer=len(b)-(bgg_index[0]+9))
	
	val=bgg[0::2]
	codes=bgg[1::2]

	val_intuitive=val.ravel()  # this will flatten out the array and each values corresponds to bggN 
	code_intuitive=codes.ravel()

	if bgg_val != '!':
		val_intuitive[bggx]=bgg_val
	if bgg_code != '!':
		code_intuitive[bggx]=bgg_code
	
	val=val_intuitive.reshape(4,6)
	codes=code_intuitive.reshape(4,6)

	bgg_new=np.hstack((val,codes)).ravel().reshape(8,6)
	
	f=open(pcr_filename,'w')
	f.writelines(pre_a)
	f.close()

	with open(pcr_filename,'a') as f_handle:
		np.savetxt(f_handle,bgg_new,fmt='%.6s',header='! Background ',comments='')

	f=open(pcr_filename,'a')
	f.writelines(post_a)
	f.close()

def step_organizer(c3):
	a=c3
	f=open(a,'r')
	d=f.readlines()
	f.close()
	"""
	search for the "#", assigne them a number of occurance and 
	then exchange the whole line with a 
	"#step_"+i 
	syntax, 
	where i is the number of occurance of the next #step
	"""
	t=1
	for i in range(0,len(d)):
		if d[i].find('#')>-1:
			d[i]="#step_"+str(t)+'\n'
			t=t+1
	f=open(a,'w')
	f.writelines(d)
	f.close()





#------------------------------------------------------------------------------
#START_MAIN
# we are at the main_folder "cwd" 
# execute the starting python code 
# :      ___________________full_path_to____/algor_run.py _____ _____ ______
#        |                                  |                  |     |     |
# python /bin_py_classes/Algor_py_31_05_2015/algor_run.py *.pcr *.dat *.ctrl 

c1=sys.argv[1]  # the *pcr file
c2=sys.argv[2]	# the *dat file
c3=sys.argv[3]	# the *ctrl file

step_organizer(c3) #organize the steps 

f=open(c3)      # open the ctrl file
d=f.readlines() #*ctrl file 
f.close()
r=read_step_and_separate(d)

#  (c1,       aa[:,i][1], aa[:,i][2], aa[:,i][3])
#  (filename, codeword,   values,     code)


#result_folder=c3.strip()[:-5]+'_'+c2.strip()[:-4]
if os.path.isdir('_refinements')==False:
	os.mkdir('_refinements')

result_folder='./_refinements/'+c3.strip()[:-5]+'_'+c2.strip()[:-4]

#os.mkdir(c3.strip()[:-5])	# make a folder of "control_file_01"

#copy_file_no_dirs_to_dir(c3.strip()[:-5])		# NO NEED TO MAKE DIR SINCE shutil.copytree makes one
#os.chdir(c3.strip()[:-5])	# navigate to this "control_file_01" folder

# Copy ONLY the pcr,ctrl, irf (if exists) and the CURRENT DATAFILE to the "redult_folfer"
#copy_file_no_dirs_to_dir(result_folder)
os.mkdir(result_folder)
shutil.copy(c1,result_folder)
shutil.copy(c2,result_folder)
shutil.copy(c3,result_folder)
[shutil.copy(i,result_folder) for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='irf']

os.chdir(result_folder)

# now we have all the *pcr, dat, irf ,ctrl file in subfolder "control_file_01" 
# and we navigated ourselves there 
analyze().create_result_files()
for ii in r: 			# for all elements of the r  ii is then one step
	aa=fill_arr(ii)		# fill arrays with codewords 
	for i in range(0,len(aa[0])):
		# send aa[:,i] to pcrEdit  ** change pcr after it was copied
		# forward all element of the vector aa[:,i] 
		print aa[:,i]
		if aa[:,i][1].find('bgg') >=0:
			bgg_section(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
		if aa[:,i][1].find('bgg') !=0:
			if aa[:,i][1].find('Biso') >=0:
				atomic_parameters().change_Biso(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
			elif aa[:,i][1].find('Occ') >=0:
				atomic_parameters().change_occ(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
			elif aa[:,i][1].find('Xpos') >=0:
				atomic_parameters().change_Xpos(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
			elif aa[:,i][1].find('Ypos') >=0:
				atomic_parameters().change_Ypos(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
			elif aa[:,i][1].find('Zpos') >=0:
				atomic_parameters().change_Zpos(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
			elif aa[:,i][1].find('Zero') >=0 or aa[:,i][1].find('SyCos') >=0 or aa[:,i][1].find('SySin') >=0:
				displacement_parameters().displacement(c1,aa[:,i][1],aa[:,i][2],aa[:,i][3])
	
			elif aa[:,i][1].find('Scale') >=0:
				scale_it_up(c1)
				profile_parameters(c1,aa[:,i][0], aa[:,i][1], aa[:,i][2], aa[:,i][3]) #	

			else:
				profile_parameters(c1,aa[:,i][0], aa[:,i][1], aa[:,i][2], aa[:,i][3]) #	

	stepname=get_stepname(ii)
	#new_not_new(c1) 
			 # !!!!
	run_fp2k(c1,c2)  # !!!! the pcr file name is always the same! 
   			 # !!!! even though each step changes it recursively 
	#rename_new_to_pcr(c1)
	#new_not_new(c1)
	analyze().results_to_file(c1,r.index(ii))
	copy_file_no_dirs_to_dir(stepname)
	print "%s done!_______________________________________________________________" %stepname
