from distutils.core import setup
from distutils.filelist import findall
import os
import matplotlib
import py2exe

setup(console=['main_zu_window.py'],data_files=matplotlib.get_py2exe_datafiles())