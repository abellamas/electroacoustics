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
    path = "datos/rta_freq"
    
    labels = ["SM57 0°", "SM57 180°"]
    f0, m0, p0 = get_data_smaart(path, "SM57_TF_0_0.txt")
    f180, m180, p180 = get_data_smaart(path, "SM57_TF_0_180.txt")
    
    # labels = ["ECM8000 0°", "ECM8000 90°", "ECM8000 180°"]
    # labels = ["ECM8000 0°", "ECM8000 180°"]
    # f0, m0, p0 = get_data_smaart(path, "ECM8000_TF_0_0.txt")
    # # f45, m45, p45 = get_data_smaart(path, "ECM8000_TF_0_90.txt")
    # f180, m180, p180 = get_data_smaart(path, "ECM8000_TF_0_180.txt")

    magnitudes = [m0, m180]
    
    frequency = f0
    
    size_y = 6 #alto en pulgadas del lienzo
    size_x = size_y*(1+np.sqrt(5))/2 #proporcion aurea para ancho lienzo 
    index_ref, freq_ref = find_value(frequency, 1000) # donde tomar la referencia
    index_20, f_value_20 = find_value(frequency, 20) # indice inf
    index_20k, f_value_20k = find_value(frequency, 20000) # indice sup
    frequency = frequency[index_20:index_20k+1] # recorte de f entre inf y sup
    mag_ref = m0[index_ref] #mag de referencia
    
    fig = plt.figure(figsize=(size_x, size_y))
    
    for i, mag in enumerate(magnitudes):
        print(labels[i], mag)
        mag = mag[index_20:index_20k+1] # recorte de m entre inf y sup
        mag = suavizado(frequency, mag, 12) #suavizado de magnitudes

        mag_norm = np.array([]) 

        for m in mag:
            mag_norm = np.append(mag_norm, m-mag_ref)
            
        # mag_norm = mag
        # Graficos con matplotlib.pyplot
        plt.semilogx(frequency, mag_norm, label = labels[i])
        
    
    f_xvalues = [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000]
    f_xticks = ["20", "", "", "", "", "", "", "", "100", "", "", "", "", "", "", "", "", "1k", "", "", "", "", "", "", "", "", "10k", "20k"]
    
    plt.xticks(f_xvalues, f_xticks, rotation=45, fontsize=12, family="arial")
    plt.yticks( fontsize=12, family="arial")   
    plt.xlim(20, 20000)
    plt.ylim(-30, 15)
    plt.xlabel('Frecuencia [Hz]', fontsize=14, family="arial")
    plt.ylabel('Nivel relativo [dB]', fontsize=14, family="arial")
    plt.legend(loc="upper right")
    plt.rc('legend', fontsize=14)
    plt.grid()
    plt.savefig(f'img/rta_freq/SM57_frente_espalda.png')

if __name__ == '__main__':
    main()
    