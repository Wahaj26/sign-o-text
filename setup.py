# setup.py
import sys
sys.setrecursionlimit(5000)
from distutils.core import setup
import py2exe
 
setup(windows=['index.py'])