ws = "ws://demo.signalk.org/signalk/v1/stream"

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
ws = "ws://demo.signalk.org/signalk/v1/stream"
stream = websocket.create_connection(ws)
          
#--------Open Logs to write data-------------#
  
log = open("C:\Users\sml\Desktop\log.txt", 'w')
#--------Cycle Through streaming data-------#
count = 0
while stream.connected == True:
    try:
        rcvd = stream.recv()
        jdata= json.loads(rcvd)
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
                
                if isinstance(data,unicode):                
                    dtype = ''.join(str(data).split('.')[1:])                 

                elif isinstance(data,dict):
                    dkeys = data.keys()
                    
                    for k in dkeys:
                        datagroup = ''.join(str(variables[i]['path']).split('.')[1:])
                        dtype = datagroup + str(k)
                        value = variables[i][key][k]
                        print str(count) + " logging data: " + str(table)                        
                        dtm = str(datetime.datetime.now())
                        log.write(dtm  + '\t' +dtype + '\t'+ str(value) + '\n')
                        count += 1

                else:
                    dtm = str(datetime.datetime.now())
                    value = data
                    log.write(dtm + '\t' + dtype + '\t'+ str(value) + '\n')
                    print str(count) + " logging data: " + str(table)
                    count += 1
  
                    
    except:
        continue

log.close()
