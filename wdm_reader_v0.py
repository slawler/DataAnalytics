# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 21:55:35 2016

Description: Testing and Sample Data for the wdmtoolbox module

Input(s): .wdm & .PS files
Output(s): .txt files

@author: slawler@dewberry.com
"""
#------------Import Python Modules-----------#
import os
from wdmtoolbox import wdmtoolbox
import pandas as pd
#--------------------------------------------#

#---Assign Directory & file paths
directory = "C:\\Users\sml\Desktop"
wdm_file = "ps_B24001_to_PU4_4440_3970.wdm"
ps_file = "B24001_PU4_4440_3970.PS"

#---Create a string variabe combining the filename & filepath for files
f1 = os.path.join(directory,wdm_file)
f2 = os.path.join(directory,ps_file)

#---Get a list of the data vectors (keys) in the file
for key in wdmtoolbox.listdsns(f1):
	print key

#---Print to the console the contents of each key in the original wdm file
for key in wdmtoolbox.listdsns(f1):
	print key
	print wdmtoolbox.describedsn(f1,key)

#---It looks like the vector in the wdm file corresponding to the data in the PS file is 3050, let's read it in: 
data_key = 3050
raw_data = wdmtoolbox.extract(f1,data_key)

#---Print the Head & Tail of the wdb file to the python console (as in R):
print raw_data.head()
print raw_data.tail()

#---Read in the PS file as a DataFrame Object
df = pd.read_csv(f2)

#---Print the Head & Tail of the PS file to the python console:
print df.head()
print df.tail()

#---Data needs some reformatting, let's do that:
df = pd.read_csv(f2, header=None, sep=',', parse_dates=[[0,1,2,3]] )
df.head()

#---Better, now lets rename and reformat the columns & index to be the same as the raw_data:
df.columns = ['Datetime', 'PS_File']
df.set_index(['Datetime'], inplace=True)
df.head()

#---Now Lets Merge, Clean & Compare:
dbm_default_column_name = wdm_file +'_DSN_%s' %(data_key)
data_check = df.merge(raw_data,right_index=True, left_index=True)
data_check = data_check.rename(columns = {dbm_default_column_name:'DBM_Data'})
data_check['Difference'] = data_check['PS_File'] - data_check['DBM_Data']
data_check.head()

#---Write DataFrame Slice to text file:
data_check.to_csv('PS_vs_WDM_Data.txt', sep = ',')


#---There was also some data in the dns=3000, lets print that and the 3050 vectors to file too:
wdmtoolbox.extract(f1,3000).to_csv('dns_3000.txt')
wdmtoolbox.extract(f1,3050).to_csv('dns_3050.txt')

'''
#----Write the contents of each key in the original wdm file (in dataframe format) to a text file
for key in wdmtoolbox.listdsns(f1):
	print key
	raw_data = wdmtoolbox.extract(f1,key)
	raw_data.to_csv('wdm_file_%s.txt' %key)
''' 