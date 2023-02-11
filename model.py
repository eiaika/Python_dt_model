# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 17:05:05 2023

@author: Anastasiia
"""

#from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
from CoolProp.CoolProp import PropsSI
from scipy.interpolate import CubicSpline
import json
import mqttAddition as mqttClient


try:
    with open("initialData.json", "r") as read_file:
        initData = json.load(read_file)
except :
    print("Read file error!")
    quit()



CH4 = initData["GasComposition"]["CH4"]
C2H6 = initData["GasComposition"]["C2H6"]
C3H8 = initData["GasComposition"]["C3H8"]
C4H10 = initData["GasComposition"]["C4H10"]
C5H12 = initData["GasComposition"]["C5H12"]
N2 = initData["GasComposition"]["N2"]
CO2 = initData["GasComposition"]["CO2"]
O2 = initData["GasComposition"]["O2"]
CO = initData["GasComposition"]["CO"]
H2 = initData["GasComposition"]["H2"]
H2S = initData["GasComposition"]["H2S"]
d_g = initData["GasComposition"]["d_g"]
d_air = initData["GasComposition"]["d_air"]
alpha = initData["GasComposition"]["alpha"]


V_0 = 0.0476 * (0.5 * CO + 0.5 * H2 + 1.5 * H2S + (1 + 4 / 4) * CH4 + 
               (2 + 6 / 4) * C2H6 + (3 + 8 / 4) * C3H8 + (4 + 10 / 4) * C4H10 +
               (5 + 12 / 4) * C5H12 - O2)

V_0_N2 = 0.79 * V_0 + N2 / 100
V_RO2 = 0.01 * (CO2 + CO + H2S + 1 * CH4 + 2 * C2H6 + 3 * C3H8 + 4 * C4H10 + 5 * C5H12)
V_0_H2O = 0.01 * (H2S + H2 + 4 / 2 * CH4 + 6 / 2 * C2H6 + 8 / 2 * C3H8 + 10 / 2 * C4H10 + 
                  12 / 2 * C5H12 + 124 * d_g + 124 * d_air * V_0)

V_H2O = V_0_H2O + 0.01 * 124 * d_air * (alpha - 1) * V_0
V_dry_g = V_RO2  + V_0_N2 + (alpha - 1) * V_0
V_g = V_dry_g + V_H2O
r_RO2 = V_RO2 / V_g
r_H2O = V_H2O / V_g
r_0_N2 = V_0_N2 / V_g
r_0 = (alpha - 1) * V_0 / V_g
p_atm = initData["GasComposition"]["p_atm"]
#R_un = 8.314
p_H2O = r_H2O * p_atm
mu = 0.044 * r_RO2 + 0.018 * r_H2O + 0.024 * r_0_N2 + 0.028963 * (alpha - 1) * V_0 / V_g
T_s = PropsSI('T', "P", p_H2O, "Q", 0, 'H2O')

T_air_var = initData["ArrayData"]["T_air_var"]
cv_air_var = initData["ArrayData"]["cv_air_var"]
cv_air = CubicSpline(T_air_var, cv_air_var, bc_type='natural')

def I (T):
    return V_RO2 * PropsSI('H', "P", p_atm, "T", T, 'CO2') * (44/22.4) + V_0_N2 * PropsSI('H', "P", p_atm, "T", T, 'N2') * (28/22.4) + V_H2O * PropsSI('H', "P", p_atm, "T", T, 'H2O') * (18/22.4) + (alpha - 1) * V_0 * cv_air (T)
def с (T):
    return V_RO2 * PropsSI('С', "P", p_atm, "T", T, 'CO2') * (44/22.4) + V_0_N2 * PropsSI('С', "P", p_atm, "T", T, 'N2') * (28/22.4) + V_H2O * PropsSI('С', "P", p_atm, "T", T, 'H2O') * (18/22.4) + (alpha - 1) * V_0 * cv_air (T) / (T - 273.15)

# Конструктивні характеристики
D_in = initData["ObjCharacteristics"]["D_in"]
D_out = initData["ObjCharacteristics"]["D_out"]
L =  initData["ObjCharacteristics"]["L"]
delta =  initData["ObjCharacteristics"]["delta"]
a =  initData["ObjCharacteristics"]["a"]
b =  initData["ObjCharacteristics"]["b"]
s =  initData["ObjCharacteristics"]["s"]
D_g_t =  initData["ObjCharacteristics"]["D_g_t"]
D_t_w =  initData["ObjCharacteristics"]["D_t_w"]
A_g_t =  initData["ObjCharacteristics"]["A_g_t"]
A_t_w =  initData["ObjCharacteristics"]["A_t_w"]
N =  initData["ObjCharacteristics"]["N"]
delta_l =  initData["ObjCharacteristics"]["delta_l"]
N_g_1_7 =  initData["ObjCharacteristics"]["N_g_1_7"]
N_g_8_9 =  initData["ObjCharacteristics"]["N_g_8_9"]
N_w_1_5 =  initData["ObjCharacteristics"]["N_w_1_5"]
N_w_6_9 =  initData["ObjCharacteristics"]["N_w_6_9"]

# Коефцієнти теплопередачі
k_tr_1_5 = initData["ObjCharacteristics"]["k_tr_1_5"]
k_tr_6_7 = initData["ObjCharacteristics"]["k_tr_6_7"]
k_tr_8_9 = initData["ObjCharacteristics"]["k_tr_8_9"]

c_w = initData["ObjCharacteristics"]["c_w"]
# Температура продуктів згорання на вході у пучок
T_g_in = (1100 + 273.15)
# Вхідні сигнали
T_w_in_6_9 = (59 + 273.15)
T_w_out_1_5 = (70 + 273.15)
w_w = 0.961
V_ng_actual = 1.81974681e-03



import numpy as np
from scipy.optimize import fsolve

def myFunction(z):
   V_ng = z[0]
   T_g_out_1_5 = z[1]
   T_g_out_6_7 = z[2]
   T_g_out_8_9 = z[3]
   T_w_out_6_7 = z[4]
   T_w_out_8_9 = z[5]

   F = np.empty((6))
   F[0] = V_ng * (I (T_g_in) - I (T_g_out_1_5)) / N_g_1_7 - k_tr_1_5 * D_g_t * delta_l * (T_g_out_1_5 - T_w_out_1_5)
   F[1] = V_ng * (I (T_g_in) - I (T_g_out_6_7)) / N_g_1_7 - k_tr_6_7 * D_g_t * delta_l * (T_g_out_6_7 - T_w_out_6_7)
   F[2] = w_w * c_w / N_w_1_5 * (2 * T_w_out_6_7 / N_w_6_9 + 2 * T_w_out_8_9 / N_w_6_9 - T_w_out_1_5) + k_tr_1_5 * D_g_t * delta_l * (T_g_out_1_5 - T_w_out_1_5)
   F[3] = w_w * c_w / N_w_6_9 * (T_w_in_6_9 - T_w_out_6_7) + k_tr_6_7 * D_g_t * delta_l * (T_g_out_6_7 - T_w_out_6_7)
   F[4] = V_ng * ((5 * I (T_g_out_1_5) / N_g_1_7 + 2 * I (T_g_out_6_7) / N_g_1_7) - I (T_g_out_8_9)) / N_g_8_9 - k_tr_8_9 * D_g_t * delta_l * (T_g_out_8_9 - T_w_out_8_9) 
   F[5] = w_w * c_w / N_w_6_9 * (T_w_in_6_9 - T_w_out_8_9) + k_tr_8_9 * D_g_t * delta_l * (T_g_out_8_9 - T_w_out_8_9)
   return F

zGuess = np.array([0.001764, 388, 382, 368, 337, 335])
z = fsolve(myFunction,zGuess)
print(z)
V_ng = z[0]

etta_theor = w_w * c_w * (T_w_out_1_5 - T_w_in_6_9) / (36872000 * V_ng)

etta_actual = w_w * c_w * (T_w_out_1_5 - T_w_in_6_9) / (36872000 * V_ng_actual)

T = (700 + 273.15)


msg= {
     "V_ng": z[0],
     "T_g_out_1_5": z[1],
     "T_g_out_6_7": z[2],
     "T_g_out_8_9": z[3],
     "T_w_out_6_7": z[4],
     "T_w_out_8_9": z[5],
     "etta_theor": etta_theor,
     "etta_actual": etta_actual
     }

client = mqttClient.connect_mqtt()
json_msg = json.dumps(msg, indent = 4)
mqttClient.publish(client,json_msg)




print (etta_theor)
print (etta_actual)