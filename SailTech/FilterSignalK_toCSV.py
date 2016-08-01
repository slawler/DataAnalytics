# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 22:28:38 2016

@author: slawler
"""

# -*- coding: utf-8 -*-
"""
Description: Read and Filter JSON stream from web socket
Input(s): ip address/web socket info
Output(s): print info to console
@author: slawler
Created on Sun Jul 17 15:28:23 2016
Comments:  Script should work in python v2 or v3
"""

#------------------MODULES-------------------#
import json
import websocket
import datetime

#---------------USER INPUT-------------------#
ws = "ws://192.168.10.102/signalk/v1/stream" #---Websocket Demo Site
stream = websocket.create_connection(ws)
          
#--------Open Logs to write data-------------#
  
#navigation = open("C:\Users\slawler\Desktop\navigationlog.csv", 'w')
#environment = open("C:\Users\slawler\Desktop\environmentlog.csv", 'w')
#performance = open("C:\Users\slawler\Desktop\performancelog.csv", 'w')        
log = open("C:\Users\slawler\Desktop\log.txt", 'w')
jlog = open("C:\Users\slawler\Desktop\jlog.txt", 'w')
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
                
                if type(data) == unicode:                
                    dtype = ''.join(str(data).split('.')[1:])                 

                elif type(data) == dict:
                    dkeys = data.keys()
                    
                    for k in dkeys:
                        datagroup = ''.join(str(variables[i]['path']).split('.')[1:])
                        dtype = datagroup + str(k)
                        value = variables[i][key][k]
                        print "logging data: " + str(table)
                        ik_dtm = jdata['updates'][0]['timestamp']
                        dtm = str(datetime.datetime.now())
                        log.write(dtm + '\t'+ ik_dtm + '\t' +dtype + '\t'+ str(value) + '\n')
                else:
                    dtm = str(datetime.datetime.now())
                    value = data
                    ik_dtm = jdata['updates'][0]['timestamp']
                    log.write(dtm + '\t' + ik_dtm + '\t' + dtype + '\t'+ str(value) + '\n')
                    print "logging data: " + str(table)
                    
    except:
        continue
	   #log.write(str(jdata))
log.close()
jlog.close()