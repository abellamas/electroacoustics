import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from respuesta_frecuencia import get_data_smaart, find_value
from suavizado import suavizado

def sum_energy(frequency, magnitude, f_central, oct):
    if len(frequency) != len(magnitude):
        raise Exception("frequency and magnitude they must be the same length")
    
    if oct == 0:
        raise Exception("The octave must be 3, 12 or 24 not 0")
    else:
        ampsmooth_db = np.zeros(np.size(magnitude))
        finf = f_central / pow(2, 1 / (2 * oct))  # calcula el corte inferior
        fsup = f_central * pow(2, 1 / (2 * oct))  # calcula el corte superior
        
        idx = np.logical_and(
                frequency >= finf, frequency <= fsup
            )  # busca los elementos dentro del rango de frecuencias
        
        energy = pow(10, magnitude[idx] / 10)
        mag_avg = 10 * np.log10(sum(energy) / len(energy))
        
        return mag_avg

def load_tf(path, measure, n_measure):
    
    tf_data = {}
    
    for n in n_measure:
        tf_data[n] = get_data_smaart(f'{path}/{measure}', f'{measure}_{n}.txt')
    
    return tf_data

def polar_pattern(tf_measure, angles, frequency:int):
     # calculo de la magnitud en la frecuencia de interes, por tercio de octava
    mag_per_angle = {}
    for angle in angles:
        mag_per_angle[angle] = sum_energy(tf_measure[angle][0], tf_measure[angle][1], frequency, 3)
    
    # separacion en dos arrays uno con los angulos y otro con las magnitudes
    mag_values = list(map(np.float32, list(mag_per_angle.values())))
    
    # normalización de la magnitud a 0°
    mag_ref = mag_values[0]
    mag_values_norm = list(map(lambda m: m - mag_ref, mag_values))
    
    angles = list(np.deg2rad(np.arange(0,361, 15)))
    mag_values_norm = np.append(mag_values_norm, np.delete(mag_values_norm[::-1],0))
    
    return mag_values_norm


def main():
    angles = list(np.arange(0,181, 15))
    path = "datos/patron_polar"
    measure = "ECM8000_TF_0"
    tf_data = load_tf(path, measure, angles)
    
    # frequencies =   [100, 1000, 10000]
    # frequencies = [250, 2000, 8000]
    frequencies = [500, 8000, 16000]    

    magnitudes = []
    
    for freq in frequencies:
        magnitudes.append(polar_pattern(tf_data, angles, freq))
    
    angles = np.deg2rad(np.arange(0, 361, 15))
    # Create the polar plot
    plt.figure()
    ax = plt.subplot( polar=True)
    
    
    ax.plot(angles, magnitudes[0], 'r--', label=f"{frequencies[0]} Hz")
    ax.plot(angles, magnitudes[1], 'g-', label=f"{int(frequencies[1]/1000)} kHz")
    ax.plot(angles, magnitudes[2], 'b-.', label=f"{int(frequencies[2]/1000)} kHz")
    # Set the title and labels
    ax.set_title(measure[:-5])
    ax.set_rlim(-30, 1)
    ax.set_theta_offset(np.pi/2)
    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.25, -0.1) ,loc="lower right")
    plt.savefig(f'img/patron_polar/polar_pattern_{measure}_{frequencies[0]}_{frequencies[1]}_{frequencies[2]}.png')
    

    plt.show()

    

    
if __name__ == "__main__":
    main()