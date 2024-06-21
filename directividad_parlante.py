import numpy as np
import matplotlib.pyplot as plt
import os
from suavizado import suavizado

def sum_energy(frequency, magnitude, f_central, oct):
    if len(frequency) != len(magnitude):
        raise Exception("frequency and magnitude must be the same length")
    
    if oct == 0:
        raise Exception("The octave must be 3, 12, or 24 not 0")
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

def load_data(file_path):
    # Load data from file_path
    try:
        data = np.loadtxt(file_path, delimiter='\t', skiprows=2, usecols=(0, 1))
    except ValueError as e:
        print(f"Error loading data from {file_path}: {e}")
        return None, None
    
    frequency = data[:, 0]  # Assuming frequency in first column
    magnitude = data[:, 1]   # Assuming magnitude in second column
    
    return frequency, magnitude

def load_all_data(folder_path, angles):
    tf_data = {}
    
    for angle in angles:
        file_name = f"sens_{angle}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        freq, mag = load_data(file_path)
        
        if freq is not None and mag is not None:
            tf_data[angle] = (freq, mag)
    
    return tf_data

def calculate_directivity(tf_data, angles, frequencies):
    directivity_matrix = np.zeros((len(angles), len(frequencies)))
    
    for i, angle in enumerate(angles):
        for j, freq in enumerate(frequencies):
            directivity_matrix[i, j] = sum_energy(tf_data[angle][0], tf_data[angle][1], freq, 3)
    
    return directivity_matrix

def plot_sonogram(directivity_matrix, angles, frequencies, measure):
    plt.figure(figsize=(10, 6))
    plt.imshow(directivity_matrix, origin='lower', aspect='auto', extent=[min(frequencies), max(frequencies), min(angles), max(angles)])
    plt.colorbar(label='Directividad (dB)')
    plt.xscale('log')  # Configura el eje x en escala logarítmica
    
    # Define las frecuencias específicas que deseas mostrar en el gráfico
    tick_frequencies = [60, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    plt.xticks(tick_frequencies, tick_frequencies)
    
    # Define los ángulos específicos que deseas mostrar en el gráfico
    custom_angles = [180, 165, 150, 135, 120, 105, 0, 15, 30, 45, 60, 75, 90]
    plt.yticks(custom_angles, custom_angles)
    
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Ángulo (grados)')
    plt.title(f'Sonograma de Directividad del Parlante')
    plt.tight_layout()
    plt.show()

def main():
    angles = [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]
    folder_path = r'C:\Users\Martin\Desktop\1C_2024\Electroacustica1\TP1Python'
    measure = "Parlante"
    tf_data = load_all_data(folder_path, angles)
    
    # Define las frecuencias específicas que deseas mostrar en el gráfico
    frequencies = [60, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    
    directivity_matrix = calculate_directivity(tf_data, angles, frequencies)
    
    plot_sonogram(directivity_matrix, angles, frequencies, measure)

if __name__ == "__main__":
    main()