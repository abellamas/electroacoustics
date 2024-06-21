import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            # Encontrar la línea donde comienzan los datos
            start_line = None
            for i, line in enumerate(lines):
                if line.startswith('* Freq(Hz)'):
                    start_line = i + 1
                    break
            
            if start_line is None:
                raise ValueError(f"No data found in {file_path}")
            
            # Leer los datos
            data = np.genfromtxt(file_path, delimiter='\t', skip_header=start_line)
            frequency = data[:, 0]
            impedance = data[:, 1]
            
            return frequency, impedance
        
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        return None, None

def plot_impedance(frequency1, impedance1, frequency2, impedance2):
    plt.figure(figsize=(10, 6))
    
    # Graficar la primera curva de impedancia
    plt.plot(frequency1, impedance1, label='Parlante')
    
    # Graficar la segunda curva de impedancia
    plt.plot(frequency2, impedance2, label='Parlante + Mm 19 g')
    
    plt.xscale('log')  # Escala logarítmica para el eje x
    plt.xlim(10, 10000)
    plt.ylim(0, 60)
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Impedancia (Ohms)')
    plt.title('Curvas de Impedancia')
    plt.legend()
    plt.grid(True)

    # Definir las ubicaciones y etiquetas de los ticks en el eje x
    tick_values = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    tick_labels = ['10', '20', '50', '100', '200', '500', '1k', '2k', '5k', '10k']
    plt.xticks(tick_values, tick_labels)

    plt.tight_layout()
    plt.show()

def main():
    # Archivos de datos
    file_path1 = 'parlante.txt'
    file_path2 = 'parlante_masa.txt'
    
    # Cargar los datos
    freq1, impedance1 = load_data(file_path1)
    freq2, impedance2 = load_data(file_path2)
    
    if freq1 is not None and impedance1 is not None and freq2 is not None and impedance2 is not None:
        # Graficar las curvas de impedancia
        plot_impedance(freq1, impedance1, freq2, impedance2)
    else:
        print("No se pudieron cargar los datos correctamente.")

if __name__ == "__main__":
    main()