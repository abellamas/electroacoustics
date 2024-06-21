import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from suavizado import suavizado

# Constante de nivel de referencia en dB SPL
nivel_referencia_dB_SPL = 102.59  # Ejemplo, ajusta según tu configuración

def find_value(data: np.ndarray, value: int):
    """
    Encuentra un valor en un np.ndarray y devuelve el valor encontrado y su índice.

    Parameters
    ----------
    data : numpy.ndarray
        Array de datos.
    value : int
        Valor a buscar.

    Returns
    -------
    tuple
        Índice y valor encontrado.
    """
    dif = np.abs(data - value)
    index = dif.argmin()
    value = data[index]
    
    return (index, value) 

def get_data_smaart(path, file):
    """
    Lee un archivo .txt de Smaart y devuelve las columnas como np.ndarrays.

    Parameters
    ----------
    path : str
        Carpeta donde se encuentran los archivos.
    file : str
        Nombre del archivo a cargar con su extensión.

    Returns
    -------
    list
        Lista de np.ndarrays con frecuencia y magnitud.
    """    
    resp_df = pd.read_csv(f'{path}/{file}', sep='\t', header=None, skiprows=2)
    resp_values = resp_df.to_numpy()

    frequency = np.array([])
    magnitude = np.array([])

    for f in resp_values:
        frequency = np.append(frequency, f[0])
        magnitude = np.append(magnitude, f[1])

    return [frequency, magnitude]

def list_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def main():
    path = "C:/Users/Martin/Desktop/1C_2024/Electroacustica1/TP1Python"
    
    labels = ["Parlante"]
    
    f0, m0 = get_data_smaart(path, "sens_0.txt")
    magnitudes = [m0]
    
    frequency = f0
    
    size_y = 5  # Alto en pulgadas del lienzo
    size_x = size_y * (1 + np.sqrt(5)) / 2  # Proporción áurea para el ancho del lienzo 
    
    index_ref, freq_ref = find_value(frequency, 1000)  # Donde tomar la referencia
    index_20, f_value_20 = find_value(frequency, 20)  # Índice inferior
    index_20k, f_value_20k = find_value(frequency, 20000)  # Índice superior
    frequency = frequency[index_20:index_20k+1]  # Recorte de f entre inf y sup
    mag_ref = m0[index_ref]  # Mag de referencia
    
    fig = plt.figure(figsize=(size_x, size_y))
    
    for i, mag in enumerate(magnitudes):
        mag = mag[index_20:index_20k+1]  # Recorte de m entre inf y sup
        mag_smoothed = suavizado(frequency, mag, 12)  # Suavizado de magnitudes
        
        # Conversión de nivel relativo a dB SPL
        mag_dB_SPL = mag_smoothed + nivel_referencia_dB_SPL
        
        # Gráficos con matplotlib.pyplot
        plt.semilogx(frequency, mag_dB_SPL)
    
    f_xvalues = [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000]
    f_xticks = ["20", "", "", "", "", "", "", "", "100", "", "", "", "", "", "", "", "", "1k", "", "", "", "", "", "", "", "", "10k", "20k"]
    
    plt.xticks(f_xvalues, f_xticks, rotation=45)
    plt.xlim(40, 20000)
    plt.ylim(20, 70)  # Ajusta el límite superior según tus datos
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Nivel (dB SPL)')
    plt.legend(loc="upper right")
    plt.grid()
    plt.savefig(f'img/rta_freq/rta_freq_parlante.png')
    plt.show()

if __name__ == '__main__':
    main()