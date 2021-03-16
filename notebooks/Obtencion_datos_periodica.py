#!/usr/bin/env python
# coding: utf-8

# ## Procesos periodicos

# In[1]:

directorio = "/home/dsc/git/TFM"
with open(directorio + '/data/dateInfo.txt','a') as outFile:
    outFile.write('\n'+"hola1 - ")

import numpy as np
import pandas as pd
import random
pd.options.display.max_columns = None
pd.options.display.max_rows = None
import matplotlib.pyplot as plt


# In[2]:


import math
import time
from datetime import timezone, datetime, date, timedelta
import os
import os.path as path
import requests
import json


# In[3]:


df_estaciones = pd.read_csv('/home/dsc/git/TFM/data/estaciones.csv')

directorio = "/home/dsc/git/TFM"
with open(directorio + '/data/PPP.txt','a') as outFile:
    outFile.write('\n'+"hola1 - ")

# In[4]:


len(df_estaciones)


# In[5]:


import requests
import json

def get_response_aemet(url_base = "", url = "", api_key = "", ide = ""):
    
    call = '/'.join([url_base, url, ide])
    if(ide == ""):
        call = call[:-1]

    headers = {    
        'Accept': 'application/json',  
        'Authorization': 'api_key' + api_key
    }
    response = requests.get(call, headers = headers)
    
    #print(call)
    #print(response.text)
    body = json.loads(response.text)["datos"]
    
    
    response = requests.get(body, headers = headers)
    if response:
        print('Success!')
    else:
        print('An error has occurred.')

    return response.text


# In[6]:


def conversor_coordenadas(coord):
    #Si coord es latitud, al norte dele cuador es siempre positiva
    #Si coord es longitud, al Oeste del Meridiano 0º son negativas
    
    D = int(coord[0:2])
    M = float(coord[2:4])
    S = float(coord[4:6])
    
    #GMS a GD
    DD = float((D) + (M/60) + (S/3600))
        
    if(coord[6] == "S" or coord[6] == "W"):
            DD = -DD
            
    return DD


# In[7]:


def get_response_OW(url = ""):
    
    response = requests.get(url)

    
    if response:
        print('Success!')
    else:
        print('An error has occurred.')

    return response.content


# In[8]:


contador_call = 0
contador_estacion = 0

for estacion in df_estaciones["indicativo"]:
    
    contador_call += 1
    contador_estacion += 1
    print(contador_estacion)
    print(estacion)

      
    api_key1 = "61da1382fcce5b67ce2ca4f27d9a34f4"
    api_key2 = "f21448c171f8f0584b48b3c51c9b6cd6"
    
    if ((contador_call*5) < 990):
        api_key = api_key1
    else:
        api_key = api_key2

    for retardo in range(0,5):

        dia = date.today() + timedelta(days = -retardo)
        dia = "{}-{}-{}".format(dia.year, str(dia.month).zfill(2), str(dia.day).zfill(2))
        print(date.today() + timedelta(days = -retardo))

        dia = datetime.strptime(dia, "%Y-%m-%d")

        # convert datetime to timestamp
        dia_unix = int(datetime.timestamp(dia))

        lat = df_estaciones[df_estaciones["indicativo"] == estacion]["latitud"]
        lat = lat[lat.index[0]]
        lon = df_estaciones[df_estaciones["indicativo"] == estacion]["longitud"]
        lon = lon[lon.index[0]]


        lat = str(float(conversor_coordenadas(lat)))
        lon = str(float(conversor_coordenadas(lon)))

        print(lat, lon)


        time = dia_unix

        url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}".format(lat, lon, time, api_key)


        response = get_response_OW(url)

        response = json.loads(response)
        df_clima_ow = pd.json_normalize(response["hourly"])

        df_we = []
        df_time = []
        df_hour = []
        df_estacion = []
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
        df_fecha = pd.DataFrame(df_fecha, columns=['fecha prediccion']) 


        df_clima_ow = pd.concat([df_clima_ow, df_we], axis=1)
        df_clima_ow = df_clima_ow.drop("weather", axis = 1)

        df_clima_ow = pd.concat([df_estacion, df_clima_ow], axis=1)

        df_time = pd.concat([df_time, df_hour, df_fecha], axis=1)
        df_clima_ow = pd.concat([df_time, df_clima_ow], axis=1)
        df_clima_ow = df_clima_ow.drop("dt", axis = 1)
        #print(df_clima_ow)

        if not(path.exists('/home/dsc/git/TFM/data/clima_ow')):
            df_clima_ow_total = pd.DataFrame()
            df_clima_ow_total.to_csv('/home/dsc/git/TFM/data/clima_ow', index = False, header = False)

        columnas = pd.DataFrame(df_clima_ow.columns)
        columnas = columnas.transpose()

        #Si el tamaño es 0 significa que el contenido está vacio.
        if (os.stat('/home/dsc/git/TFM/data/clima_ow').st_size == 0):
            df_clima_ow.to_csv('/home/dsc/git/TFM/data/clima_ow', header = columnas.all, index = False)
            #print(df_clima_ow.head())
        else:
            df_clima_ow_total = pd.read_csv('/home/dsc/git/TFM/data/clima_ow')
            df_clima_ow_total = df_clima_ow_total.append(df_clima_ow, ignore_index = True)
            #print(df_clima_ow_total)
            df_clima_ow_total.to_csv('/home/dsc/git/TFM/data/clima_ow', index = False, header = columnas.all)   


# ## Predicciones de clima

# In[ ]:


contador_estacion = 0

for estacion in df_estaciones["indicativo"]:
    
    contador_call += 1
    contador_estacion += 1
    print(contador_estacion)
    print(estacion)

    lat = df_estaciones[df_estaciones["indicativo"] == estacion]["latitud"]
    lat = lat[lat.index[0]]
    lon = df_estaciones[df_estaciones["indicativo"] == estacion]["longitud"]
    lon = lon[lon.index[0]]


    lat = str(float(conversor_coordenadas(lat)))
    lon = str(float(conversor_coordenadas(lon)))

    print(lat, lon)

    api_key1 = "61da1382fcce5b67ce2ca4f27d9a34f4"
    api_key2 = "f21448c171f8f0584b48b3c51c9b6cd6"
    
    if ((contador_call*5) < 990):
        api_key = api_key1
    else:
        api_key = api_key2

    exclude = "current,minutely,daily,alerts"

    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(lat, lon, exclude, api_key)


    response = get_response_OW(url)
    response = json.loads(response)
    df_pred_ow = pd.json_normalize(response["hourly"])


    df_we = []
    df_time = []
    df_hour = []
    df_estacion = []
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
    df_fecha = pd.DataFrame(df_fecha, columns=['fecha prediccion']) 

    df_pred_ow = pd.concat([df_pred_ow, df_we], axis=1)
    df_pred_ow = df_pred_ow.drop("weather", axis = 1)

    df_pred_ow = pd.concat([df_estacion, df_pred_ow], axis=1)

    df_time = pd.concat([df_time, df_hour, df_fecha], axis=1)
    df_pred_ow = pd.concat([df_time, df_pred_ow], axis=1)
    df_pred_ow = df_pred_ow.drop("dt", axis = 1)

    
    if not(path.exists('/home/dsc/git/TFM/data/pred_ow')):
        df_pred_ow_total = pd.DataFrame()
        df_pred_ow_total.to_csv('/home/dsc/git/TFM/data/pred_ow', index = False, header = False)

    columnas = pd.DataFrame(df_pred_ow.columns)
    columnas = columnas.transpose()

    #Si el tamaño es 0 significa que el contenido está vacio.
    if (os.stat('/home/dsc/git/TFM/data/pred_ow').st_size == 0):
        df_pred_ow.to_csv('/home/dsc/git/TFM/data/pred_ow', header = columnas.all, index = False)
    else:
        df_pred_ow_total = pd.read_csv('/home/dsc/git/TFM/data/pred_ow')
        df_pred_ow_total = df_pred_ow_total.append(df_pred_ow, ignore_index = True)
        df_pred_ow_total.to_csv('/home/dsc/git/TFM/data/pred_ow', index = False, header = columnas.all)   


# # Radiacion ayer

# In[15]:


import csv

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGVqYW5kcm8ucnVpei5iZXJjaWFub0BnbWFpbC5jb20iLCJqdGkiOiI2NDNmZjZmMi04OTQyLTQ1YzYtODIxNC0yZGU4NmQzMDU0NWYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYxMzQ3NjEwNywidXNlcklkIjoiNjQzZmY2ZjItODk0Mi00NWM2LTgyMTQtMmRlODZkMzA1NDVmIiwicm9sZSI6IiJ9.CCEfI4NjKp9kiTCFsNLQFB-u_oLhcXJTEtdHluoToe8"

url_base = "https://opendata.aemet.es/opendata/api"

estaciones_url = "red/especial/radiacion"

resp = get_response_aemet(url_base, estaciones_url, api_key)

datos_rad = resp[32:]



lines = datos_rad.splitlines()
fecha = (resp.splitlines()[1])[1:len(fecha)-1]

reader = csv.reader(lines)
parsed_csv = list(reader)

titulos = [palabra.strip() for palabra in parsed_csv[0][0].replace(';', ', ').replace("\"", "").split(",")]
filas = [[palabra.strip() for palabra in fila[0].replace(';', ', ').replace("\"", "").split(",")] for fila in parsed_csv[1:]]

#9 y 16 tienen el titulo partido
filas[9][0] = filas[9][0] + filas[9][1]
filas[9].pop(1)
filas[16][0] = filas[16][0] + filas[16][1]
filas[16].pop(1)

df_rad_aemet = pd.DataFrame(columns = titulos, data = filas)
df_rad_aemet.loc[df_rad_aemet['Indicativo'] == '6156', 'Indicativo'] = '6156X'

            
df_fecha = []
for i in range(0, len(df_rad_aemet['Indicativo'])):
    for j in range(0, len(df_estaciones['indicativo'])):
        if (df_rad_aemet['Indicativo'][i] == df_estaciones['indicativo'][j]):
            df_rad_aemet.loc[df_rad_aemet['Indicativo'] == df_estaciones['indicativo'][j], 'Estación'] = df_estaciones['nombre'][j]
    for j in range(0, len(titulos)):
        if(df_rad_aemet.iloc[i][j] == ""):
            #df_rad_aemet.iloc[i][j] =  math.nan
            continue
    df_fecha.append(fecha)
df_fecha = pd.DataFrame(df_fecha, columns=['fecha']) 
df_rad_aemet = pd.concat([df_fecha, df_rad_aemet], axis=1)

    
if not(path.exists('/home/dsc/git/TFM/data/rad_aemet')):
    df_rad_aemet_total = pd.DataFrame()
    df_rad_aemet_total.to_csv('/home/dsc/git/TFM/data/rad_aemet', index = False, header = False)

columnas = pd.DataFrame(df_rad_aemet.columns)
columnas = columnas.transpose()

#Si el tamaño es 0 significa que el contenido está vacio.
if (os.stat('/home/dsc/git/TFM/data/rad_aemet').st_size == 0):
    df_rad_aemet.to_csv('/home/dsc/git/TFM/data/rad_aemet', header = columnas.all, index = False)
else:
    df_rad_aemet_total = pd.read_csv('/home/dsc/git/TFM/data/rad_aemet')
    df_rad_aemet_total = df_rad_aemet_total.append(df_rad_aemet, ignore_index = True)
    df_rad_aemet_total.to_csv('/home/dsc/git/TFM/data/rad_aemet', index = False, header = columnas.all)   


# # Radiación

# In[8]:


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


# In[9]:


import io

def getCamsData(camsFile, nbLinesToSkip):

    # List of variables in CAMS files
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
    for ll in camsFile.readlines():
        cont_lines += 1
        if (cont_lines > nbLinesToSkip):
            ll = ll[0:len(ll)-1]
            print(ll)
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

    dictio = {"dateBegins":dateBegins, "dateEnds":dateEnds, "toa":toa, "cs_ghi":cs_ghi, "cs_bhi":cs_bhi, "cs_dhi":cs_dhi, "cs_bni":cs_bni, "ghi":ghi, "bhi":bhi, "dhi" : dhi, "bni" : bni, "reliability" : reliability}
    datacolumns = pd.DataFrame(dictio)

    return datacolumns


# In[10]:


import math
import time
from bs4 import BeautifulSoup


cont_call_rad = 0

dia = date.today() + timedelta(days = -2)
fecha = "{}-{}-{}".format(dia.year, str(dia.month).zfill(2), str(dia.day).zfill(2))
fecha_ini = fecha
fecha_fin = fecha     

    
for estacion in df_estaciones["indicativo"]:
    
    cont_call_rad += 1
    print(cont_call_rad)
    #time.sleep(2*60) # espera en segundos
    
    print(estacion)

    lat = df_estaciones[df_estaciones["indicativo"] == estacion]["latitud"]
    lat = lat[lat.index[0]]
    lon = df_estaciones[df_estaciones["indicativo"] == estacion]["longitud"]
    lon = lon[lon.index[0]]
        
       
    lat = str(float(conversor_coordenadas(lat)))
    lon = str(float(conversor_coordenadas(lon)))
    print(lat, lon)
        
    correo1 = 'arb%2540technologyenergychain.com'
    correo2 = 'ruizber23%2540gmail.com'
    correo3 = 'alejandro.ruiz.berciano%2540gmail.com'
    if (cont_call_rad < 95):
        correo = correo1
    elif(cont_call_rad > 95 & cont_call_rad < 195):
        correo = correo2
    else:
        correo = correo3
        
    url = 'http://www.soda-is.com/service/wps?Service=WPS&Request=Execute&Identifier=get_cams_radiation&version=1.0.0&DataInputs=latitude={};longitude={};altitude=-999;date_begin={};date_end={};time_ref=UT;summarization=PT01H;username={}&RawDataOutput=irradiation'.format(lat, lon, fecha_ini, fecha_fin, correo)
    print(url)
        
    response = requests.get(url)
    soup = BeautifulSoup(response.content)

    f = soup.text
    nbTotalLines = 0
    nbLinesToSkip = 0
    nbTotalLines, nbLinesToSkip = openAndSkipLines(f, '#')

    if(nbTotalLines < 0):
        print('No hay datos')
        exit()
    sizeData = nbTotalLines - nbLinesToSkip
    df_soda = getCamsData(f, nbLinesToSkip)
        
    if not(path.exists('/home/dsc/git/TFM/data/rad_soda')):
        df_soda_total = pd.DataFrame()
        df_soda_total.to_csv('/home/dsc/git/TFM/data/rad_soda', index = False, header = False)

    columnas = pd.DataFrame(df_soda.columns)
    columnas = columnas.transpose()

    #Si el tamaño es 0 significa que el contenido está vacio.
    if (os.stat('/home/dsc/git/TFM/data/rad_soda').st_size == 0):
        df_soda.to_csv('/home/dsc/git/TFM/data/rad_soda', header = columnas.all, index = False)
    else:
        df_soda_total = pd.read_csv('/home/dsc/git/TFM/data/rad_soda')
        df_soda_total = df_soda_total.append(df_soda, ignore_index = True)
        df_soda_total.to_csv('/home/dsc/git/TFM/data/rad_soda', index = False, header = columnas.all)   


# In[25]:


df_soda


# In[12]:


get_ipython().system(" jupyter nbconvert --to script 'Obtencion_datos_periodica.ipynb'")


# In[ ]:




