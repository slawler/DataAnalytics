
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
from datetime import datetime
from windrose import WindroseAxes
from matplotlib import pyplot as plt
#from mpl_toolkits.basemap import Basemap
#import matplotlib.cm as cm
import numpy as np
import mplleaflet


logfile = 'log.txt'
cols= [0,1,2]
cnames = ['date','data','obs']
dtypes={'date':'str','data':'str','obs':'float' }
dtm = ['date']
resample_rate = 2
log_updated = datetime.now()
saildate= log_updated.strftime(format = 'Pegasus_Sail_Log_%Y_%m_%d')

#------------------------------Signal K Ouput----------------------------------#

#tr_wind = [('obs', 'windspeedTrue'),
#           ('obs', 'windangleTrueWater')]

ap_wind = [('obs', 'windspeedApparent'),
           ('obs', 'windangleApparent')]

perf = [('obs', 'speedOverGround'),
        ('obs', 'speedThroughWater')]


degdata = [ap_wind] # All data requiring conversion to degrees from radians
veldata = [perf]    # All data requiring conversion to knots from m/s

#------------------------------------------------------------------#
#---------------------------END FUNCTIONS--------------------------#
#------------------------------------------------------------------#
def TransformLog(csv,resample_rate ):
    df_in = pd.read_csv(csv, sep = '\t', usecols= cols, names=cnames,
                    dtype=dtypes, parse_dates=dtm )
    df = df_in.set_index(['date'])
    d = df.groupby([pd.TimeGrouper('{}min'.format(resample_rate )), 'data']).agg({'obs': np.mean})
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
            
def PlotWind(ws,wd):
    ax = WindroseAxes.from_ax()
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()

def PlotScalar(df, obs):
    ax1 = df.plot(x = df.index,y = obs)
    lines, u_labels = ax1.get_legend_handles_labels()
    s_labels = [str(i) for i in u_labels]
    labels = [i.split()[-1][:-1] for i in s_labels]
    ax1.legend(lines[:], labels[:], loc='best') 

'''
#-Basemap Plot
def PlotCourse(lons,lats):    
    fig = plt.figure(figsize=(20,10))
    
    map = Basemap(projection='gall', 
                  # with low resolution,
                  resolution = 'l', 
                  # And threshold 100000
                  area_thresh = 100000.0,
                  # Centered at 0,0 (i.e null island)
                  lat_0=0, lon_0=0)
    
    
    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color = '#888888')
    map.drawmapboundary(fill_color='#f4f4f4')
    x,y = map(lons,lats)   
    map.plot(lons, lats, 'ro', markersize=6)
    plt.show()    
'''

def PlotCourse(lons,lats,logtitle):      
    plt.hold(True)
    plt.plot(lons, lats, 'b') # Draw blue line
    plt.plot(lons, lats, 'rs') # Draw red squares
    mplleaflet.show(tiles = 'esri_aerial', path = '{}.html'.format(logtitle))


def rad2deg(vector):
    d_vector = vector*(180/np.pi)
    negatives = d_vector <0
    d_vector[negatives] = d_vector[negatives]*(-1)+180
    return d_vector

def ms2kn(vector):
    d_vector = vector*1.94684
    return d_vector


#------------------------------------------------------------------#
#---------------------------END FUNCTIONS--------------------------#
#------------------------------------------------------------------#


#++++++++++++++++++++++++++++++++++++++++++++BEGIN SCRIPT++++++++++++++++++++++++++++++++++#
df = TransformLog(logfile,resample_rate )
mydata = GetThisBoatData(df)

#---Check to see how Pegasus Positions are labeled
lons,lats = df[('obs', 'positionlongitude')].values, df[('obs', 'positionlatitude')].values

#Convert Radian Vectors to Degrees
for d in degdata:
    df[d] = rad2deg(df[d])

#Convert m/S to Knots
for d in veldata:
    df[d] = ms2kn(df[d])

#--Current list length ==1, need to increase for multiple variables, add titles to plots
for d in degdata:
    for i, col in enumerate(d):
        if i == 0:
            ws = df[d][col][:]
        elif i ==1:
            wd = df[d][col][:]
    #PlotWind(ws,wd)

#PlotScalar(df,perf)
PlotCourse(lons,lats, saildate)
