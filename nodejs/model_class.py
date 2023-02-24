# -*- coding: utf-8 -*-

import json
import tableData as tdata
import numpy as np
from scipy.integrate import odeint
import sys

class boiler:
    p_atm = 100000
    R_un = 8.314
    c_w = 4180
    ro_w = 988
    
    
    def __init__(self, InstanceID):
        try:
            with open("instancesData/"+ InstanceID + "/initialData.json", "r") as read_file:
                initData = json.load(read_file)
        except :
            print("Read file error!")
            sys.exit()
        
        try:
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
            self.alpha = initData["GasComposition"]["alpha"]
        except :
            print("Read ''GasComposition' data error!")
            sys.exit()
            
        try:
            self.D_in = initData["ObjCharacteristics"]["D_in"]
            self.D_out = initData["ObjCharacteristics"]["D_out"]
            self.delta = initData["ObjCharacteristics"]["delta"]
            self.N = initData["ObjCharacteristics"]["N"]
            self.N_g_1_7 =  initData["ObjCharacteristics"]["N_g_1_7"]
            self.N_g_8_9 =  initData["ObjCharacteristics"]["N_g_8_9"]
            self.N_w_1_5 =  initData["ObjCharacteristics"]["N_w_1_5"]
            self.N_w_6_9 =  initData["ObjCharacteristics"]["N_w_6_9"]
            self.k_tr_1_5 = initData["ObjCharacteristics"]["k_tr_1_5"]
            self.k_tr_6_7 = initData["ObjCharacteristics"]["k_tr_6_7"]
            self.k_tr_8_9 = initData["ObjCharacteristics"]["k_tr_8_9"]
            self.T_g_in = initData["ObjCharacteristics"]["T_g_in"] # Температура продуктів згорання на вході у пучок
            self.w_w = initData["ObjCharacteristics"]["w_w"]
        except :
            print("Read ''ObjCharacteristics' data error!")
            sys.exit()
        self.V_0 = 0.0476 * (0.5 * CO + 0.5 * H2 + 1.5 * H2S + (1 + 4 / 4) * CH4 + (2 + 6 / 4) * C2H6 + (3 + 8 / 4) * C3H8 + (4 + 10 / 4) * C4H10 + (5 + 12 / 4) * C5H12 - O2)
        self.V_0_N2 = 0.79 * self.V_0 + N2 / 100
        self.V_RO2 = 0.01 * (CO2 + CO + H2S + 1 * CH4 + 2 * C2H6 + 3 * C3H8 + 4 * C4H10 + 5 * C5H12)
        V_0_H2O = 0.01 * (H2S + H2 + 4 / 2 * CH4 + 6 / 2 * C2H6 + 8 / 2 * C3H8 + 10 / 2 * C4H10 + 
                          12 / 2 * C5H12 + 124 * d_g + 124 * d_air * self.V_0)

        self.V_H2O = V_0_H2O + 0.01 * 124 * d_air * (self.alpha - 1) * self.V_0
        V_dry_g = self.V_RO2  + self.V_0_N2 + (self.alpha - 1) * self.V_0
        V_g = V_dry_g + self.V_H2O
        r_RO2 = self.V_RO2 / V_g
        r_H2O = self.V_H2O / V_g
        r_0_N2 = self.V_0_N2 / V_g
        #r_0 = (self.alpha - 1) * self.V_0 / V_g
        #p_H2O = r_H2O * self.p_atm
        self.mu = 0.044 * r_RO2 + 0.018 * r_H2O + 0.024 * r_0_N2 + 0.028963 * (self.alpha - 1) * self.V_0 / V_g
        #T_s = PropsSI('T', "P", p_H2O, "Q", 0, 'H2O')
        
        # Конструктивні характеристики

        self.L = 3.1415926 * 4 * (self.D_in + self.D_out) / 2
        self.delta = 0.001
        a = (self.D_in - self.D_out) / 2 - 2 * self.delta
        b = 0.007 - 0.001 - 2 * self.delta
        s = a * b
        self.D_g_t = 2 * (a + 2 * self.delta) + 2 * (b + 2 * self.delta)
        self.D_t_w = 2 * a + 2 * b
        self.A_g_t = 0.001 * (self.D_in - self.D_out) / 2
        self.A_t_w = s
        self.delta_l = self.L / self.N
        
        # # Вхідні сигнали
        # self.T_w_in_6_9 = T_w_in_6_9
        # self.T_w_out_1_5 = T_w_out_1_5
    
    def I (self,T):
        return self.V_RO2 * tdata.cv_RO2 (T) + self.V_0_N2 * tdata.cv_N2 (T) + self.V_H2O * tdata.cv_H2O (T) + (self.alpha - 1) * self.V_0 * tdata.cv_air (T)

    def cg (self,T):
        return self.V_RO2 * tdata.cv_RO2 (T) / (T - 273.15) + self.V_0_N2 * tdata.cv_N2 (T) / (T - 273.15) + self.V_H2O * tdata.cv_H2O (T) / (T - 273.15) + (self.alpha - 1) * self.V_0 * tdata.cv_air (T) / (T - 273.15)


    def AlgebrEquationSys(self,z,T):
       V_ng = z[0]
       T_g_out_1_5 = z[1]
       T_g_out_6_7 = z[2]
       T_g_out_8_9 = z[3]
       T_w_out_6_7 = z[4]
       T_w_out_8_9 = z[5]
       T_w_in_6_9,T_w_out_1_5 = T

       F = np.empty((6))
       F[0] = V_ng * (self.I (self.T_g_in) - self.I (T_g_out_1_5)) / self.N_g_1_7 - self.k_tr_1_5 * self.D_g_t * self.delta_l * (T_g_out_1_5 - T_w_out_1_5)
       F[1] = V_ng * (self.I (self.T_g_in) - self.I (T_g_out_6_7)) / self.N_g_1_7 - self.k_tr_6_7 * self.D_g_t * self.delta_l * (T_g_out_6_7 - T_w_out_6_7)
       F[2] = self.w_w * self.c_w / self.N_w_1_5 * (2 * T_w_out_6_7 / self.N_w_6_9 + 2 * T_w_out_8_9 / self.N_w_6_9 - T_w_out_1_5) + self.k_tr_1_5 * self.D_g_t * self.delta_l * (T_g_out_1_5 - T_w_out_1_5)
       F[3] = self.w_w * self.c_w / self.N_w_6_9 * (T_w_in_6_9 - T_w_out_6_7) + self.k_tr_6_7 * self.D_g_t * self.delta_l * (T_g_out_6_7 - T_w_out_6_7)
       F[4] = V_ng * ((5 * self.I (T_g_out_1_5) / self.N_g_1_7 + 2 * self.I (T_g_out_6_7) / self.N_g_1_7) - self.I (T_g_out_8_9)) / self.N_g_8_9 - self.k_tr_8_9 * self.D_g_t * self.delta_l * (T_g_out_8_9 - T_w_out_8_9) 
       F[5] = self.w_w * self.c_w / self.N_w_6_9 * (T_w_in_6_9 - T_w_out_8_9) + self.k_tr_8_9 * self.D_g_t * self.delta_l * (T_g_out_8_9 - T_w_out_8_9)
       return F
   
    def StaticCalculation (self, T_w_in_6_9, T_w_out_1_5, V_ng_actual):
        from scipy.optimize import fsolve
        zGuess = np.array([0.001764, 388, 382, 368, 337, 335])
        T = [T_w_in_6_9,T_w_out_1_5]
        z = fsolve(self.AlgebrEquationSys,zGuess,(T,))
        
        V_ng = z[0]
        T_g_out_8_9 = z[3]

        etta_theor = self.w_w * self.c_w * (T_w_out_1_5 - T_w_in_6_9) / (36872000 * V_ng)
        etta_actual = self.w_w * self.c_w * (T_w_out_1_5 - T_w_in_6_9) / (36872000 * V_ng_actual)

        # Корисна теплота, розрахована через параметри води
        Q_net_w = self.w_w * self.c_w * (T_w_out_1_5 - T_w_in_6_9)
        # Корисна теплота, розрахована через параметри продуктів згорання
        Q_net_g = V_ng * (self.I (self.T_g_in) - self.I (T_g_out_8_9))

        return [z,etta_theor,etta_actual,Q_net_w,Q_net_g]

    def DiffEquantionSys (self,T_out,time,T_in,V):
        T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9 = T_out
        T_g_in,T_w_in_6_9 = T_in
        V_ng = V
        
        dT_g_out_1_5_dt = (V_ng * (self.I (T_g_in) - self.I (T_g_out_1_5)) / self.N_g_1_7 - self.k_tr_1_5 * self.D_g_t * self.delta_l * (T_g_out_1_5 - T_w_out_1_5))/(self.cg(T_g_out_1_5)*self.p_atm/(self.R_un/self.mu)/T_g_out_1_5*self.A_g_t*self.delta_l)
        dT_g_out_6_7_dt = (V_ng * (self.I (T_g_in) - self.I (T_g_out_6_7)) / self.N_g_1_7 - self.k_tr_6_7 * self.D_g_t * self.delta_l * (T_g_out_6_7 - T_w_out_6_7))/(self.cg(T_g_out_6_7)*self.p_atm/(self.R_un/self.mu)/T_g_out_6_7*self.A_g_t*self.delta_l)
        dT_w_out_1_5_dt = (self.w_w * self.c_w / self.N_w_1_5 * (2 * T_w_out_6_7 / self.N_w_6_9 + 2 * T_w_out_8_9 / self.N_w_6_9 - T_w_out_1_5) + self.k_tr_1_5 * self.D_g_t * self.delta_l * (T_g_out_1_5 - T_w_out_1_5))/(self.c_w*self.ro_w*self.A_t_w*self.delta_l)
        dT_w_out_6_7_dt = (self.w_w * self.c_w / self.N_w_6_9 * (T_w_in_6_9 - T_w_out_6_7) + self.k_tr_6_7 * self.D_g_t * self.delta_l * (T_g_out_6_7 - T_w_out_6_7))/(self.c_w*self.ro_w*self.A_t_w*self.delta_l)
        dT_g_out_8_9_dt = (V_ng * ((5 * self.I (T_g_out_1_5) / self.N_g_1_7 + 2 * self.I (T_g_out_6_7) / self.N_g_1_7) - self.I (T_g_out_8_9)) / self.N_g_8_9 - self.k_tr_8_9 * self.D_g_t * self.delta_l * (T_g_out_8_9 - T_w_out_8_9))/(self.cg(T_g_out_8_9)*self.p_atm/(self.R_un/self.mu)/T_g_out_8_9*self.A_g_t*self.delta_l) 
        dT_w_out_8_9_dt = (self.w_w * self.c_w / self.N_w_6_9 * (T_w_in_6_9 - T_w_out_8_9) + self.k_tr_8_9 * self.D_g_t * self.delta_l * (T_g_out_8_9 - T_w_out_8_9))/(self.c_w*self.ro_w*self.A_t_w*self.delta_l)
        
        
        return [dT_g_out_1_5_dt,dT_g_out_6_7_dt,dT_w_out_1_5_dt,dT_w_out_6_7_dt,dT_g_out_8_9_dt,dT_w_out_8_9_dt]

    def DynamicCalculation (self, duration, T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9,T_w_in_6_9,V_ng):
        T0 = [T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9]
        t = np.linspace(0,duration,duration*10)
        Tin = [self.T_g_in,T_w_in_6_9]
        Vin = V_ng

        sys = odeint(self.DiffEquantionSys, T0, t,(Tin,Vin))
        
        return [list(t),list(sys[:,0]),list(sys[:,1]),list(sys[:,2]),list(sys[:,3]),list(sys[:,4]),list(sys[:,5])]
        #return [t,sys[:,0],sys[:,1],sys[:,2],sys[:,3],sys[:,4],sys[:,5]]
    
    def StepCalculation (self, dt, T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9,T_w_in_6_9,V_ng):
        T0 = [T_g_out_1_5,T_g_out_6_7,T_w_out_1_5,T_w_out_6_7,T_g_out_8_9,T_w_out_8_9]
        t = [0,dt]
        Tin = [self.T_g_in,T_w_in_6_9]
        Vin = V_ng
        sys = odeint(self.DiffEquantionSys, T0, t,(Tin,Vin))
        return [t,sys[:,0],sys[:,1],sys[:,2],sys[:,3],sys[:,4],sys[:,5]]

# InstanceID = "1"

# T_w_in_6_9 = (59 + 273.15)
# T_w_out_1_5 = (70 + 273.15) 
# heater = boiler(InstanceID)
# V_ng =  0.001783232844700864

# V_ng_actual = 1.81974681e-03
# res1 = heater.StaticCalculation(T_w_in_6_9, T_w_out_1_5, V_ng_actual)
# print (res1)


# #T = [402.13603092246535, 397.39257463168565, 343.15, 338.1716801498798, 342.80933917634246, 333.13382277970135]


# res = heater.DynamicCalculation(15,402.13603092246535, 397.39257463168565, 343.15, 338.1716801498798, 342.80933917634246, 333.13382277970135, T_w_in_6_9, V_ng)
# import matplotlib.pyplot as plt
# plt.plot(res[0],res[1])
# plt.plot(res[0],res[2])
# plt.plot(res[0],res[3])
# plt.plot(res[0],res[4])
# plt.plot(res[0],res[5])
# plt.plot(res[0],res[6])
# plt.xlabel('time')
# plt.ylabel('y(t)')
# plt.show()






