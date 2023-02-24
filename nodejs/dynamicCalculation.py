# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 13:43:43 2023

@author: Anastasiia
"""
# E:\OneDrive\Desktop\Нова папка\DT\Class\dynamicCalculation.py InstanceID duration T_g_out_1_5 T_g_out_6_7 T_w_out_1_5 T_w_out_6_7 T_g_out_8_9 T_w_out_8_9 T_w_in_6_9 V_ng
# E:\OneDrive\Desktop\Нова папка\DT\Class\dynamicCalculation.py 1 15 402.13603092246535 397.39257463168565 343.15 338.1716801498798 342.80933917634246 333.13382277970135 332.15 0.001783232844700864

# duration, T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9,T_w_in_6_9,V_ng

import model_class as model
import json
import mqttAddition as mqttClient
import sys

try:
    InstanceID = sys.argv[1]
    cmdId = sys.argv[2]
    duration = int(sys.argv[3])
    T_g_out_1_5 = float(sys.argv[4])
    T_g_out_6_7 = float(sys.argv[5])
    T_w_out_1_5 = float(sys.argv[6])
    T_w_out_6_7 = float(sys.argv[7])
    T_g_out_8_9 = float(sys.argv[8])
    T_w_out_8_9 = float(sys.argv[9])
    T_w_in_6_9 = float(sys.argv[10]) 
    V_ng = float(sys.argv[11])
    
except:
    print ("error")
    sys.exit(-1)

instance = model.boiler(InstanceID)
res = instance.DynamicCalculation(duration, T_g_out_1_5, T_g_out_6_7, T_w_out_1_5, T_w_out_6_7, T_g_out_8_9, T_w_out_8_9, T_w_in_6_9, V_ng)

#T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9

msg= {
     "time": res[0],
     "T_g_out_1_5": res[0],
     "T_g_out_6_7": res[0],
     "T_w_out_1_5": res[0],
     "T_w_out_6_7": res[0],
     "T_g_out_8_9": res[0],
     "T_w_out_8_9": res[1]
     }

client = mqttClient.connect_mqtt()
json_msg = json.dumps(msg, indent = 4)
mqttClient.publish(client,json_msg)

#print (msg)
print("success")
sys.exit(1)
