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
    index_fechas = [j.strftime('%Y%m%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in p_archivos])]
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

    print(global_tickers)
    # eliminamos las posiciones que vamos a tomar como cash

    [global_tickers.remove(i) for i in ['USD.MX', 'KOFUBL.MX', 'BSMXB.MX', 'NMKA.MX', 'MXN.MX', 'SITESB.1.MX']]

    inicio = time.time()
    data = yf.download(global_tickers, start="2020-01-31", end="2022-07-29", actions=False, group_by="close",
                       interval="1d",
                       auto_adjust=False, prepost=False, threads=True)
    print('se tardo', time.time() - inicio, 'segundos')

    return data


# Limpiamos y ordenamos los precios de data que nos interesan
def clean_price(data_archivos, dates_list, data, t_fechas):
    ini_tickers = []
    [ini_tickers.append(j + '.MX') for j in [data_archivos[dates_list[0]]['Ticker']]]
    ini_tickers = np.concatenate(ini_tickers)
    ini_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in ini_tickers]
    [ini_tickers.remove(i) for i in ['MXN.MX', 'KOFUBL.MX', 'BSMXB.MX']]

    # Bajamos los precios de cierre de yahoo
    data_close = pd.DataFrame({i: data[i]['Close'] for i in ini_tickers})
    precios = data_close.iloc[np.concatenate([np.where(data_close.index.astype(str) == i)[0] for i in t_fechas])]
    precios = precios.reindex(sorted(precios.columns), axis=1)
    return precios, data_close


# Codigo de la inversion pasiva
def pasiva_ini(data_archivos, dates_list, precios):
    k = 1000000
    c = 0.00125
    # En esta parte pongo cuales son los datos que me serviran de cash, extraemos la lista de los archivos que voy a eliminar
    c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'NMKA', 'USD', 'MXN']

    inv_pasiva = {'timestamp': ['31-01-2020'], 'capital': [k]}

    pos_datos = data_archivos[dates_list[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]

    i_activos = list(pos_datos[list(pos_datos['Ticker'].isin(c_activos))].index)

    pos_datos.drop(i_activos, inplace=True)
    # resetear el index
    pos_datos.reset_index(inplace=True, drop=True)
    # Agrego el MX para que pueda leer los archivos
    pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'
    # Corrijo el ticker de liverpool para que lo busque tambien
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')

    match = 0
    m2 = [precios.iloc[match, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]
    pos_datos['Precio'] = m2
    return pos_datos


def inv_pasiva(pos_datos, dates_list, precios):
    k = 1000000
    c = 0.00125

    # Aqui hacemos todas las condiciones para que sepamos cuanto capital nos toma cada peso, los titulos que podemos comprar
    # Nuestras posturas y rendondear para no comprar fracciones de titulos y al final contar cuanto fue la comision
    pos_datos['Capital'] = pos_datos['Peso (%)'] * k - pos_datos['Peso (%)'] * k * c

    pos_datos['Títulos'] = pos_datos['Capital'] / pos_datos['Precio']

    pos_datos['Títulos'] = [math.floor(pos_datos['Títulos'][i]) for i in range(pos_datos.shape[0])]

    pos_datos['Postura'] = pos_datos['Títulos'] * pos_datos['Precio']

    pos_datos['Comisión'] = pos_datos['Títulos'] * pos_datos['Precio'] * c

    # calculamos la suma de todas posiciones y cuanto nos quedo de cash
    pos_value = pos_datos['Postura'].sum()

    cash = 1000000 - pos_value - pos_datos['Comisión'].sum()
    Capital = pos_value + cash

    inv_pasiva = [{'timestamp': '29-07-2022', 'Capital': 1000000, 'rend': 0, 'rend_acum': 0}]

    # ciclo donde se multiplica el precio por la cantidad de titulos
    for i in range(0, len(dates_list) - 1):
        match = i
        m2 = [precios.iloc[match, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]
        pos_datos['Precio'] = m2
        pos_datos['Postura'] = pos_datos['Títulos'] * pos_datos['Precio']

        # Calcular la suma de las posiciones
        pos_value = pos_datos['Postura'].sum()
        Capital = pos_value + cash
        rend = (Capital - inv_pasiva[i]['Capital']) / inv_pasiva[i]['Capital']
        acum = rend + inv_pasiva[i]['rend_acum']
        inv_pasiva.append({'timestamp': dates_list[i], 'Capital': Capital, 'rend': rend, 'rend_acum': acum})

    inv_pasiva = pd.DataFrame(inv_pasiva)

    return inv_pasiva


# A partir de esta parte voy a hacer la inversion activa:


# tomamos las mismas ponderaciones iniciales del archivo del 31 de enero 2022 y hacemos sort con los pesos de mayor a menor
def activa_ini(data_archivos, dates_list, precios):
    activa_ini = data_archivos[dates_list[0]].copy().sort_values('Peso (%)', ascending=False)[
        ['Ticker', 'Nombre', 'Peso (%)']]

    # Hacemos el mismo prcoeso que con la pasiva de eliminar los actovos que seran cash
    c_activos = ['KOFL', 'KOFUBL', 'BSMXB', 'USD', 'MXN', ]
    i_activos = list(activa_ini[list(activa_ini['Ticker'].isin(c_activos))].index)

    # Quitamos las acciones que eliminamos de la lista, reseteamos el index para actualizarlo
    # Agregamos el MX para que se pueda usar de yahoofinance y corregimos los ticker que no esten bien escritos
    activa_ini.drop(i_activos, inplace=True)

    activa_ini.reset_index(inplace=True, drop=True)

    activa_ini['Ticker'] = activa_ini['Ticker'] + '.MX'

    activa_ini['Ticker'] = activa_ini['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')

    # Para la estrategia voy a comenzar con bajarle el peso al activo con mas peso en el naftrac y de ahi ver como se ve
    activa_ini = activa_ini.copy()
    activa_ini.loc[0, 'Peso (%)'] = activa_ini.loc[0, 'Peso (%)'] / 2

    k = 1000000
    c = 0.00125

    match = 0
    m2 = [precios.iloc[match, precios.columns.to_list().index(i)] for i in activa_ini['Ticker']]
    activa_ini['Precio'] = m2

    # Aqui pongo el capital que mando a cada activo
    # La cantidad de titulos por accion
    # El redondeo para no comprar titulos fraccionados
    # El costo de todos los titulos por su precio
    # Las comisiones que me cobra cada transaccion

    activa_ini['Capital'] = activa_ini['Peso (%)'] * k - activa_ini['Peso (%)'] * k * c

    activa_ini['Títulos'] = activa_ini['Capital'] / activa_ini['Precio']

    activa_ini['Títulos'] = [math.floor(activa_ini['Títulos'][i]) for i in range(activa_ini.shape[0])]

    activa_ini['Postura'] = activa_ini['Títulos'] * activa_ini['Precio']

    activa_ini['Comisión'] = activa_ini['Títulos'] * activa_ini['Precio'] * c

    value_activa = activa_ini['Postura'].sum()

    # Esta parte me dice despues de todas las condiciones cuanto dinero nos queda libre en cash para rebalanceo

    cash_ini = 1000000 - value_activa - activa_ini['Comisión'].sum()
    cash_activa = 1000000 - value_activa - activa_ini['Comisión'].sum()

    return activa_ini, cash_ini, cash_activa
