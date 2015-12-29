#! /usr/bin/env python
import os,re
import numpy as np
#from pylab import *
import matplotlib.pyplot as plt
import sys


def natural_sort(l): 
	"""
	Sorts the list l in ascending order regarding the digits in the entry of the list.
	It also sorts regarding the numbers and letters in the word.

	Example:
	l=['1_2koko','23loco','3_4disco','1.3','0.123']
	
	In [1]: natural_sort(l)
	Out[1]: ['0.123', '1.3', '1_2koko', '3_4disco', '23loco']
	

	"""
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

