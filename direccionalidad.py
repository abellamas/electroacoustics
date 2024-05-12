import pandas as pd
import numpy as np
import matplotlib as plt

sens_df = pd.read_csv('rta_freq_ecm8000.txt', sep=" ", sheet_name='Sensibilidad')
sens_values = sens_df.to_numpy()

direc_df = pd.read_excel('Sensibilidad y Directividad - Curvas Smart.xlsx', sheet_name='Directividad')
direc_values = direc_df.to_numpy()

