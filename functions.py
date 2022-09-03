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


# Aqui voy a descargar los datos historicos de internet para poder usarlos en la inv pasiva
# Cambio los nombres de lo que viene en el excel por los nombres con los que aparecen en yahoo finance
def prices_download(global_tickers):
    global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

    # eliminamos las posiciones que vamos a tomar como cash

    [global_tickers.remove(i) for i in ['USD.MX', 'KOFL.MX', 'KOFUBL.MX', 'BSMXB.MX', 'NMKA.MX']]

    inicio = time.time()
    data = yf.download(global_tickers, start="31-01-2020", end="29-07-2022", actions=False, group_by="close",
                       interval="1d",
                       auto_adjust=False, prepost=False, threads=True)
    print('se tardo', time.time() - inicio, 'segundos')

    return data


# Limpiamos y ordenamos los precios de data que nos interesan
def clean_price(data_archivos, dates_list, data, t_fechas):
    ini_tickers = []
    [ini_tickers.append(j + '.MX') for j in [data_archivos[dates_list[0]]['Ticker']]]
    ini_tickers = np.concatenate(ini_tickers)
    # Bajr los datos de yahoofinance

    ini_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in ini_tickers]

    # quitamos los tickers que no están en el archivo inicial
    [ini_tickers.remove(i) for i in ['KOFL.MX', 'BSMXB.MX']]

    # Obtener los precios de cierre
    data_close = pd.DataFrame({i: data[i]['Close'] for i in ini_tickers})
    precios = data_close.iloc[np.concatenate([np.where(data_close.index.astype(str) == i)[0] for i in t_fechas])]
    precios = precios.reindex(sorted(precios.columns), axis=1)
    return precios, data_close


