# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Resample Signal K Filtered t-series to 6min pd dataframe

Input(s):
Output(s):

slawler@dewberry.com
Created on Wed Sep 21 16:49:49 2016
"""
#------------Load Python Modules--------------------#
import pandas as pd
import numpy as np
#------------------------------BEGIN SCRIPT----------------------------------#

cols= [0,2,3]
cnames = ['date','data','value']
dtypes={'date':'str','data':'str','value':'float' }
dtm = ['date']

df_in = pd.read_csv('log3.txt', sep = '\t', usecols= cols, names=cnames,
                    dtype=dtypes, parse_dates=dtm )

df = df_in.set_index(['date'])

d= df.groupby([pd.TimeGrouper('6min'), 'data']).agg({'value': np.mean})

print d.head()




