import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from suavizado import suavizado


def find_value(data: np.ndarray, value: int):
        
    """
    Allow finding a value in a np.ndarray and returns the nearby value found with the index 
    
    Parameters
    ----------
    data : numpy.ndarray
        Frequencies from lowest to highest
    value : numpy.ndarray
        Value to find

    Returns
    -------
    out : tuple
        Tuple of two elements, the index of the value and the value founded

    """

    dif = np.abs(data - value)
    index = dif.argmin()
    value = data[index]
    
    return (index, value) 

def get_data_smaart(path, file):
    
    """
    Read the .txt with Smaart data, and returns the values of cols separated in np.ndarrays
    
    Parameters
    ----------
    path : str
        Folder where the files are saved.
    file : str
        Name of the file to load with the extension

    Returns
    -------
    out : list
        List of np.ndarray with frequency, magnitude and phase

    """    

    # Lectura de datos del txt, se borran las primeras columnas del .txt para facilidad
    # Frecuencia ---- Magnitud ---- Fase ---- Coherencia
    resp_df = pd.read_csv(f'{path}/{file}', sep='\t', header=None, skiprows=2)
    resp_values = resp_df.to_numpy() # dataframe se pasa a numpy array

    #Separación de datos en arrays independientes
    frequency = np.array([])
    magnitude = np.array([])
    phase = np.array([])

    for f in resp_values:
        frequency = np.append(frequency, f[0])
        magnitude = np.append(magnitude, f[1])
        phase = np.append(phase, f[2])

    return [frequency, magnitude, phase]

def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def main():
    
    # Usage
    files = list_files_in_directory("datos/rta_freq")

    for rta in files:
    
        frequency, magnitude, phase = get_data_smaart("datos/rta_freq", rta)

        # Valor mas cercano en frecuencia a 1000 Hz
        index_ref, freq_ref = find_value(frequency, 1000)

        magnitude = suavizado(frequency, magnitude, 12)
        mag_ref = magnitude[index_ref]
        index_20, f_value_20 = find_value(frequency, 20)
        index_20k, f_value_20k = find_value(frequency, 20000)
        frequency = frequency[index_20:index_20k+1]
        magnitude = magnitude[index_20:index_20k+1]

        magnitude_norm = np.array([])

        for m in magnitude:
            magnitude_norm = np.append(magnitude_norm, m-mag_ref)
            
        f_xvalues = [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000]
        f_xticks = ["20", "", "", "", "", "", "", "", "100", "", "", "", "", "", "", "", "", "1k", "", "", "", "", "", "", "", "", "10k", "20k"]

        # Graficos con matplotlib.pyplot

        size_y = 5 #ancho en pulgadas
        size_x = size_y*(1+np.sqrt(5))/2 #proporcion aurea
        fig = plt.figure(figsize=(size_x, size_y))
        plt.semilogx(frequency, magnitude_norm, label=rta[9:-4])
        plt.xticks(f_xvalues, f_xticks, rotation=45)
        plt.xlim(20, 20000)
        plt.ylim(-10, 10)
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud [dB]')
        plt.legend(loc="upper right")
        plt.grid()
        plt.savefig(f'img/rta_freq/{rta[0:-4]}.png')

if __name__ == '__main__':
    main()
    