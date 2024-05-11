import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from suavizado import suavizado

resp_df = pd.read_csv('datos/rta_freq_ecm8000.txt', sep='\t', header=None)
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
dif = np.abs(frecuencia - 1000)
index_closest_1000 = dif.argmin()

frec_ref = frecuencia[index_closest_1000]
mag_ref = magnitud[index_closest_1000]

#print(frec_ref, mag_ref)

magnitud_normalizada = np.array([])

for m in magnitud:
    magnitud_normalizada = np.append(magnitud_normalizada, m-mag_ref)


A = suavizado(frecuencia,magnitud_normalizada,12)
plt.semilogx(frecuencia, A)
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Sensibilidad [dB SPL]')
plt.grid()
plt.show()

print(A)