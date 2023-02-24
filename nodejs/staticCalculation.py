# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 13:43:43 2023

@author: Anastasiia
"""
# E:\OneDrive\Desktop\Нова папка\DT\Class\staticCalculation.py InstanceID T_w_in_6_9 T_w_out_1_5 V_ng_actual
# E:\OneDrive\Desktop\Нова папка\DT\Class\staticCalculation.py 1 332.15 343.15 1.81974681e-03

import model_class as model
import json
import mqttAddition as mqttClient
import sys

try:
    InstanceID = sys.argv[1]
    cmdId = sys.argv[2]
    T_w_in_6_9 = float(sys.argv[3])
    T_w_out_1_5 = float(sys.argv[4])
    V_ng_actual = float(sys.argv[5])
    
except:
    sys.exit("args")

instance = model.boiler(InstanceID)
res = instance.StaticCalculation(T_w_in_6_9,T_w_out_1_5,V_ng_actual)


msg= {
     "cmdId": cmdId,
     "V_ng": res[0][0],
     "T_g_out_1_5": res[0][1],
     "T_g_out_6_7": res[0][2],
     "T_g_out_8_9": res[0][3],
     "T_w_out_6_7": res[0][4],
     "T_w_out_8_9": res[0][5],
     "etta_theor": res[1],
     "etta_actual": res[2],
     "Q_net_w": res[3],
     "Q_net_g": res[4]
     }

client = mqttClient.connect_mqtt()
json_msg = json.dumps(msg, indent = 4)
mqttClient.publish(client,json_msg)

print("success")
sys.exit(1)
