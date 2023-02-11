


import json

CH4 = 88.8825
C2H6 = 5.0932
C3H8 = 1.3142
C4H10 = 0.386
C5H12 = 0.234
N2 = 1.6896
CO2 = 2.3921 + 0.00010000000001753051
O2 = 0.0083
CO = 0
H2 = 0
H2S = 0
d_g = 0.010
d_air = 0.013
alpha = 1.3
sum = (CH4 + C2H6 + C3H8 + C4H10 + C5H12 + N2 + CO2 + O2 + CO + H2 + H2S)

p_atm = 100000

#R_un = 8.314




T_air_var = [20 + 273.15, 50 + 273.15, 80 + 273.15, 100 + 273.15,
     200 + 273.15, 300 + 273.15, 400 + 273.15, 500 + 273.15,
     600 + 273.15, 700 + 273.15, 800 + 273.15, 900 + 273.15,
     1000 + 273.15, 1100 + 273.15, 1200 + 273.15, 1300 + 273.15,
     1400 + 273.15, 1500 + 273.15, 1600 + 273.15, 1700 + 273.15]
cv_air_var = [26000, 65000, 104000, 133000, 267000, 404000, 543000, 686000,
     832000, 982000, 1134000, 1285000, 1440000, 1600000, 1760000, 1919000,
     2083000, 2247000, 2411000, 2574000]



# Конструктивні характеристики
D_in = 0.225
D_out = 0.180
L = 3.1415926 * 4 * (D_in + D_out) / 2
delta = 0.001
a = (D_in - D_out) / 2 - 2 * delta
b = 0.007 - 0.001 - 0.2 * delta
s = a * b
D_g_t = 2 * (a + 2 * delta) + 2 * (b + 2 * delta)
D_t_w = 2 * a + 2 * b
A_g_t = 0.001 * (D_in - D_out) / 2
A_t_w = s
N = 1
delta_l = L / N
N_g_1_7 = 7
N_g_8_9 = 2
N_w_1_5 = 5
N_w_6_9 = 4

# Коефцієнти теплопередачі
k_tr_1_5 = 1000
k_tr_6_7 = 1000
k_tr_8_9 = 1000

c_w = 4180
# Температура продуктів згорання на вході у пучок
T_g_in = (1100 + 273.15)
# Вхідні сигнали
T_w_in_6_9 = (59 + 273.15)
T_w_out_1_5 = (70 + 273.15)
w_w = 0.961
V_ng_actual = 1.81974681e-03

outData = {

    "GasComposition": {
        "CH4": CH4,
        "C2H6": C2H6,
        "C3H8": C3H8,
        "C4H10": C4H10,
        "C5H12": C5H12,
        "N2" : N2,
        "CO2" :  CO2,
        "O2" :  O2,
        "CO" :  CO,
        "H2" :  H2,
        "H2S" :  H2S,
        "d_g" :  d_g,
        "d_air" :  d_air,
        "alpha" :  alpha,
        "p_atm": p_atm},
            
    "ObjCharacteristics": {
        "D_in": D_in,
        "D_out": D_out,
        "L": L,
        "delta": delta,
        "a": a,
        "b": b,
        "s": s,
        "D_g_t": D_g_t,
        "D_t_w": D_t_w,
        "A_g_t": A_g_t,
        "A_t_w": A_t_w,
        "N": N,
        "delta_l": delta_l,
        "N_g_1_7": N_g_1_7,
        "N_g_8_9": N_g_8_9,
        "N_w_1_5": N_w_1_5,
        "N_w_6_9": N_w_6_9,
        "k_tr_1_5": k_tr_1_5,
        "k_tr_6_7": k_tr_6_7,
        "k_tr_8_9": k_tr_8_9,
        "c_w": c_w
        
        },
    "ArrayData":{
        "T_air_var": T_air_var,
        "cv_air_var": cv_air_var,
        }
        
        
    }


# try:
#     with open("initialData.json", "r") as read_file:
#         initData = json.load(read_file)
# except :
#     print("Read file error!")
#     quit()
    
try:
    with open("initialData.json", "w") as write_file:
        json.dump(outData, write_file, indent=4)
    write_file.close()
except :
    print("Write file error!")
    quit()


