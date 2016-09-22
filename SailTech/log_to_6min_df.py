
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
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
#------------------------------BEGIN SCRIPT----------------------------------#

cols= [0,1,2]
cnames = ['date','data','obs']
dtypes={'date':'str','data':'str','obs':'float' }
dtm = ['date']

def TransformLog(csv):
    df_in = pd.read_csv(csv, sep = '\t', usecols= cols, names=cnames,
                    dtype=dtypes, parse_dates=dtm )
    df = df_in.set_index(['date'])
    d = df.groupby([pd.TimeGrouper('2min'), 'data']).agg({'obs': np.mean})
    dn = d.unstack()
    return dn

def GetThisBoatData(dataframe):
    data = []
    for col in dataframe:
        data.append(col)
    return data

def GetDataUnits(data,DataDict):
    for d in DataDict:
        if data in d:
            return data

def rad2deg(vector):
    d_vector = vector*(180/np.pi)
    negatives = d_vector <0
    d_vector[negatives] = d_vector[negatives]*(-1)+180
    return d_vector

df = TransformLog('log.txt')
mydata = GetThisBoatData(df)

#Convert Radian Vectors to Degrees
degdata = [('obs', 'windangleApparent'),
           ('obs', 'windangleTrueWater')]

tr_wind = [('obs', 'windspeedTrue'),
           ('obs', 'windangleTrueWater')]

ap_wind = [('obs', 'windspeedApparent'),
           ('obs', 'windangleApparent')]

perf = [('obs', 'speedOverGround'),
        ('obs', 'speedThroughWater'),
        ('obs', 'velocityMadeGood')]


for d in degdata:
    df[d] = rad2deg(df[d])

df.plot(x = df.index, y = perf)

ws, wd = df[tr_wind [0]], df[tr_wind[1]]
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
