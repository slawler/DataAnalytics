# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Interpolate two columns of coastal data to create a single x axis
Input(s): excel file
Output(s): excel file
slawler@dewberry.com
Created on Tue Apr 19 15:08:33 2016
Comments: May need to run --allow a crash-- and look at the output dataframe 
column names to setup for automated processing: df.head()
"""
#------------Load Python Modules--------------------#
import pandas as pd
import numpy as np
from scipy import interpolate 

#--------------------------Assign Variables----------------------------------#

WorkBook     = 'Copy of WHAFIS_500_for_Seth.xlsx' #Excel Input Workbook

New_WorkBook = 'Copy of WHAFIS_500_for_Seth_Interp_v2.xlsx' #Excel Output Workbook

x1, y1  = 'LOCATION', 'ELEVATION'   #x,y point pair column names, basis of interp
x2, y2  = 'STATION' , 'ELEVATION.1'  #secondary x,y point pair names, to be interp
y1_new, y2_new  = 'Wave Crest', 'Ground Elevation'       #new column names to replace y1 &y2
skiprows = 1
#------------------------------BEGIN SCRIPT----------------------------------#

for i in range(1):  
    #--Get list of tabs (worksheets)
    tabs = pd.ExcelFile(WorkBook).sheet_names 
    
    #--inititate excelwriter
    writer = pd.ExcelWriter(New_WorkBook, engine='xlsxwriter')
    
    #---For each sheet in the workbook
    for t in tabs: 
        print 'reading: ', t
        
        #---Read in the sheet
        df = pd.read_excel(WorkBook,skiprows=skiprows, sheetname=t)
        
        #---Select 1st set of columns, convert to dataframe, rename (for the merge function)
        df1 = pd.concat([df[x1], df[y1]], axis=1, keys=[x1, y1])
        df1.rename(columns = {x1:x2}, inplace=True)
        df1.rename(columns = {y1:y2}, inplace=True)
        
        #---Select 2nd set of columns, convert to dataframe, rename (for the merge function)
        df2 = pd.concat([df[x2], df[y2]], axis=1, keys=[x2, y2])
        df2.rename(columns = {y2:y1}, inplace=True)
        
        #---Stack the index lists, sort, drop duplicates and make a dataframe with the clean index
        idx          = pd.DataFrame()
        idx          = pd.concat([df[x1],df[x2]])      
        df_idx       = pd.DataFrame(idx, columns = [x2])     
        df_idx_sort  = df_idx.sort([x2], ascending = True) 
        idx_df    = df_idx_sort.drop_duplicates().dropna()
        
        #---Merge the 2 dataframes to the new df index
        df_part1 = idx_df.merge(df1,on=x2, how = 'left')
        df_part1.rename(columns = {y2 : y1_new}, inplace=True)
        
        df_part2 = df_part1.merge(df2,on=x2, how = 'left')
        df_part2.rename(columns = {y1: y2_new}, inplace=True)
        
        #---Interpolate to a 3rd dataframe, merge with the original and drop redundant column
        df3 = df_part2.interpolate(method='polynomial', order=1,inplace=False)
        output = df_idx.merge(df3,on=x2, how = 'left')
        
        #----Rename Columns if needed, and write to a new sheet in the excel file

        
        output.to_excel(writer, sheet_name= t, index = False)
        print output.head()
        print 'writing : ', t
        print '.................'
        
    #---Save the excel file and end program    
    writer.save()
