"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import pandas as pd
import numpy as np
import time as time
import yfinance as yf
import math


# %% Paso 1

# Para usar los tickers de yfinance como se solicitaron es necesario mover los csv para dejarlos en el formato necesario
# En esta parte hago la primera funcion para que mis datos queden en una lista como un indice de los archivos

def f_fechas(p_archivos):
    t_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in p_archivos])]
    # lista con fechas ordenadas (para usarse como indexadores de archivos)]
    index_fechas = [j.strftime('%d%m%y') for j in sorted([pd.to_datetime(i[8:]).date() for i in p_archivos])]
    r_f_fechas = {'index_fechas': index_fechas, 't_fechas': t_fechas}

    return r_f_fechas


# Para esta función voy a crear mis tickers del índice y agregarles el .MX para que yfinance me los pueda leer y
# comprarlos desde ahi
def f_global_tickers(data_archivos, filenames):
    tickers = []
    [tickers.append(j + '.MX') for j in [data_archivos[i]['Ticker'] for i in filenames]]

    tickers = np.concatenate(tickers)
    global_tickers = np.unique(tickers).tolist()

    return global_tickers


