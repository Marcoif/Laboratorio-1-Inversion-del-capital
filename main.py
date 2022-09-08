
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# En esta seccion pondre las funciones mas importantes y que es lo que hacen En esta funcion se construyen los
# archivos de la inversion pasiva para poder trabajar con ellos acomodarlos para poder trabajar con ellos
fechas = fn.f_fechas(p_archivos=dt.archivos)

# Esta funcion me hace ya el indice de todos los archivos para poder leerlos y bajar los datos de yahoofinance

global_tickers = fn.f_global_tickers(data_archivos=dt.data_archivos, filenames=dt.filenames)


# Esta funcion me descarga ya los precios que toma de global tickers para que ya tome el precio de cierre que necesitamos
data = fn.prices_download(global_tickers=global_tickers)


# Esta funcion tambien la agregue en el notebook sirve para ordenar los datos de precio de cierre que se tiene con
# los archivos csv, se explica mejor en el notebook
dates_list = [datetime.datetime.strptime(i, "%Y%m%d").date() for i in fechas['index_fechas']]
for i in range(len(fechas['index_fechas'])):
    for j in range(31):
        if fechas['index_fechas'][i] in dt.filenames[j]:
            dt.data_archivos[fechas['index_fechas'][i]]=dt.data_archivos.pop(dt.filenames[j])
            dt.data_archivos[dates_list[i]]=dt.data_archivos.pop(fechas['index_fechas'][i])

# Esta funcion ya nos muestra el ultimo precio de cierre de los tickers de yahoo
clean_prices, data_close = fn.clean_price(data_archivos=dt.data_archivos, dates_list=dates_list, data=data,
                                          t_fechas=fechas['t_fechas'])

# Esta funcion me crea la primera tabla donde ya se ve el ticker el peso el precio y el nombre de la accion
pos_datos = fn.pasiva_ini(data_archivos=dt.data_archivos, dates_list=dates_list, precios=clean_prices)

# Por ultimo de la inversion pasiva, esta funcion me muestra la tabla de todos los timestamps y muestra el resultado
# de cuanto fue el rendimiento en el periodo y cuanto fue el rendimiento acumulado
inv_pasiva = fn.inv_pasiva(pos_datos=pos_datos, dates_list=dates_list, precios=clean_prices)

# En esta funcion muestro la tabla de los datos que tenemos los precios, titulos, capital, titulos, postura y la comision

activa_ini,cash_activa,cash_ini = fn.activa_ini(data_archivos=dt.data_archivos, dates_list=dates_list,precios=clean_prices)
