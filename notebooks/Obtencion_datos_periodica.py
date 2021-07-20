#!/usr/bin/env python
# coding: utf-8

# # Obtaining historical data for prediction models
# This notebook will be used to obtain the historical data necessary for the prediction models to be used in the photovoltaic production prediction application.:
# 
# **Radiation from the day before the call** https://opendata.aemet.es/centrodedescargas/productosAEMET<br>
# **Solar radiation for two days before the day of data obtention** http://www.soda-pro.com/web-services/radiation/cams-radiation-service<br>
# **Climate data for the five days prior to the call** https://openweathermap.org/api/one-call-api#history<br>
# **Weather forecast for the two days after the call** https://openweathermap.org/api/one-call-api<br>
# 
# 
# - [Preparación](#Preparación)<br>
# 
# ### 1. [Weather data of the previous 5 days](#Weather-data-of-the-previous-5-days)
# 
# ### 2. [Weather predictions for the next 2 days](#Weather-predictions-for-the-next-2-days)
# 
# ### 3. [Radiation data from two days before](#Radiation-data-from-two-days-before)
# 
# ### 4. [Radiation from the day before](#Radiation-from-the-day-before)
# 
# ### 5. [Convert the script to a .py so it can be run automatically](#Convert-the-script-to-a-.py-so-it-can-be-run-automatically)
# 

# ## Preparación
# 
# The different libraries, datasets and functions are loaded

# In[14]:


import numpy as np
import pandas as pd
import random
pd.options.display.max_columns = None
pd.options.display.max_rows = None
import matplotlib.pyplot as plt


# In[15]:


import math
import time
from datetime import timezone, datetime, date, timedelta
import os
import requests
import json
import re
import io


# The working directory is set

# In[16]:


get_ipython().run_line_magic('cd', '/home/dsc/git/TFM/')


# In[17]:


directorio = '/home/dsc/git/TFM/'


# Program execution begins

# In[18]:


with open(directorio + 'data/dateInfo.txt','a') as outFile:
    outFile.write('\n' + "Ejecutando funciones: " + str(datetime.now()))


# In[19]:


df_estaciones = pd.read_csv(directorio + 'data/estaciones.csv')


# In[20]:


len(df_estaciones)


# ### ``get_response_aemet()``
# 
# API Aemet function

# In[8]:


import requests
import json

def get_response_aemet(url_base = "", url = "", api_key = "", ide = ""):
    
    # Join the parts of the final url
    call = '/'.join([url_base, url, ide])
    if(ide == ""):
        call = call[:-1]

    headers = {    
        'Accept': 'application/json',  
        'Authorization': 'api_key' + api_key
    }
    response = requests.get(call, headers = headers)
    
    # The body data is obtained
    body = json.loads(response.text)["datos"]
    
    
    response = requests.get(body, headers = headers)
    if response:
        print('Exito')
    else:
        print('Ha ocurrido un error')

    return response.text


# ### ``conversor_coordenadas()``
# 
# GMS to decimal coordinate converter

# In[9]:


def conversor_coordenadas(coord):
    #Si coord es latitud, al norte del ecuador es siempre positiva
    #Si coord es longitud, al oeste del Meridiano 0º son negativas
    
    D = int(coord[0:2])
    M = float(coord[2:4])
    S = float(coord[4:6])
    
    #GMS a GD
    DD = float((D) + (M/60) + (S/3600))
        
    if(coord[6] == "S" or coord[6] == "W"):
            DD = -DD
            
    return DD


# ### ``get_response_OW()``
# 
# OpenWeather API

# In[10]:


def get_response_OW(url = ""):
    
    response = requests.get(url)

    if response:
        print('Exito')
    else:
        print('Ha ocurrido un error')

    return response.content


# ### ``openAndSkipLines()``
# 
# Function to count the lines up to the data from the CAMS API response

# In[11]:


from datetime import datetime
import os
import re
import io

def openAndSkipLines(f, symbol):
# open a file, e.g. a CSV file, and skip lines beginning with symbol. Return the total number of lines and number of lines to skip (i.e. not containing data). If <0, file is empty
# The file is ready to be read at the first line of data

    buf = io.StringIO(f)
    
    nbTotalLines = len(buf.read())
    if(nbTotalLines == 0): return -1, -1
    buf.seek(0,0)
    stop = False
    nbLine = 0
    while (not stop) :
        nbLine = nbLine + 1
        l = buf.readline()
        if (l[0] != symbol): stop = True
    buf.seek(buf.tell()-len(l),0)
    nbLinesToSkip = nbLine-1
    return nbTotalLines, nbLinesToSkip 


# ### ``getCamsData()``
# 
# Function to generate dataframe with the data from the CAMS API response

# In[12]:


import io

def getCamsData(camsFile, nbLinesToSkip):

    # CAMS variable list:
    # Observation period;TOA;Clear sky GHI;Clear sky BHI;Clear sky DHI;Clear sky BNI;GHI;BHI;DHI;BNI;Reliability
    camsFile = io.StringIO(camsFile) 
    datacolumns = pd.DataFrame()
    dateBegins = list()
    dateEnds = list()
    toa = list()
    cs_ghi = list()
    cs_bhi = list()
    cs_dhi = list()
    cs_bni = list()
    ghi = list()
    bhi = list()
    dhi = list()
    bni = list()
    reliability = list()
    cont_lines = 0
    
    # The data of each row is stored
    for ll in camsFile.readlines():
        cont_lines += 1
        if (cont_lines > nbLinesToSkip):
            ll = ll[0:len(ll)-1]
            #print(ll)
            l = ll.split(';')
            date = l[0].split('/')
            dateBegins.append(date[0].strip())
            dateEnds.append(date[1].strip())
            toa.append(l[1].strip())
            cs_ghi.append(l[2].strip())
            cs_bhi.append(l[3].strip())
            cs_dhi.append(l[4].strip())
            cs_bni.append(l[5].strip())
            ghi.append(l[6].strip())
            bhi.append(l[7].strip())
            dhi.append(l[8].strip())
            bni.append(l[9].strip())
            reliability.append(l[10].strip())

    # The data frame is generated
    dictio = {"dateBegins":dateBegins, "dateEnds":dateEnds, "toa":toa, "cs_ghi":cs_ghi, "cs_bhi":cs_bhi, "cs_dhi":cs_dhi, "cs_bni":cs_bni, "ghi":ghi, "bhi":bhi, "dhi" : dhi, "bni" : bni, "reliability" : reliability}
    datacolumns = pd.DataFrame(dictio)

    return datacolumns


# In[13]:


with open(directorio + 'data/dateInfo.txt','a') as outFile:
    outFile.write('\n' + "Funciones ejecutadas, ejecutando CLIMA: " + str(datetime.now()))


# # Weather data of the previous 5 days
# <div style = "float:right"><a style="text-decoration:none" href = "#Obtaining-historical-data-for-prediction-models">

# This data is obtained from the OpenWeather portal (thanks to a student license that allows making a large number of calls per day) (https://openweathermap.org/api/one-call-api#history). **Data in UTC.** The hourly weather data for the 5 days prior to the call is accessed. The fields obtained are:
# 
# - ``dt``: Time of historical data, Unix, UTC
# - ``temp``: Temperature. Units: kelvin
# - ``feels_like``:  Temperature. This accounts for the human perception of weather. Units: kelvin
# - ``pressure``: Atmospheric pressure on the sea level, hPa
# - ``humidity``: Humidity, %
# - ``dew_point``: Atmospheric temperature below which water droplets begin to condense and dew can form. Units: kelvin
# - ``clouds``: Cloudiness, %
# - ``visibility``: Average visibility, metres
# - ``wind_speed``: Wind speed. Wind speed. Units: m/s
# - ``wind_gust``: Wind gust. Units: m/s
# - ``wind_deg``: Wind direction, degrees (meteorological)
# - ``rain``: Precipitation volume, mm
# - ``snow``: Snow volume, mm
# - ``weather``: Includes an id and other parameters

# In[14]:


try:
    contador_call = 0
    contador_estacion = 0

    # For each station
    for estacion in df_estaciones["indicativo"]:


        contador_estacion += 1
        print("Estación numero {}".format(contador_estacion))
        print("Estación {}".format(estacion))


        # API password
        api_key = "f21448c171f8f0584b48b3c51c9b6cd6"
        
        # For each historical day (previous 5 days)
        for retardo in range(0,5):

            contador_call += 1

            dia = date.today() + timedelta(days = -retardo)
            dia = "{}-{}-{}".format(dia.year, str(dia.month).zfill(2), str(dia.day).zfill(2))
            print("fecha: {}".format(date.today() + timedelta(days = -retardo)))

            dia = datetime.strptime(dia, "%Y-%m-%d")

            # Convert datetime to timestamp
            dia_unix = int(datetime.timestamp(dia))

            lat = df_estaciones[df_estaciones["indicativo"] == estacion]["latitud"]
            lat = lat[lat.index[0]]
            lon = df_estaciones[df_estaciones["indicativo"] == estacion]["longitud"]
            lon = lon[lon.index[0]]

            lat = str(float(conversor_coordenadas(lat)))
            lon = str(float(conversor_coordenadas(lon)))

            
            time = dia_unix

            url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}".format(lat, lon, time, api_key)

            print("url: {}".format(url))
            response = get_response_OW(url)
            
            
            # The response data is obtained
            response = json.loads(response)
            df_clima_ow = pd.json_normalize(response["hourly"])
            
            # Extra columns are generated
            
            # Weather indicator
            df_we = []
            # Date of data day
            df_time = []
            # Hour
            df_hour = []
            # Station ID
            df_estacion = []
            # Data collection date
            df_fecha = []
            for m in range(0,24):
                df_we.append(df_clima_ow["weather"][m][0]["id"])
                df_estacion.append(estacion)
                df_time.append(datetime.utcfromtimestamp(int(df_clima_ow["dt"][m])).strftime('%Y-%m-%d'))
                df_hour.append(datetime.utcfromtimestamp(int(df_clima_ow["dt"][m])).strftime('%H:%M'))
                hoy = "{}-{}-{}".format(date.today().year, str(date.today().month).zfill(2), str(date.today().day).zfill(2)) 
                df_fecha.append(hoy)
            
            df_we = pd.DataFrame(df_we, columns=['we']) 
            df_estacion = pd.DataFrame(df_estacion, columns=['estacion'])
            df_time = pd.DataFrame(df_time, columns=['date']) 
            df_hour = pd.DataFrame(df_hour, columns=['hour']) 
            df_fecha = pd.DataFrame(df_fecha, columns=['fecha_prediccion']) 

            # The column with the weather indicator is added
            df_clima_ow = pd.concat([df_clima_ow, df_we], axis=1)
            # The weather row is eliminated, with more indicators
            df_clima_ow = df_clima_ow.drop("weather", axis = 1)
            
            # The column with the station ID is added
            df_clima_ow = pd.concat([df_estacion, df_clima_ow], axis=1)

            # The column is added with the date of the day the data is obtained and the day and hour to which each one corresponds
            # The dt from which they were obtained is eliminated
            df_time = pd.concat([df_time, df_hour, df_fecha], axis=1)
            df_clima_ow = pd.concat([df_time, df_clima_ow], axis=1)
            df_clima_ow = df_clima_ow.drop("dt", axis = 1)

            
            nombre_csv = "clima_ow_" + str(hoy)
            archivo = directorio + 'data/Clima_OW/' + nombre_csv

            # If the file does not exist, it is created
            if not(os.path.exists(archivo)):
                df_clima_ow_total = pd.DataFrame()
                df_clima_ow_total.to_csv(archivo, index = False, header = False)
            
            columnas = pd.DataFrame(df_clima_ow.columns)
            columnas = columnas.transpose()

            # If the size is 0 it means that the content is empty
            if (os.stat(archivo).st_size == 0):
                df_clima_ow.to_csv(archivo, header = columnas.all, index = False)
                #print(df_clima_ow.head())
            else:
                # If it exists, the content is added
                df_clima_ow_total = pd.read_csv(archivo)
                df_clima_ow_total = df_clima_ow_total.append(df_clima_ow, ignore_index = True)
                #print(df_clima_ow_total)
                df_clima_ow_total.to_csv(archivo, index = False, header = columnas.all)   
except:
    with open(directorio + 'data/dateInfo.txt','a') as outFile:
        outFile.write('\n' + "CLIMA ha fallado: " + str(datetime.now()))


# In[15]:


with open(directorio + 'data/dateInfo.txt','a') as outFile:
    outFile.write('\n' + "CLIMA ejecutado, ejecutando PREDICCION: " + str(datetime.now()))


# # Weather predictions for the next 2 days
# <div style = "float:right"><a style="text-decoration:none" href = "#Obtaining-historical-data-for-prediction-models">

# This data is obtained from the OpenWeather portal (thanks to a student license that allows a large number of calls per day) (https://openweathermap.org/api/one-call-api). **Data in UTC.** The hourly weather forecast for the 2 days following the call is accessed. The fields obtained are:
# 
# - ``dt``: Time of the forecasted data, Unix, UTC
# - ``temp``: Temperature. Units: kelvin
# - ``feels_like``: Temperature. This accounts for the human perception of weather. Units: kelvin
# - ``pressure``: Atmospheric pressure on the sea level, hPa
# - ``humidity``: Humidity, %
# - ``dew_point``: Atmospheric temperature (varying according to pressure and humidity) below which water droplets begin to condense and dew can form. Units: kelvin
# - ``uvi``: UV index
# - ``clouds``: Cloudiness, %
# - ``visibility``: Average visibility, metres
# - ``wind_speed``: Wind speed. Units: m/s
# - ``wind_gust``: Wind gust. Units: m/s
# - ``wind_deg``: Wind direction, degrees (meteorological)
# - ``pop``: Probability of precipitation
# - ``rain``: Rain volume for last hour, mm
# - ``snow``: Snow volume for last hour, mm
# - ``weather``: Includes an id and other parameters

# In[16]:


try:
    contador_call = 0
    contador_estacion = 0
    
    
    # For each station
    for estacion in df_estaciones["indicativo"]:

        contador_call += 1
        contador_estacion += 1
        print("Estación numero {}".format(contador_estacion))
        print("Estación {}".format(estacion))

        lat = df_estaciones[df_estaciones["indicativo"] == estacion]["latitud"]
        lat = lat[lat.index[0]]
        lon = df_estaciones[df_estaciones["indicativo"] == estacion]["longitud"]
        lon = lon[lon.index[0]]


        lat = str(float(conversor_coordenadas(lat)))
        lon = str(float(conversor_coordenadas(lon)))


        api_key= "f21448c171f8f0584b48b3c51c9b6cd6"

        exclude = "current,minutely,daily,alerts"

        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(lat, lon, exclude, api_key)


        response = get_response_OW(url)
        response = json.loads(response)
        df_pred_ow = pd.json_normalize(response["hourly"])


        # Extra columns are generated
            
        # Weather indicator
        df_we = []
        # Date of data day
        df_time = []
        # Hour
        df_hour = []
        # Station ID
        df_estacion = []
        # Data collection date
        df_fecha = []
        for m in range(0,48):
            df_we.append(df_pred_ow["weather"][m][0]["id"])
            df_estacion.append(estacion)
            df_time.append(datetime.utcfromtimestamp(int(df_pred_ow["dt"][m])).strftime('%Y-%m-%d'))
            df_hour.append(datetime.utcfromtimestamp(int(df_pred_ow["dt"][m])).strftime('%H:%M'))
            hoy = "{}-{}-{}".format(date.today().year, str(date.today().month).zfill(2), str(date.today().day).zfill(2)) 
            df_fecha.append(hoy)
        df_we = pd.DataFrame(df_we, columns=['we'])  
        df_estacion = pd.DataFrame(df_estacion, columns=['estacion'])
        df_time = pd.DataFrame(df_time, columns=['date']) 
        df_hour = pd.DataFrame(df_hour, columns=['hour'])
        df_fecha = pd.DataFrame(df_fecha, columns=['fecha_prediccion']) 
        
        # The weather indicator is added and the weather column is removed, with more values
        df_pred_ow = pd.concat([df_pred_ow, df_we], axis=1)
        df_pred_ow = df_pred_ow.drop("weather", axis = 1)
        
        # Station ID is added
        df_pred_ow = pd.concat([df_estacion, df_pred_ow], axis=1)

        # The date of the day of the data request and the day and time to which they correspond are added.
        # The column dt, of the day when the values were obtained, is eliminated
        df_time = pd.concat([df_time, df_hour, df_fecha], axis=1)
        df_pred_ow = pd.concat([df_time, df_pred_ow], axis=1)
        df_pred_ow = df_pred_ow.drop("dt", axis = 1)

        nombre_csv = "pred_ow_" + str(hoy)
        archivo = directorio + 'data/Pred_OW/' + nombre_csv
        
        # If the file does not exist, it is created
        if not(os.path.exists(archivo)):
            df_pred_ow_total = pd.DataFrame()
            df_pred_ow_total.to_csv(archivo, index = False, header = False)

        columnas = pd.DataFrame(df_pred_ow.columns)
        columnas = columnas.transpose()

        # If the size is 0 it means that the content is empty
        if (os.stat(archivo).st_size == 0):
            df_pred_ow.to_csv(archivo, header = columnas.all, index = False)
        else:
            # If it already exists, the data is added
            df_pred_ow_total = pd.read_csv(archivo)
            df_pred_ow_total = df_pred_ow_total.append(df_pred_ow, ignore_index = True)
            df_pred_ow_total.to_csv(archivo, index = False, header = columnas.all)   
except:
    with open(directorio + 'data/dateInfo.txt','a') as outFile:
        outFile.write('\n' + "PREDICCION ha fallado: " + str(datetime.now()))


# In[17]:


with open(directorio + 'data/dateInfo.txt','a') as outFile:
    outFile.write('\n' + "PREDICCION ejecutada, ejecutando RADIACION AEMET: " + str(datetime.now()))


# # Radiation from the day before
# <div style = "float:right"><a style="text-decoration:none" href = "#Obtaining-historical-data-for-prediction-models">

# **These data are only available for the different radiation stations**

# the accumulated hours (**TRUE SOLAR TIME**) of global, direct, diffuse and infrared radiation. These data are obtained from the AEMET Opendata portal (https://opendata.aemet.es/centrodedescargas/productosAEMET). The fields obtained for each day are:
# 
# - ``Estación``: Name of the station
# - ``Indicativo``: Indicative Climatological Station
# - ``Tipo``: Measured variable (Global/Diffuse/Direct/Erythematic UV/Infrared)
# - ``GL/DF/DT``: Hourly radiation accumulated between: (indicated hour -1) and (indicated hour) between 5 and 20. True Solar Time. Variables: Global/Diffuse/Direct (10 * kJ/m²)
# - ``UVER``: Semi-hourly radiation accumulated between: (hour: indicated minutes - 30 minutes and (hour: indicated minutes) between 4:30 and 20. True Solar Time. Variables: Erythematic Ultraviolet Radiation (J/m²)
# - ``IR``: Hourly radiation accumulated between (indicated hour -1) and (indicated hour) between 1 and 24 True Solar Time. Variables: Infrared radiation (10 * kJ/m²)
# - ...

# It will not be necessary to transform the hour as it is approximately equal to UTC (https://relojesdesol.info/node/748)

# In[18]:


try:
    import csv
    
    hoy = "{}-{}-{}".format(date.today().year, str(date.today().month).zfill(2), str(date.today().day).zfill(2)) 

    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGVqYW5kcm8ucnVpei5iZXJjaWFub0BnbWFpbC5jb20iLCJqdGkiOiI2NDNmZjZmMi04OTQyLTQ1YzYtODIxNC0yZGU4NmQzMDU0NWYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYxMzQ3NjEwNywidXNlcklkIjoiNjQzZmY2ZjItODk0Mi00NWM2LTgyMTQtMmRlODZkMzA1NDVmIiwicm9sZSI6IiJ9.CCEfI4NjKp9kiTCFsNLQFB-u_oLhcXJTEtdHluoToe8"

    url_base = "https://opendata.aemet.es/opendata/api"

    estaciones_url = "red/especial/radiacion"

    resp = get_response_aemet(url_base, estaciones_url, api_key)
    
    # The data is processed
    datos_rad = resp[32:]

    lines = datos_rad.splitlines()
    fecha = (resp.splitlines()[1])
    fecha = fecha[1:len(fecha)-1]

    reader = csv.reader(lines)
    parsed_csv = list(reader)

    titulos = [palabra.strip() for palabra in parsed_csv[0][0].replace(';', ', ').replace("\"", "").split(",")]
    filas = [[palabra.strip() for palabra in fila[0].replace(';', ', ').replace("\"", "").split(",")] for fila in parsed_csv[1:]]

    # Some stations have the split title, we have to join the strings
   
    #filas[9][0] = filas[9][0] + filas[9][1]
    #filas[9].pop(1)
    filas[15][0] = filas[15][0] + filas[15][1]
    filas[15].pop(1)

    # An indicative is corrected
    df_rad_aemet = pd.DataFrame(columns = titulos, data = filas)
    df_rad_aemet.loc[df_rad_aemet['Indicativo'] == '6156', 'Indicativo'] = '6156X'
    
    
    # The column with the date to which the data corresponds is added
    # It is also ensured that the names of the stations that are also in the station list are the same
    df_fecha = []
    for i in range(0, len(df_rad_aemet['Indicativo'])):
        for j in range(0, len(df_estaciones['indicativo'])):
            if (df_rad_aemet['Indicativo'][i] == df_estaciones['indicativo'][j]):
                df_rad_aemet.loc[df_rad_aemet['Indicativo'] == df_estaciones['indicativo'][j], 'Estación'] = df_estaciones['nombre'][j]
        for j in range(0, len(titulos)):
            if(df_rad_aemet.iloc[i][j] == ""):
                continue
        df_fecha.append(fecha)
    df_fecha = pd.DataFrame(df_fecha, columns=['fecha']) 
    df_rad_aemet = pd.concat([df_fecha, df_rad_aemet], axis=1)


    nombre_csv = "rad_aemet_" + str(hoy)
    archivo = directorio + 'data/Rad_AEMET/' + nombre_csv
    
    # If the file does not exist, it is created
    if not(os.path.exists(archivo)):
        df_rad_aemet_total = pd.DataFrame()
        df_rad_aemet_total.to_csv(archivo, index = False, header = False)

    columnas = pd.DataFrame(df_rad_aemet.columns)
    columnas = columnas.transpose()
    
    
    # If the size is 0 it means that the content is empty
    if (os.stat(archivo).st_size == 0):
        df_rad_aemet.to_csv(archivo, header = columnas.all, index = False)
    else:
        # If the file already exists, the new content is added
        df_rad_aemet_total = pd.read_csv(archivo)
        df_rad_aemet.columns = df_rad_aemet_total.columns
        df_rad_aemet_total = pd.concat([df_rad_aemet_total, df_rad_aemet], axis=0, ignore_index=True)
        df_rad_aemet_total.to_csv(archivo, index = False, header = columnas.all)   
        
except:
    with open(directorio + 'data/dateInfo.txt','a') as outFile:
        outFile.write('\n' + "RAD AEMET ha fallado: " + str(datetime.now()))


# In[19]:


with open(directorio + 'data/dateInfo.txt','a') as outFile:
    outFile.write('\n' + "RADIACION AEMET ejecutada, ejecutando RADIACION SODA: " + str(datetime.now()))


# # Radiation data from two days before
# <div style = "float:right"><a style="text-decoration:none" href = "#Obtaining-historical-data-for-prediction-models">

# These data are obtained from the CAMS Radiation Service portal of the European Union (http://www.soda-pro.com/web-services/radiation/cams-radiation-service). **In UTC hour.** Provide radiation for any date up to 2 days before the call (3 day delay). The fields obtained for each day are:
# 
# - ``Observation period``: Beginning/end of the time period with the format "yyyy-mm-ddTHH:MM:SS.S/yyyy-mm-ddTHH:MM:SS.S"
# - ``TOA``: Irradiation on horizontal plane at the top of atmosphere (Wh/m2) computed from Solar Geometry 2
# - ``Clear sky GHI``: Clear sky global irradiation on horizontal plane at ground level (Wh/m2)
# - ``Clear sky BHI``: Clear sky beam irradiation on horizontal plane at ground level (Wh/m2)
# - ``Clear sky DHI``: Clear sky diffuse irradiation on horizontal plane at ground level (Wh/m2)
# - ``Clear sky BNI``: Clear sky beam irradiation on mobile plane following the sun at normal incidence (Wh/m2)
# - ``GHI``: Global irradiation on horizontal plane at ground level (Wh/m2)
# - ``BHI``: Beam irradiation on horizontal plane at ground level (Wh/m2)
# - ``DHI``: Diffuse irradiation on horizontal plane at ground level (Wh/m2)
# - ``BNI``: Beam irradiation on mobile plane following the sun at normal incidence (Wh/m2)
# - ``Reliability``: Proportion of reliable data in the summarization (0-1)

# In[20]:


try:
    import math
    import time
    from bs4 import BeautifulSoup
    
    hoy = "{}-{}-{}".format(date.today().year, str(date.today().month).zfill(2), str(date.today().day).zfill(2)) 

    cont_call_rad = 0

    dia = date.today() + timedelta(days = -2)
    fecha = "{}-{}-{}".format(dia.year, str(dia.month).zfill(2), str(dia.day).zfill(2))
    print(fecha)
    fecha_ini = fecha
    fecha_fin = fecha     


    for estacion in df_estaciones["indicativo"]:

        cont_call_rad += 1
        #time.sleep(2*60) # espera en segundos
        print("Llamada numero {}".format(cont_call_rad))
        print("Estación {}".format(estacion))

        lat = df_estaciones[df_estaciones["indicativo"] == estacion]["latitud"]
        lat = lat[lat.index[0]]
        lon = df_estaciones[df_estaciones["indicativo"] == estacion]["longitud"]
        lon = lon[lon.index[0]]


        lat = str(float(conversor_coordenadas(lat)))
        lon = str(float(conversor_coordenadas(lon)))
        print(lat, lon)

        # Three emails are used, because only 100 calls are allowed per day
        correo1 = 'prueba.soda1%2540gmail.com'
        correo2 = 'adelgaster69%2540gmail.com'
        correo3 = 'alejandro.ruiz.berciano%2540gmail.com'

        if (cont_call_rad <= 99):
            correo = correo1
        elif(cont_call_rad > 99 and cont_call_rad <= 199):
            correo = correo2
        elif(cont_call_rad > 199):
            correo = correo3


        url = 'http://www.soda-is.com/service/wps?Service=WPS&Request=Execute&Identifier=get_cams_radiation&version=1.0.0&DataInputs=latitude={};longitude={};altitude=-999;date_begin={};date_end={};time_ref=UT;summarization=PT01H;username={}&RawDataOutput=irradiation'.format(lat, lon, fecha_ini, fecha_fin, correo)
        print(url)

        response = requests.get(url)
        
        # The response is converted into text and it is determined how many lines there are until the data
        soup = BeautifulSoup(response.content)

        f = soup.text
        nbTotalLines = 0
        nbLinesToSkip = 0
        nbTotalLines, nbLinesToSkip = openAndSkipLines(f, '#')

        if(nbTotalLines < 0):
            print('No hay datos')
            exit()
        sizeData = nbTotalLines - nbLinesToSkip
        
        # The data frame is created and a column is added with the station ID
        df_soda = getCamsData(f, nbLinesToSkip)
        df_soda.insert(len(df_soda.columns),"estacion",list(np.repeat([estacion], len(df_soda["dateEnds"]))),True)
        
        nombre_csv = "rad_soda_" + str(hoy)
        archivo = directorio + 'data/Rad_SODA/' + nombre_csv
        
        # If the file does not exist, it is generated
        if not(os.path.exists(archivo)):
            print("el archivo no existe")
            df_soda_total = pd.DataFrame()
            df_soda_total.to_csv(archivo, index = False, header = False)

        columnas = pd.DataFrame(df_soda.columns)
        columnas = columnas.transpose()

        

        # If the size is 0 it means that the content is empty
        if (os.stat(archivo).st_size == 0):
            df_soda.to_csv(archivo, header = columnas.all, index = False)
        else:
            # If the file exists, the data is added
            df_soda_total = pd.read_csv(archivo)
            df_soda_total = df_soda_total.append(df_soda, ignore_index = True)
            df_soda_total.to_csv(archivo, index = False, header = columnas.all)   
except:
    with open(directorio + 'data/dateInfo.txt','a') as outFile:
        outFile.write('\n' + "RAD SODA ha fallado: " + str(datetime.now()))


# In[21]:


with open(directorio + 'data/dateInfo.txt','a') as outFile:
    outFile.write('\n' + "RADIACION SODA ejecutado: " + str(datetime.now()))


# # Convert the script to a .py so it can be run automatically
# <div style = "float:right"><a style="text-decoration:none" href = "#Obtaining-historical-data-for-prediction-models">

# To be able to run it daily automatically using *cron*, it is needed to convert this notebook into ``.py`` format

# In[24]:


get_ipython().system(" jupyter nbconvert --to script ./notebooks/'Obtencion_datos_periodica.ipynb'")

