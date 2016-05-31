# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Interpolate two columns of coastal data to create a single x axis
Input(s): excel file
Output(s): excel file
slawler@dewberry.com
Created on Tue Apr 19 15:08:33 2016
"""
#------------Load Python Modules--------------------#
import pandas as pd
import numpy as np
from scipy import interpolate 

#------------------------------BEGIN SCRIPT----------------------------------#

tabs = []

for i in range(1,29):
    tab = 'P' + str(i)
    tabs.append(tab)


for i in range(1):  
    #--inititate excelwriter
    writer = pd.ExcelWriter('PlaqWHAFIS2008_500yr_wground_v_Interp_sl.xlsx', engine='xlsxwriter')
    
    #---For each sheet in the workbook
    for t in tabs:  
        #---Read in the sheet
        df = pd.read_excel('PlaqWHAFIS2008_500yr_wground_vsl.xlsx', sheetname = t)
        
        #---Select 1st set of columns, convert to dataframe, rename (for the merge function)
        df1 = pd.concat([df['Station'], df['Wave Crest']], axis=1, keys=['Station', 'Wave Crest'])
        df1.rename(columns = {'Station':'STATION'}, inplace=True)
        
        #---Select 2nd set of columns, convert to dataframe, rename (for the merge function)
        df2 = pd.concat([df['Station.1'], df['Elevation']], axis=1, keys=['Station.1', 'Elevation'])
        df2.rename(columns = {'Station.1':'STATION'}, inplace=True)
        
        #---Stack the index lists, sort, drop duplicates and make a dataframe with the clean index
        idx          = pd.DataFrame()
        idx          = pd.concat([df['Station'],df['Station.1']])      
        df_idx       = pd.DataFrame(idx, columns = ['Station.1'])     
        df_idx_sort  = df_idx.sort(['Station.1']) 
        
        idx_df    = df_idx_sort.sort().drop_duplicates()  
        idx_df.rename(columns = {'Station.1':'STATION'}, inplace=True)
        
        #---Merge the 2 dataframes to the new df index
        df_part1 = idx_df.merge(df1,on="STATION", how = 'left')
        df_part2 = df_part1.merge(df2,on="STATION", how = 'left')
        
        #---Interpolate to a 3rd dataframe, merge with the original and drop redundant column
        df3 = df_part2.interpolate()
        output = df1.merge(df3,on="STATION", how = 'left')
        output.drop('Wave Crest_y', axis=1, inplace=True)
        
        #----Rename Columns if needed, and write to a new sheet in the excel file
        output.rename(columns = {'Wave Crest_x': 'Wave Crest'}, inplace=True)
        output.to_excel(writer, sheet_name= t, index = False)
        print '.................'
        print 'writing : ', t
        
    #---Save the excel file and end program    
    writer.save()

