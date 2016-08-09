# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description:
Input(s):
Output(s):
slawler@dewberry.com
Created on Tue Aug 09 08:36:48 2016
"""
#------------Load Python Modules--------------------#
#import pandas as pd
#import numpy as np
#import sys

#MODPATH, MOD  = 'C:\\PATH', 'MODULE.py'
#sys.path.append(MODPATH)
#from MOD import *
#------------------------------BEGIN SCRIPT----------------------------------#
	
import pandas as pd
from pandas.io.json import json_normalize
import json
import numpy as np
import ast

with open('jlog.txt') as f:
    for i in range(10):
        line = f.readline()
        data = ast.literal_eval(line)
        #d = json.dumps(data)
        df = json_normalize(data,'updates')['values'][0]
        print df
        

