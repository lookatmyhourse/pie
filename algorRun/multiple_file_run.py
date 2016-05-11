import os,shutil,subprocess
import time

#dat=os.listdir('./_data_files/')
#pcr=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='pcr']
#ctrl=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='ctrl']

#for i in dat:
#	t='./_data_files/'+i
#	shutil.copy(t,os.getcwd())
#	run_this="algorRun.py "+pcr[0]+' '+i+' '+ctrl[0]
#	a=subprocess.Popen(run_this,shell=True,stdout=None)
#a.wait()
#[os.remove(i) for i in dat]



def greeting_message():
	print """
	' ________________________________________ '
	'|                                        |'
	'|        AlgorRun --version 0.1          |'
	'|                                        |'
	'|________________________________________|'
	'|New in this version:                    |'
	'| -added a version printout to the "mult-|'
	'|  iple_file_run.py" script              |'
	'| -printout not only the step number but |'
	'|  also the current dataset in the refin-|'
	'|  ement                                 |'
	'|________________________________________|'
	"""


def run_multiple_files(n,path_to_algor):
	"""
	n is the number of the simultaneously running refinements

	this is due to the subprocess.Popen() and .wait() methods
	to use more resources in order to speed up the whole refinement 
	process this number can be more then n=1 i which case the code will make 
	work through one dataset AFTER the other. 
	However to use the CPU and memory resources more, by giving n=5 or n=10, the
	subprocess.Popne will forward 5 or 10 request to the shell.
	"""
	#start_time=time.strftime('%D %H:%M:%S')

	dat=os.listdir('./_data_files/')
	pcr=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='pcr']
	ctrl=[i for i in os.listdir(os.getcwd()) if i.split('.')[-1]=='ctrl']

	c=0
	for i in dat:
		c=c+1
		t='./_data_files/'+i
		shutil.copy(t,os.getcwd())
		#run_this="python C:/algor_win_test/algorRun/algorRun.py "+pcr[0]+' '+i+' '+ctrl[0]
		run_this= path_to_algor + ' ' + pcr[0] + ' ' + i + ' ' + ctrl[0]

		a=subprocess.Popen(run_this,shell=True,stdout=None)
		if c==n:
			a.wait()
			c=0
	a.wait()
	[os.remove(i) for i in dat]
	#b=time.strftime('%D %H:%M:%S')
	#print 'start %s    end     %s' % (start_time,b)

#path_to_algor="python C:/Documents\ and\ Settings/me/My\ Documents/Public/algor_win_test/algorRun/algorRun/algorRun.py"
path_to_algor="python /home/mare/calcus/_Arch_HCOOH/algorRun/algorRun.py"

"""
DON'T USE WHITESPACE IN THE PATH WHEN THE shell=True is on ! 
the shell=True nust be on of the argument running fullprof so NO WHITESPACE IN PATH! 

The path to the 'algorRun.py' needs to be given here only once, 
At the execution of the code 'multiplt_file_run.py' is only needed to be pointed every 
time to the folder where it's located. 
"""
greeting_message()
run_multiple_files(3,path_to_algor)


