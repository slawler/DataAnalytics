#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: FIlter Signal K to csv, for python v 3.5.x

Input(s):
Output(s):

@author: slawler@dewberry.com
Created on Sat Oct  8 23:33:18 2016
"""
#------------Load Python Modules--------------------#
import json
import websocket
import datetime

ws = "ws://demo.signalk.org/signalk/v1/stream"
stream = websocket.create_connection(ws)
          
#--------Open Logs to write data-------------#       
log = open("log.txt", 'w')
jlog = open("jlog.txt", 'w')
#--------Cycle Through streaming data-------#
 
while stream.connected == True:
    try:
        rcvd = stream.recv()
        jdata= json.loads(rcvd)
        jlog.write(str(jdata)+'\n')
    except(KeyboardInterrupt, SystemExit):
        print("Terminate Test")
        break

#--------Filter & Write data to logs-------#
    try:
        table  = jdata['updates'][0]['values'][0]['path'].split('.')[0]
        variables = jdata['updates'][0]['values']
        
        for i, v in enumerate(variables):                
            keys = v.keys()
            
            for key in keys:
                data = variables[i][key]
                
                if isinstance(data,str):                
                    dtype = ''.join(data.split('.')[1:])                 

                elif isinstance(data, dict):
                    dkeys = data.keys()
                    
                    for k in dkeys:
                        datagroup = ''.join(str(variables[i]['path']).split('.')[1:])
                        dtype = datagroup + k
                        value = variables[i][key][k]                        
                        dtm = str(datetime.datetime.now())
                        log_entry = '{}\t{}\t{}\n'.format(dtm,dtype,str(value))
                        log.write(log_entry)
                        print("logging data: {}".format(table))
                        
                else:
                    dtm, value = str(datetime.datetime.now()), data
                    log_entry = '{}\t{}\t{}\n'.format(dtm,dtype,str(value))
                    log.write(log_entry)
                    print("logging data: {}".format(table))
                    
    except:
        print('Error')
        continue
	   #log.write(str(jdata))
log.close()
jlog.close()
