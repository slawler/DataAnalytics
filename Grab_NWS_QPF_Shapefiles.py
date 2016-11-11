# -*- coding: utf-8 -*-
"""
Description: Download Hourly QPF shapefiles of historical data 
    from NWS web archive: http://www.srh.noaa.gov/ridge2/RFC_Precip/

Input(s)   : Start & End Date
Output(s)  : .tar.gz files for every hour

slawler@dewberry.com
Created on Wed May 11 20:20:13 2016
"""
#---------------LOAD PYTHON MODULES-----------------------#
from pandas import date_range, DateOffset
from datetime import datetime
import requests

#---------------ENTER VARIABLES---------------------------#
start     = datetime(2014, 1, 1,0)            #Start Date
stop      = datetime(2014, 1, 2,0)            #End Date
interval  = DateOffset(hours=1)               #interval   

#----------------------------------------------------------#
#-----------------------RUN SCRIPT-------------------------#
#----------------------------------------------------------#

#---Create Time Series (DatetimeIndex) 
daterange = date_range(start,stop - interval ,freq = interval)
s = '/'

for d in daterange:   
    print 'Downloading QPF for', d
    year   = d.strftime(format='%Y')
    month  = d.strftime(format='%m')
    day    = d.strftime(format='%d')
    hour   = d.strftime(format='%H')
    dtm    = year + s + year + month + s + year+month+day + s
    tstamp = 'nws' + '_' + 'precip' + '_' + year+month+day+hour + '.tar.gz'
    url = 'http://www.srh.noaa.gov/ridge2/Precip/qpehourlyshape/%s%s' %(dtm, tstamp) 
    r = requests.get(url)
    open(tstamp, 'wb').write(r.content)    
