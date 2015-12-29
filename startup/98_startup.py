#! /usr/bin/env python
import os 
import numpy as np
from pylab import *

def getFiles(x):
	"""
	Lists out all the files of x extension in the current working directory (example 'txt')
	
	Same functionality as shell command ls *.xxx, but getFiles returns a list.
		
	The list of filenames t=getFiles('txt') can be used with pop to remove elements, and act on separate files as desired.
	"""
	g=os.getcwd()
	gg=os.listdir(g)
	t=[]
	for element in gg:
		if element.find(x)>0:
			t.append(element)
			#print t.index(element)
	return t

def fopen(x,m):
	""" x is filename m is the type of the reading:
	0 - read ,
	1 - readlines ,
	2 - loadtxt for without header files
	Returns a string -> read, list -> readlines, nd.array -> loadtxt

	Example d=fopen('foo.dat',2)
	"""
	
	if m==0:
		f=open(x,'r')
		data=f.read()
		f.close()
	if m==1:
		f=open(x,'r')
		data=f.readlines()
		f.close()
	if m==2:
		data=np.loadtxt(x)
	
	return data
