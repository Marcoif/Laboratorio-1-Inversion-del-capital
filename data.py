
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

#En esta seccion voy a correr toda la data del NAFTRAC
# Para ello necesito las librerias necesarias

import time as time
import pandas as pd
import numpy as np
from datetime import datetime
from glob import glob
import yfinance as yf
import collections
import math



filenames = glob("/Users/marcoochoa/Downloads/MICROESTRUCTURAS DE TRADING/Lab 1/Laboratorio-1-Inversion-del-capital/NAFTRAC/*.csv")

# para poder abrir todos los archivos use la libreria glob para leer todos los csv poniendo la ruta de acceso de los archivos y el *csv al final

# archivos me da la lectura de los archivos con el numero de posiciones
archivos = [filenames[i][-20:-4] for i in range(len(filenames))]


# Crear el diccionario donde metemos todos los datos brindados

data_archivos = {}

#este for me ayuda con la limpieza de los datos para poder trabajar con ellos
for i in filenames:
    data = pd.read_csv(i, skiprows=2, header=None)
    # renombrar las columnas con lo que tiene el 1er renglon
    data.columns = list(data.iloc[0, :])
    # quitar las columnas que no sean nan
    data = data.loc[:, pd.notnull(data.columns)]
    # reiniciar índice
    data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
    # quitar las comas de la columna Precio
    data['Precio'] = [i.replace(',', '') for i in data['Precio']]
    # quitar asterisco de la colmuna ticker
    data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
    # hacer conversiones de tipos de columna a númerico
    convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
    data = data.astype(convert_dict)
    # convertir a decimal la columna de peso (%)
    data['Peso (%)'] = data['Peso (%)'] / 100
    data_archivos[i] = data




