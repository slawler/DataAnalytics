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

#--------Data Requested from stream----------#
logdata = {"navigation.courseOverGroundMagnetic":'COG',
           "navigation.speedThroughWater":'STW',
           "performance.velocityMadeGood":"VMG",
           "environment.wind.speedApparent":'ApWnd',
           "environment.wind.angleApparent":'ApWndAngle',
           "environment.wind.speedTrue":'TrWnd',
           "environment.depth.belowTransducer": 'dpth',
           "timestamp": 't'
        }


#--------Cycle Through streaming data-----#
output = datetime.datetime.now().strftime("%m_%d_%Y_%M%S")
with open('TEST%s.txt' % output,'w') as f:
    while stream.connected == True:
        try:
            rcvd = stream.recv()
            jdata= json.loads(rcvd)
        except(KeyboardInterrupt, SystemExit):
            print("Terminate Test")
            break

        try:
            dtype= jdata['updates'][0]['values'][0]['path']
            dval = jdata['updates'][0]['values'][0]['value']
            time = jdata['updates'][0]['timestamp']
            if dtype in logdata:
                data = time +'\t' + logdata[dtype]+'\t' + str(round(dval,1))+'\n'
                f.write(str(data))
                print(data)
        except:
            continue



