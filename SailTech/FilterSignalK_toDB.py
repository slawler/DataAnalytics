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
import psycopg2
import threading

#---------------USER INPUT-------------------#
ws = "ws://192.168.10.102/signalk/v1/stream" #---Websocket Demo Site
stream = websocket.create_connection(ws)
          
#--------Open DB to write data-------------#
db = psycopg2.connect(database="signalk", user="postgres", password="Password", host="localhost", port="5433")
cur = db.cursor()
print "Connected to PostgreSQL database instance"

#--------Cycle Through streaming data-------#
 
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
                
                if type(data) == unicode:                
                    dtype = ''.join(str(data).split('.')[1:])                 

                elif type(data) == dict:
                    dkeys = data.keys()
                    
                    for k in dkeys:
                        datagroup = ''.join(str(variables[i]['path']).split('.')[1:])
                        dtype = datagroup + str(k)
                        value = variables[i][key][k]
                        print "logging data: " + str(table)
                        #ik_dtm = jdata['updates'][0]['timestamp']
                        dtm = str(datetime.datetime.now())
                        expression = "INSERT INTO pegasusv0 (dtm,dtype, dvalue) VALUES \
                                      ('{0}', '{1}', {2})".format(dtm,dtype,value);
                        cur.execute(expression);
                        db.commit()

                else:
                    dtm = str(datetime.datetime.now())
                    value = data
                    #ik_dtm = jdata['updates'][0]['timestamp']
                    expression = "INSERT INTO pegasusv0 (dtm,dtype, dvalue) VALUES \
                                   ('{0}', '{1}', {2})".format(dtm,dtype,value);
                    cur.execute(expression);
                    db.commit()               
                    print "logging data: " + str(table)
                    
    except:
        continue
    
db.commit()
db.close()
print "Process stopped"
