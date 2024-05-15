import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from respuesta_frecuencia import get_data_smaart, find_value
from suavizado import suavizado


def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def sum_energy(frequency, magnitude, f_central, oct):
    if len(frequency) != len(magnitude):
        raise Exception("frequency and magnitude they must be the same length")
    
    if oct == 0:
        raise Exception("The octave must be 3, 12 or 24 not 0")
    else:
        ampsmooth_db = np.zeros(np.size(magnitude))
        finf = f_central / pow(2, 1 / (2 * oct))  # calcula el corte inferior
        fsup = f_central * pow(2, 1 / (2 * oct))  # calcula el corte superior
        print("f_inf: ", finf)
        print("f_sup: ", fsup)
        
        idx = np.logical_and(
                frequency >= finf, frequency <= fsup
            )  # busca los elementos dentro del rango de frecuencias
        
        energy = pow(10, magnitude[idx] / 10)
        mag_avg = 10 * np.log10(sum(energy) / len(energy))
        
        print(mag_avg)
        
        return mag_avg



def main():
    # Usage
    dir_ecm8000 = "datos/patron_polar/ECM8000_TF_0"
    dir_sm57 = "datos/patron_polar/SM57_TF_0"
    files_ecm8000 = list_files_in_directory(dir_ecm8000)
    files_ecm8000.sort()
    files_sm57 = list_files_in_directory(dir_ecm8000)
    tf_ecm8000 = {} # diccionario donde se guardará cada medicion con nombre del archivo como clave y en valores una tupla de freq, mag y pha
    # print(files_ecm8000)
    
    # lectura de archivos
    for tf in files_ecm8000:
        tf_data = get_data_smaart(dir_ecm8000, tf)
        tf_ecm8000[tf[13:-4]] = tf_data    #hardcoding de 13:-4 para el ECM8000 y ?:-4 para el SM57

    # ordenamiento para lectura de los archivos de 0 a 180
    azimuth_list = list(map(int, list(tf_ecm8000.keys())))
    azimuth_list.sort()
    azimuth_list = list(map(str, azimuth_list))
    
    # calculo de la magnitud en la frecuencia de interes, por tercio de octava
    mag_per_azimuth = {}
    for azimuth in azimuth_list:
        # magnitudes = tf_ecm8000[azimuth]
        # for tf in tf_ecm8000:
        mag_per_azimuth[azimuth] = sum_energy(tf_ecm8000[azimuth][0], tf_ecm8000[azimuth][1], 63, 3)
    
    # separacion en dos arrays uno con los angulos y otro con las magnitudes
    azimuth_values = list(map(int, list(mag_per_azimuth.keys())))
    mag_values = list(map(np.float32, list(mag_per_azimuth.values())))
    # normalización de la magnitud a 0°
    mag_ref = mag_values[0]
    mag_value_norm = np.array([])
    for mag in mag_values:
        mag_value_norm = np.append(mag_value_norm, mag - mag_ref)
    
    azimuth_values = azimuth_values + [195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345, 360]
    mag_lob_rest = mag_value_norm[::-1]
    mag_lob_rest = np.delete(mag_lob_rest, 0)
    mag_value_norm = np.append(mag_value_norm, mag_lob_rest)
    print(azimuth_values)
    print(mag_value_norm)
    azimuth_values = np.deg2rad(azimuth_values)
    print(azimuth_values)
    
    # Define the directivity pattern for a hypothetical microphone
    # theta = np.linspace(0, 2*np.pi, 1000)  # angle in radians
    theta = azimuth_values
    # r = np.abs(np.sin(theta))  # directivity pattern
    r = mag_value_norm

    # Create the polar plot
    plt.figure()
    ax = plt.subplot( polar=True)
    ax.plot(theta, r)

    # Set the title and labels
    ax.set_title('Microphone Directivity Pattern')
    ax.set_rlim(-10, 1)
    ax.set_theta_offset(np.pi/2)
    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)


    plt.show()

    

    
if __name__ == "__main__":
    main()