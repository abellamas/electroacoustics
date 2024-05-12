import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from suavizado import suavizado


def find_value(data, value):
    dif = np.abs(data - value)
    index = dif.argmin()
    value = data[index]
    
    return index, value 

resp_df = pd.read_csv('datos/rta_freq_sm57.txt', sep='\t', header=None)
resp_values = resp_df.to_numpy() #Para tener los datos numericos en un array

# Frecuencia ---- Magnitud ---- Fase ---- Coherencia

#print(resp_values)

frecuencia = np.array([])
magnitud = np.array([])

for f in resp_values:
    frecuencia = np.append(frecuencia, f[0])
    magnitud = np.append(magnitud, f[1])

#print (frecuencia.shape, magnitud.shape)

# Valor mas cercano en frecuencia a 1000 Hz
index_1000, value_1000 = find_value(frecuencia, 1000)
frec_ref = value_1000
mag_ref = magnitud[index_1000]

#print(frec_ref, mag_ref)

index_20, value_20 = find_value(frecuencia, 20)
index_20k, value_20k = find_value(frecuencia, 20000)
frecuencia = frecuencia[index_20:index_20k+1]
magnitud = magnitud[index_20:index_20k+1]

magnitud_normalizada = np.array([])

for m in magnitud:
    magnitud_normalizada = np.append(magnitud_normalizada, m-mag_ref)
    
mag_suavizada = suavizado(frecuencia, magnitud_normalizada, 12)

f_values_x = [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000]
# f_xticks = ["20", "30", "40", "50", "60", "70", "80", "90", "100", "200", "300", "400", "500", "600", "700", "800", "900", "1k", "2k", "3k", "4k", "5k", "6k", "7k", "8k", "9k", "10k", "20k"]
f_xticks = ["20", "", "", "", "", "", "", "", "100", "", "", "", "", "", "", "", "", "1k", "", "", "", "", "", "", "", "", "10k", "20k"]
# f_ticks_x = list(map(str, f_values_x))
size_y = 5
size_x = size_y*(1+np.sqrt(5))/2
fig = plt.figure(figsize=(size_x, size_y))
plt.semilogx(frecuencia, mag_suavizada)
plt.xticks(f_values_x, f_xticks, rotation=45)
plt.xlim(80, 20000)
plt.ylim(-10, 10)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.grid()
plt.savefig("img/SM57_rta_freq.png")

# print(A)