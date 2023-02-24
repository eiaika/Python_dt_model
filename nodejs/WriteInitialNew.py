


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


#R_un = 8.314



# Конструктивні характеристики
D_in = 0.225
D_out = 0.180

delta = 0.001


N = 1
N_g_1_7 = 7
N_g_8_9 = 2
N_w_1_5 = 5
N_w_6_9 = 4

# Коефцієнти теплопередачі
k_tr_1_5 = 704 #
k_tr_6_7 = 704
k_tr_8_9 = 704

# Температура продуктів згорання на вході у пучок
T_g_in = (1200 + 273.15)
# Вхідні сигнали

w_w = 0.961

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
        "alpha" :  alpha},
            
    "ObjCharacteristics": {
        "D_in": D_in,
        "D_out": D_out,
        "delta": delta,
        "N": N,
        "N_g_1_7": N_g_1_7,
        "N_g_8_9": N_g_8_9,
        "N_w_1_5": N_w_1_5,
        "N_w_6_9": N_w_6_9,
        "k_tr_1_5": k_tr_1_5,
        "k_tr_6_7": k_tr_6_7,
        "k_tr_8_9": k_tr_8_9,
        "T_g_in": T_g_in,
        "w_w": w_w
        
        }
    }


# try:
#     with open("initialData.json", "r") as read_file:
#         initData = json.load(read_file)
# except :
#     print("Read file error!")
#     quit()
    
try:
    with open("confData\initialData.json", "w") as write_file:
        json.dump(outData, write_file, indent=4)
    write_file.close()
except :
    print("Write file error!")
    quit()


