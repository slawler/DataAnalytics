# -*- coding: utf-8 - Python 2.7.11 *-
"""
Description: Extract Files from FGDB

Adapted from:
http://gis.stackexchange.com/questions/25430/exporting-features-with-attachments-for-use-outside-arcgis

Input(s): Dirs,GDB,Fields
Output(s):Attached Files

skoka@dewberry.com, slawler@dewberry.com
Created on Tue Aug 09 12:16:17 2016
"""
#------------Load Python Modules--------------------#
from arcpy import da
import os, sys
#------------------------------USER INPUT----------------------------------#

gdb = r"C:\Users\slawler\Desktop\Data_Identification_Test2\506d9a100bdf47fd913959627b14f3a9.gdb\\Data_Identification__ATTACH"
outdir = r"C:\Users\slawler\Desktop\Data_Identification_Test2"
fields = ['Data','ATT_NAME']

#------------------------------BEGIN SCRIPT----------------------------------#
with da.SearchCursor(gdb,[fields[0],fields[1]]) as cursor:
   for row in cursor:
      binaryRep = row[0]
      fileName  = row[1]
      print fileName
      open(outdir + os.sep + fileName, 'wb').write(binaryRep.tobytes())
      del row; del binaryRep; del fileName
