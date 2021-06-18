


# Se importan las librerías necesarias

import streamlit as st
import numpy as np
import pandas as pd
import os
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import folium
from folium.plugins import MousePosition
import streamlit.components.v1 as components
import base64


# Se muestra el título y las instrucciones

directorio = '/home/dsc/git/TFM/'
st.image(directorio + 'images/fondo.jpg', width = 800)
html_temp = """
<p style="text-align: center;"><strong><span style="font-size: 50px;
color: rgb(255, 255, 255);">Plataforma de predicci&oacute;n de producci&oacute;n fotovoltaica</span></strong></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)


########################################### MAPA #############################################################

st.text("\n")
st.text("\n")
html_temp = """
<p style="text-align: center;"><span style="font-size: 26px; font-family: Tahoma, Geneva, sans-serif; text-shadow: rgba(255, 240, 36, 0) 3px 3px 2px;
color: rgb(250, 197, 28);">Por favor, seleccione la ubicaci&oacute;n de su instalaci&oacute;n 🗺️</span></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)


# Imagen 

col1, mid, col2 = st.beta_columns([2,6,1])
with col1:
    st.image(directorio + 'images/mapa.png', width = 100)
with mid:
    st.write('Solamente localizaciones válidas en España')


# Se genera el mapa y se leen las coordenadas marcadas por el usuario

hay_coord = 0
_RELEASE = False
if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url = "http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path = build_dir)

def my_component(key = None):
    component_value = _component_func(key = key, default = 0)
    return component_value
if not _RELEASE:
    import streamlit as st
    hay_coord = my_component()
    #st.markdown(clicked_coords)




########################################### BARRA LATERAL #############################################################


# Se solicitan las características de la instalación
    
# Título
html_temp = """
<p style="text-align: center;"><span style="font-size: 22px; font-family: Tahoma, Geneva, sans-serif; text-shadow: 
rgba(255, 240, 36, 0) 3px 3px 2px;"></span><span style="font-size: 22px; font-family: Impact, Charcoal, sans-serif; text-shadow:
rgba(255, 240, 36, 0) 3px 3px 2px;"><strong>Introduzca las caracter&iacute;sticas de su instalaci&oacute;n 🌞</strong></span></p>
"""
st.sidebar.markdown(html_temp, unsafe_allow_html = True)


#### Orientación

html_temp = """
<h4 style="text-align: left;"><span style="color: rgb(250, 197, 28); font-size: 20px;
font-family: Impact, Charcoal, sans-serif;">Orientaci&oacute;n de la instalaci&oacute;n (grados)</span></h4>
"""
st.sidebar.markdown(html_temp, unsafe_allow_html = True)

# Imagen 
col1, mid, col2 = st.sidebar.beta_columns([1.5,7,1])
with col1:
    st.image(directorio + 'images/orientation.png', width = 40)
with mid:
    st.write('Seleccione la orientación de su instalación')

# Orientación 
html_temp = """
<p style="text-align: center;"><em><strong><span style='font-family:
"Lucida Console", Monaco, monospace; font-size: 12px;'>Valores positivos hacia el oeste</span></strong></em></p>
"""
st.sidebar.markdown(html_temp, unsafe_allow_html = True)
orient = st.sidebar.slider(
    label = "Orientación",
    min_value = -180.0,
    max_value = 180.0,
    value = 0.0,
    step = 0.5,
)

# Orientación media de un rango de valores
orient_media_indicador = 0
sidebar_expander_1 = st.sidebar.beta_expander("Si no está seguro de la orientación:")
with sidebar_expander_1:
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])
    with slider_col:
        orient_media = st.slider("Rango de valores", -180, 180, value = (-180,180))   

        
# Mostrar orientación
with sidebar_expander_1:
    if st.button("Borrar rango de orientación"):
        st.success("Valor borrado")
        orient_media = 0
if np.mean(orient_media) != 0:
    orient = np.mean(orient_media)
    st.sidebar.text("Se ha tomado un valor medio")


col1, mid, col2 = st.sidebar.beta_columns([6,5,1])
with col1:
    html_temp = """
    <p style="text-align: center;"><em><strong><span style="font-size:
    12px; color: rgb(250, 197, 28);">Valor de orientaci&oacute;n introducido:</span></strong></em></p>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
with mid:
    st.text("\n")
    st.text("{} grados".format(orient))

    
st.sidebar.text("\n")
st.sidebar.text(" ")


#### Inclinación

html_temp = """
<h4 style="text-align: left;"><span style="color: rgb(250, 197, 28); font-size: 20px;
font-family: Impact, Charcoal, sans-serif;">Inclinaci&oacute;n de la instalaci&oacute;n (grados)</span></h4>
"""
st.sidebar.markdown(html_temp, unsafe_allow_html = True)


# Imagen 
col1, mid, col2 = st.sidebar.beta_columns([2,7,1])
with col1:
    st.image(directorio + 'images/inclination.png', width = 60)
with mid:
    st.write('Seleccione la inclinación de su instalación')

# Inclinación
html_temp = """
<p style="text-align: center;"><em><strong><span style='font-family: "Lucida Console", Monaco, monospace; font-size: 12px;
'>0 grados significa que el panel est&aacute; horizontal y 90&ordm; significa que est&aacute; vertical</span></strong></em></p>
"""
st.sidebar.markdown(html_temp, unsafe_allow_html = True)
incl = st.sidebar.slider(
    label = "Inclinación",
    min_value = 0.0,
    max_value = 90.0,
    value = 25.0,
    step = 0.01,
)

# Inclinación media de un rango de valores
incl_media_indicador = 0
sidebar_expander_2 = st.sidebar.beta_expander("Si no está seguro de la inclinación:")
with sidebar_expander_2:
    _, slider_col, _ = st.beta_columns([0.02, 0.96, 0.02])
    with slider_col:
        incl_media = st.slider("Rango de valores", 0, 90, value = (0,90))   
        
# Mostrar inclinación
with sidebar_expander_2:
    if st.button("Borrar rango de inclinación"):
        st.success("Valor borrado")
        incl_media = (90/2)
        
if np.mean(incl_media) != (90/2):
    incl = np.mean(incl_media)
    st.sidebar.text("Se ha tomado un valor medio")

    
col1, mid, col2 = st.sidebar.beta_columns([6,5,1])
with col1:
    html_temp = """
    <p style="text-align: center;"><em><strong><span style="font-size:
    12px; color: rgb(250, 197, 28);">Valor de inclinaci&oacute;n introducido:</span></strong></em></p>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
with mid:
    st.text("\n")
    st.text("{} grados".format(incl))





########################################### POTENCIA PICO #############################################################


st.text("\n")
html_temp = """
<p style="text-align: center;"><span style="font-size: 26px; font-family: Tahoma, Geneva, sans-serif; text-shadow:
rgba(255, 240, 36, 0) 3px 3px 2px; color: rgb(250, 197, 28);">Introduzca la potencia pico de su instalaci&oacute;n ⚡️</span></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)


# Imagen 
col1, mid, col2 = st.beta_columns([2,6,1])
with col1:
    st.image(directorio + 'images/peak.png', width = 100)
with mid:
    st.write('Seleccione la potencia pico de su instalación en kW')
    
    
# Se solicita la potencia pico 

potencia = 0

html_temp = """
<p style="text-align: left;"><em><strong><span style='font-family: "Lucida Console", Monaco, monospace; font-size: 12px; color: rgb(239, 239, 239);
'>En caso de indicar potencia unitaria (1 kW), los resultados de producci&oacute;n el&eacute;ctrica de su instalaci&oacute;n deber&aacute;
ser multiplicados por la potencia pico real</span></strong></em></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)

message = st.text_area("Introduzca un valor")

try:
    potencia = float(str(message).replace(',', '.'))
except:
    potencia = 0
st.write('O')
if st.checkbox('Usar potencia unitaria (1 kW)'):
    potencia = 1

if potencia == 0:
    html_temp = """
    <p style="text-align: center;"><em><strong><span style="
    12px; color: rgb(250, 197, 28);">Introduzca valor de potencia v&aacute;lido. Ejemplo: 4.5 kW</span></strong></em></p>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
else:
    col1, mid, col2 = st.beta_columns([4,2,1])
    with col1:
        html_temp = """
        <p style="text-align: center;"><em><strong><span style="
        12px; color: rgb(250, 197, 28);">Potencia pico de la instalaci&oacute;n: </span></strong></em></p>
        """
        st.markdown(html_temp, unsafe_allow_html = True)
    with mid:
        st.text("{} kW".format(potencia))

    
########################################### DATOS CONSUMIDOR #############################################################  


compens = 0
falta_comp = 0

st.text("\n")
st.text("\n")
html_temp = """
<p style="text-align: center;"><span style="font-size: 26px; font-family: Tahoma, Geneva, sans-serif;
rgba(255, 240, 36, 0) 3px 3px 2px; color: rgb(250, 197, 28);">Estimaci&oacute;n de compensaci&oacute;n por excedentes (&euro;) 💶</span></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)

html_temp = """
<p><font color="#efefef" face="Calibri, sans-serif"><span style="font-size: 10px;">Para poder proporcionarle una estimaci&oacute;n
de la compensaci&oacute;n econ&oacute;mica que podr&aacute; recibir ma&ntilde;ana por la energ&iacute;a que vierta a la red (aquella
de la producida por sus paneles solares que no consuma) se necesita estimar el perfil de consumo de su vivienda</span></font></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)

if st.checkbox('Deseo recibir una estimación de mi compensación por excedentes'):
    
    compens = 1
    falta_comp = 0
    
    #### Potencia contratada
    
    
    # Imagen 
    col1, mid, col2 = st.beta_columns([1,6,1])
    with col1:
        st.image(directorio + 'images/pot_c.png', width = 40)
    with mid:
        st.write('Seleccione la potencia contratada de su hogar')

    pot_c = 0
    message = st.text_area("Introduzca su potencia contratada")
    try:
        pot_c = float(str(message).replace(',', '.'))
    except:
        html_temp = """
        <p style="text-align: center;"><em><strong><span style="
        12px; color: rgb(250, 197, 28);">Introduzca valor de potencia v&aacute;lido. Ejemplo: 4.5 kW</span></strong></em></p>
        """
        st.markdown(html_temp, unsafe_allow_html = True)
        
    if pot_c == 0:
        pass
    else:
        col1, mid, col2 = st.beta_columns([4,3,1])
        with col1:
            html_temp = """
            <p style="text-align: center;"><em><strong><span style="
            12px; color: rgb(250, 197, 28);">Potencia contratada: </span></strong></em></p>
            """
            st.markdown(html_temp, unsafe_allow_html = True)
        with mid:
            st.text("{} kW".format(pot_c))

      
    
    #### Tipo de vivienda
    
    
    # Imagen 
    col1, mid, col2 = st.beta_columns([1,6,1])
    with col1:
        st.image(directorio + 'images/house.png', width = 70)
    with mid:
        st.write('Seleccione el tipo de vivienda en la que se encuentra la instalación fotovoltaica')
    
    hogar = ["Casa", "Piso"]
    make_choice = st.selectbox('Seleccione el tipo de vivienda en el que se encuentra la instalación fotovoltaica:', hogar)
    if make_choice == "Casa":
        casa = 1
        piso = 0
    elif make_choice == "Piso":
        casa = 0
        piso = 1
    
    
    #### Tipo de cohabitantes
    
    
    # Imagen 
    col1, mid, col2 = st.beta_columns([1,6,1])
    with col1:
        st.image(directorio + 'images/home.png', width = 40)
    with mid:
        st.write('Seleccione el tipo de comportamiento de los habitantes de su vivienda')
        
    html_temp = """
    <p><span style="font-family: Calibri, sans-serif;"><span style="color: rgb(239, 239, 239); font-size: 10px;">Para poder estimar el consumo de su vivienda,
    se va a realizar una predicci&oacute;n de este en base a los datos medios de la sociedad espa&ntilde;ola. para ello, es necesario conocer a qu&eacute;
    horas suele estar ocupada. Por ello, se requiere que indique el tipo de comportamiento t&iacute;pico que tiene el grupo de habitantes de la vivienda. 
    Por ejemplo, si suelen irse de casa muy pronto por la ma&ntilde;ana: Madrugadores. Si pasan las tardes en casa, porque trabajan/estudian
    por la ma&ntilde;ana: Ma&ntilde;anas fuera...</span></span></p>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
        
    tipo_1 = 0
    tipo_2 = 0
    tipo_3 = 0
    tipo_4 = 0
    tipo_5 = 0
    tipo_6 = 0
    tipo_cliente = ["Madrugadores", "Caseros", "Mañanas en casa", "Tardes en casa", "Fuera durante el día", "Horario inusual (trabajo nocturno)"]
    tipo_casa = st.selectbox('Seleccione el horario que más identifique a la gente que habita en la vivienda:', tipo_cliente)
    if tipo_casa == "Madrugadores":
        tipo_1 = 1
    elif tipo_casa == "Caseros":
        tipo_2 = 1
    elif tipo_casa == "Mañanas en casa":
        tipo_3 = 1
    elif tipo_casa == "Tardes en casa":
        tipo_4 = 1
    elif tipo_casa == "Fuera durante el día":
        tipo_5 = 1
    elif tipo_casa == "Horario inusual":
        tipo_6 = 1

# Se comprueba que se hayan introducido los datos
if compens == 1 and pot_c == 0:
    falta_comp = 1
        
########################################### FUNCIONES 1 #############################################################    
# De Funciones de Funciones_solares.py


# Excentricidad 

import math 

def excentricidad(dia):
    e_0 = 1 + 0.033 * math.cos((2*math.pi*dia)/365)
    return e_0


# Declinacion de la tierra

import math 

def gamma_declinacion(dia):
    gamma = 2.0 * math.pi *(dia-1)/365.0
    return gamma


import math 

def angulo_declinacion_solar(dia):
    gamma = gamma_declinacion(dia)
    delta = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) - 0.006758 * math.cos(2*gamma) + 0.000907 * math.sin(2* gamma) - 0.002697 * math.cos(3*gamma) + 0.001480 * math.sin(3*gamma)
    return delta #(radianes)


# Ángulo de salida del sol

import math 

def angulo_salida_sol(latitud, declinacion):
    w = math.acos( -math.tan(latitud) * math.tan(declinacion))
    return w


# Horas hasta el mediodia solar

import math 

def horas_mediodia(wsr):
    horas = wsr * 12/math.pi
    return horas

def segundos_(horas_mediodia):
    segundos = (horas_mediodia - math.trunc(horas_mediodia)) * 3600
    return segundos


def hora_inicial_(horas_mediodia):
    hora_inicial = 12 - math.trunc(horas_mediodia)
    return hora_inicial


def hora_final_(horas_mediodia):
    hora_final = 12 + math.trunc(horas_mediodia)
    return hora_final


# Ángulo solar horario

import math 

def angulo_solar_primera_ultima_hora(segundos, w_sr):
    w = w_sr - ((segundos/3600)/2 * math.pi/12)
    return w


def angulo_solar(hora):
    w = (hora - 12 - 0.5) * math.pi/12
    return w


# Altura solar horaria

import math 

def altura_solar(declinacion, latitud, angulo_solar_hora):
    altura = math.asin(math.sin(declinacion) * math.sin(latitud) + math.cos(declinacion) * math.cos(latitud) * math.cos(angulo_solar_hora))
    return altura


# Acimut solar horario

import math 

def acimut_solar(altura_solar, latitud, declinacion, angulo_horario):
    if(latitud > 0):
        acimut = math.acos((math.sin(altura_solar) * math.sin(latitud) - math.sin(declinacion))/(math.cos(altura_solar) * math.cos(latitud)))
    else:
        acimut = math.acos((math.sin(declinacion) * math.sin(latitud) - math.cos(declinacion) * math.sin(latitud) * math.cos(angulo_horario))/math.cos(declinacion))
    return acimut


# Radiación extraterrestre incidente

import math 

K_solar = 1367 #W/m^2

def radiacion_incidente_extraterrestre(excentricidad, altura_solar_hora):
    r_incidente = K_solar * excentricidad * math.sin(altura_solar_hora)
    return r_incidente


def radiacion_incidente_extraterrestre_primera_ultima_hora(excentricidad, altura_solar_hora, segundos):
    radiacion = radiacion_incidente_extraterrestre(excentricidad, altura_solar_hora)
    radiacion = radiacion * segundos / 3600
    return radiacion


# Obtener dataframe de medidas horarias para una inclinación, latitud, longitud, altura y acimut (orientación)

import math 
import pandas as pd
import itertools



def df_energia_solar(lat, lon, orientacion = 0, inclinacion = 0):
    lat = lat * math.pi/180
    lon = lon * math.pi/180
    inclinacion = inclinacion * math.pi/180
    orientacion = orientacion * math.pi/180
  
    mes = [1]*31 + [2]*28 + [3]*31 + [4]*30 + [5]*31 + [6]*30 + [7]*31 + [8]*31 + [9]*30 + [10]*31 + [11]*30 + [12]*31
    dia = list(range(1,32)) + list(range(1,29)) + list(range(1,32)) + list(range(1,31)) + list(range(1,32)) + list(range(1,31)) + list(range(1,32)) + list(range(1,32)) + list(range(1,31)) + list(range(1,32)) + list(range(1,31)) + list(range(1,32))
    dia_juliano = list(range(1,366))
  
    df = pd.DataFrame({'mes' : mes,
                       'dia' : dia,
                       'dia_juliano' : dia_juliano})
    df.insert(3, "declinacion_solar", list(map(angulo_declinacion_solar, dia_juliano)), True) 
    df.insert(4, "excentricidad_diaria", list(map(excentricidad, dia_juliano)), True) 
    df.insert(5, "w_sr", list(map(angulo_salida_sol, df["declinacion_solar"], itertools.repeat(lat, len(df["declinacion_solar"])))), True) 
    df.insert(6, "horas_mediodia", list(map(horas_mediodia,df["w_sr"])), True) 
    df.insert(7, "duracion_dia", df["horas_mediodia"]*2, True) 
    df.insert(8, "hora_inicial", list(map(hora_inicial_, df["horas_mediodia"])), True) 
    df.insert(9, "hora_final", list(map(hora_final_, df["horas_mediodia"])), True) 
    df.insert(10, "segundos", list(map(segundos_, df["horas_mediodia"])), True) 
    
    
    df_radiacion = pd.DataFrame(dia_juliano[0:365])
    df_radiacion.columns = ['dia_juliano']
    df_altura = pd.DataFrame(dia_juliano[0:365])
    df_altura.columns = ['dia_juliano']
    df_acimut = pd.DataFrame(dia_juliano[0:365])
    df_acimut.columns = ['dia_juliano']
    df_angulo_solar = pd.DataFrame(dia_juliano[0:365])
    df_angulo_solar.columns = ['dia_juliano']
    
    # Para cada hora del día, se obtinene las diferenets variable solares en función del día del año
    for h in range(1,25):
        w = []
        altura = []
        acimut = []
        radiacion = []
    
        for d in range(0,365):
            hora_inicial = df["hora_inicial"][d]
            hora_final = df["hora_final"][d]
            segundos = df["segundos"][d]
            w_sr = df["w_sr"][d]
            delta = df["declinacion_solar"][d] 
            E = df["excentricidad_diaria"][d]          
                   
            
            if(h == (hora_inicial) or h == (hora_final+1)):
                w_d = angulo_solar_primera_ultima_hora(segundos, w_sr)
                altura_d = altura_solar(delta, lat, w_d)
                acimut_d = acimut_solar(altura_d, lat, delta, w_d)       
                if(h == (hora_inicial)):
                    acimut_d = -acimut_d
                    w_d = -w_d              
                rad_d = radiacion_incidente_extraterrestre_primera_ultima_hora(E, altura_d, segundos)
                
            elif(h >= (hora_inicial+1) and h < (hora_final+1)):
                w_d = angulo_solar(h)
                altura_d = altura_solar(delta, lat, w_d)
                acimut_d = acimut_solar(altura_d, lat, delta, w_d)
                if(h < 13):
                    acimut_d = -acimut_d
                rad_d = radiacion_incidente_extraterrestre(E, altura_d)
                
            else:
                w_d = 0
                altura_d = 0
                acimut_d = 0
                rad_d = 0
        

            w.append(w_d)
            altura.append(altura_d)
            acimut.append(acimut_d)
            radiacion.append(rad_d)
            
        # angulo solar
        df_angulo_solar.insert(len(df_angulo_solar.columns), str("W_{}_{}".format(h-1, h)), w)
        
        # altura solar
        df_altura.insert(len(df_altura.columns), str("Altura_{}_{}".format(h-1, h)), altura)

        # acimut solar
        df_acimut.insert(len(df_acimut.columns), str("Acimut_{}_{}".format(h-1, h)), acimut)

        # Radiacion extraterrestre
        df_radiacion.insert(len(df_radiacion.columns), str("Gh0_{}_{}".format(h-1, h)), radiacion)

    df = df.merge(df_angulo_solar, left_on = "dia_juliano", right_on = "dia_juliano")
    df = df.merge(df_altura, left_on="dia_juliano", right_on="dia_juliano")
    df = df.merge(df_acimut, left_on="dia_juliano", right_on="dia_juliano")
    df = df.merge(df_radiacion, left_on="dia_juliano", right_on="dia_juliano")

    
    return df


# Radiación global

def radiacion_global(r_directa, r_difusa, r_reflejada):
    r_global = r_directa + r_difusa + r_reflejada
    return r_global


# Índice de transparencia atmosférico

def indice_transparencia(r_global, r_extraterrestre):
    i_transparencia = r_global/r_extraterrestre
    return i_transparencia


# Radiación difusa

import math 

def radiacion_difusa_horizontal(indice_transparencia, r_global):
    if(indice_transparencia >= 0 and indice_transparencia <= 0.22):
        r_difusa = r_global *(1 - 0.09 * indice_transparencia)
    elif(0.22 < indice_transparencia and indice_transparencia <= 0.8):
        r_difusa = r_global * (0.9511 - 0.16 * indice_transparencia + 4.388 * indice_transparencia**2 - 16.638 * indice_transparencia**3 + 12.336 * indice_transparencia**4)
    else:
        r_difusa = r_global * 0.165
    
    return r_difusa

def radiacion_difusa_inclinada(r_difusa, beta):
    if(beta != 0):
        r_difusa_beta = (1 + math.cos(beta))/2 * r_difusa
        
    return r_difusa_beta


# Radiación reflejada

import math 

def radiacion_reflejada(radiacion_global, albedo = 0.2, beta = 0):
    radiacion_reflejada = radiacion_global * albedo * (1- math.cos(beta))/2
    
    return radiacion_reflejada


# Radiación directa

import math 

def wsrm_(orientacion, beta, latitud, declinacion, angulo_salida_solar):
    
    if(orientacion < 0):
        signo = -1
    else:
        signo = 1
    
    A = math.sin(latitud)/math.tan(orientacion) + math.cos(latitud)/(math.sin(orientacion) * math.tan(beta))
    B = -math.tan(declinacion)*(math.sin(latitud)/(math.sin(orientacion)*math.tan(beta)) - math.cos(latitud)/math.tan(orientacion))
  
    wsrm = math.acos((A*B + signo*math.sqrt(A*A-B*B+1))/(A*A+1))
    wsrm = - min(wsrm,angulo_salida_solar) 
  
    return wsrm


def wsrt_(orientacion, beta, latitud, declinacion, angulo_salida_solar):
    
    if (orientacion < 0):
        signo = -1
    else:
        signo <- 1
  
    A = math.sin(latitud)/math.tan(orientacion) + math.cos(latitud)/(math.sin(orientacion) * math.tan(beta))
    B = -math.tan(declinacion)*(math.sin(latitud)/(math.sin(orientacion)*math.tan(beta)) - math.cos(latitud)/math.tan(orientacion))
  
    wsrt = math.acos((A*B - signo*math.sqrt(A*A-B*B+1))/(A*A+1))
    wsrt = min(wsrt, angulo_salida_solar)
    
    return wsrt



def radiacion_directa(r_global, r_difusa, acimut_solar_h, altura_solar_h, declinacion, latitud, angulo_solar_h, angulo_salida_solar, beta = 0, orientacion = 0):
    
    r_directa = r_global - r_difusa
  
    if (beta != 0):
        
        if(orientacion <0 and acimut_solar_h > 0):
            wsrt = wsrt_(orientacion, beta, latitud, declinacion, angulo_salida_solar)
            if(angulo_solar_h > wsrt):
                angulo_solar_h = wsrt

        if(orientacion >0 and acimut_solar_h <0):
            wsrm = wsrm_(orientacion, beta, latitud, declinacion, angulo_salida_solar) 
            if(angulo_solar_h < wsrm):
                angulo_solar_h = wsrm

        costhita = math.sin(declinacion) * math.sin(latitud) * math.cos(beta) - math.sin(declinacion) * math.cos(latitud) * math.sin(beta) * math.cos(orientacion) + math.cos(declinacion) * math.cos(latitud) * math.cos(beta) * math.cos(angulo_solar_h) + math.cos(declinacion) * math.sin(latitud) * math.sin(beta) * math.cos(orientacion) * math.cos(angulo_solar_h) + math.cos(declinacion) * math.sin(beta) * math.sin(orientacion) * math.sin(angulo_solar_h)

        if(costhita < 0):
            costhita = 0

        costhitaz = math.sin(declinacion) * math.sin(latitud) + math.cos(declinacion) * math.cos(latitud) * math.cos(angulo_solar_h)

        
        if(costhitaz > 0):
            rb = costhita/costhitaz
        else:
            rb = 1

        r_directa = r_directa * rb


    return r_directa


# Obtención de la potencia generada por los paneles fotovoltaicos

import math 
import numpy as np

def temperatura_instalacion(temperatura_ambiente, irradiacion_solar, velocidad_viento, m = -3.56, n = -0.079):
    temperatura = []
    for i in range(0, len(temperatura_ambiente)):
        temperatura.append(temperatura_ambiente[i] + irradiacion_solar[i] * math.exp(m + n * velocidad_viento[i]))
    return temperatura


def potencia_generada(t_ambiente, irr_solar, v_viento, ppico):
    
    g_ref = 1000 #W/m^2
    coef_y = -0.0048
    t_ref = 25
    P_ref = 1000 * ppico
  
    coefCC = 0.97 * 0.98 * 0.98 * 0.98
    efinversor = 0.95
    perdCA = 0.99
    T_m = temperatura_instalacion(t_ambiente, irr_solar, v_viento)
  
    potencia = P_ref * np.array(irr_solar)/g_ref * (1 + coef_y * (np.array(T_m) - t_ref))
    potencia = potencia * coefCC * efinversor * perdCA
  
    return potencia


# Función auxiliar para calcular la radiación global horaria necesaria para obtener la producción fotovoltaica horaria

def calculo_radiacion_horaria(r_global, K, acimut_sol, altura_sol, angulo_sol, decl, latitud, inclinacion, orientacion, angulo_salida_solar):
    
    r_difusa_horiz = []
    r_difusa_incl = []
    r_directa_h = []
    r_reflejada_h = []
    r_global_h = []
    
    for h in range(0,len(r_global)):
        k = K[h]
        rg = r_global[h]
        acimut_h = acimut_sol[h]
        altura_h = altura_sol[h]
        angulo_h = angulo_sol[h]
        declinacion = decl

        r_difusa  = radiacion_difusa_horizontal(k, rg)
        r_difusa_horiz.append(r_difusa)
    
        r_directa = radiacion_directa(r_global = rg, 
                                       r_difusa = r_difusa, 
                                       beta = inclinacion, 
                                       orientacion = orientacion, 
                                       acimut_solar_h = acimut_h, 
                                       altura_solar_h = altura_h, 
                                       declinacion = declinacion, 
                                       latitud = latitud, 
                                       angulo_solar_h = angulo_h,
                                       angulo_salida_solar = angulo_salida_solar)
        r_directa_h.append(r_directa)
    
        r_difusa_beta = radiacion_difusa_inclinada(r_difusa = r_difusa, beta = inclinacion)
        r_difusa_incl.append(r_difusa_beta)

        r_reflejada = radiacion_reflejada(radiacion_global = rg, beta = inclinacion)
        r_reflejada_h.append(r_reflejada)

        r_global_plano = radiacion_global(r_directa = r_directa, r_difusa = r_difusa_beta, r_reflejada = r_reflejada)
        r_global_h.append(r_global_plano)

    df_radiaciones = pd.DataFrame({'r_difusa_incl':r_difusa_incl, 'r_reflejada_h':r_reflejada_h, 'r_directa_h':r_directa_h, 'r_global_h':r_global_h})
    return df_radiaciones


# Función que calcula la distancia euclidea o de Manhattan entre dos puntos

import math 

def distancia(lat1, lon1, lat2, lon2, distancia = "euclidea"):
    
    if(distancia == "euclidea"):
        dist = math.sqrt((lat1 - lat2)**2 + (lon1 -lon2)**2)
    
    elif(distancia == "manhattan"):
        dist = abs(lat1 - lat2) + abs(lon1 -lon2)
  
    return dist 


# Saber si un día tiene horario invierno o verano en España

from datetime import date, datetime

def verano_invierno(now):
    
    Y = 2000 #año bisiesto genérico
    inv_ver = [(1, (date(Y,  1,  1),  date(Y,  3, 26))),
               (2, (date(Y,  3, 27),  date(Y,  10, 30))),
               (1, (date(Y, 10, 31),  date(Y, 12, 31)))]
    # 1 Invierno, 2 Verano
    
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in inv_ver
                if start <= now <= end)


# Función de cálculo

from datetime import timezone, datetime, date, timedelta
import math

def calcularEnergia(lat, lon, orient, incl, ppico, fecha, dia_Gh, ta):
       
    fecha = str(fecha)
    
    # Dia y mes actual
  
    actualDay = datetime.strptime(fecha, '%Y-%m-%d').day
    actualMonth = datetime.strptime(fecha, '%Y-%m-%d').month
 
    
    # Se calcula el dataframe con la informacion de radiacion (excentricidad, wsr...) para la lat, lon, orient e inclinacion que se esta procesando
    
    df_solar_energy = df_energia_solar(lat, lon, orient, incl) 
    
    # Nos quedamos con los datos de radiacion para el dia
    
    calculos_dia = df_solar_energy[df_solar_energy["mes"] == actualMonth]
    calculos_dia = calculos_dia[calculos_dia["dia"] == actualDay]
   
    acimut_h_dia = []
    altura_h_dia = []
    angulo_h_dia = []
    gh0_h_dia = []
    
    
    for i in range(4, 20):
        acimut_h_dia.append("Acimut_" + str(i) + "_" + str(i+1))
    for i in range(4, 20):
        altura_h_dia.append("Altura_" + str(i) + "_" + str(i+1))
    for i in range(4, 20):
        angulo_h_dia.append("W_" + str(i) + "_" + str(i+1))
    for i in range(4, 20):
        gh0_h_dia.append("Gh0_" + str(i) + "_" + str(i+1))
    
    
    dia_Acimut_h = calculos_dia[acimut_h_dia]     #Valores horarios de acimut para el dia
    dia_Altura_h = calculos_dia[altura_h_dia]     #Valores horarios de altura solar para el dia
    dia_Angulo_h = calculos_dia[angulo_h_dia]     #Valores horarios de angulo solar para el dia
    dia_declinacion = calculos_dia["declinacion_solar"]   #Valores horarios de declinacion para el dia
    dia_Gh0 = calculos_dia[gh0_h_dia]   #Valores horarios de Gh0 (Radiacion extraterrestre) para el dia
  
    dia_Kh  = indice_transparencia(r_global = dia_Gh, r_extraterrestre = dia_Gh0)  #Valores horarios de indice de transparencia para el dia
    dia_Kh_lista = list(pd.DataFrame(dia_Kh).reset_index(drop=True).iloc[0].isnull())
    for i in range(0, len(dia_Kh_lista)):
        if (dia_Kh_lista[i] == True):
            dia_Kh[dia_Kh.columns[i]] = 0
    
    
    inclinacion = incl * math.pi/180
    orientacion = orient * math.pi/180
    lat = lat * math.pi/180
    angulo_salida_solar = angulo_salida_sol(lat, dia_declinacion)
    
    
    # Obtener dataframe de radiacion para el dia actual 
  
    df_radiacion_horaria = calculo_radiacion_horaria(dia_Gh,
                                                    list(dia_Kh.iloc[0]), 
                                                    list(dia_Acimut_h.iloc[0]), 
                                                    list(dia_Altura_h.iloc[0]), 
                                                    list(dia_Angulo_h.iloc[0]),
                                                    dia_declinacion,
                                                    lat,
                                                    inclinacion,
                                                    orientacion,
                                                    angulo_salida_solar)
     
    # Temperatura ambiente y velocidad de viento
    
    temperatura_ambiente = ta
    
    vel_viento = []
    for i in range (0, len(temperatura_ambiente)):
        vel_viento.append(3.5)
    
    # Se calcula la energia
    
    potencia_dia_h = potencia_generada(temperatura_ambiente, list(df_radiacion_horaria["r_global_h"]), vel_viento, ppico)
        
        
    # Saber cuantas horas adelantar los datos para pasarlos a hora local
    
    horas_atrasar = verano_invierno(datetime.strptime(fecha, '%Y-%m-%d').date())
    
    if (horas_atrasar == 1):
        potencia_dia_h = [0,0,0,0,0] + list(potencia_dia_h) + [0,0,0]
    else:
        potencia_dia_h = [0,0,0,0,0,0] + list(potencia_dia_h) + [0,0]
        
        
    return potencia_dia_h


########################################### EJECUCIÓN #############################################################
# De Script_funcional.ipynb

import numpy as np
import pandas as pd
import random
pd.options.display.max_columns = None
pd.options.display.max_rows = None
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import math
import time
from datetime import timezone, datetime, date, timedelta
import os
import requests
import json
import re
import io
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle as pk
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
import time
import urllib


hora_ini = 4
hora_fin = 20

directorio = '/home/dsc/git/TFM/'
df_estaciones = pd.read_csv(directorio + 'data/estaciones.csv')
df_estaciones_rad = pd.read_csv(directorio + 'data/estaciones_rad.csv')
df_estaciones_rad.dropna(inplace = True)
df_estaciones_rad.reset_index(drop = True, inplace = True)

def get_response_aemet(url_base = "", url = "", api_key = "", ide = ""):
    
    # Se unen las partes de la url final
    call = '/'.join([url_base, url, ide])
    if(ide == ""):
        call = call[:-1]

    headers = {    
        'Accept': 'application/json',  
        'Authorization': 'api_key' + api_key
    }
    response = requests.get(call, headers = headers)
    
    #Se obtienen los datos del body
    body = json.loads(response.text)["datos"]
    
    
    response = requests.get(body, headers = headers)
    if response:
        print('Exito')
    else:
        print('Ha ocurrido un error')

    return response.text

def get_response_OW(url = ""):
    
    response = requests.get(url)

    if response:
        print('Exito')
    else:
        print('Ha ocurrido un error')

    return response.content


def openAndSkipLines(f, symbol):

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

def getCamsData(camsFile, nbLinesToSkip):

    # Lista de variables CAMS:
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
    
    # Almaceno los datos de cada fila
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

    # Genero el data frame
    dictio = {"dateBegins":dateBegins, "dateEnds":dateEnds, "toa":toa, "cs_ghi":cs_ghi, "cs_bhi":cs_bhi, "cs_dhi":cs_dhi, "cs_bni":cs_bni, "ghi":ghi, "bhi":bhi, "dhi" : dhi, "bni" : bni, "reliability" : reliability}
    datacolumns = pd.DataFrame(dictio)

    return datacolumns

def distancia(lat1, lon1, lat2, lon2, distancia = "euclidea"):
    
    if(distancia == "euclidea"):
        dist = math.sqrt((lat1 - lat2)**2 + (lon1 -lon2)**2)
    
    elif(distancia == "manhattan"):
        dist = abs(lat1 - lat2) + abs(lon1 -lon2)
  
    return dist 

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

def dividir_train_test(x,y, prop = 0.8):
    
    # Proporción de train
    tam_train = prop

    # Divido en train y test
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = tam_train, random_state = 1)

    print('x_train: {}%. Nº de datos: {}'.format((len(x_train)/len(x))*100, len(x_train)))
    print('y_train: {}%. Nº de datos: {}'.format((len(y_train)/len(y))*100, len(y_train)))


    print('x_test: {}%. Nº de datos: {}'.format((len(x_test)/len(x))*100, len(x_test)))
    print('y_test: {}%. Nº de datos: {}'.format((len(y_test)/len(y))*100, len(y_test)))
    
    return x_train, x_test, y_train, y_test

def graf_compara(nombre_modelo, y_real, y_pred):
    
    # Valores predicción
    predic = pd.DataFrame({'Dato': y_pred})
    predic.insert(len(predic.columns),"index",[i for i in range(0,len(predic["Dato"]))],True)
    
    # Valores reales
    real = pd.DataFrame({'Dato': y_real})
    real.insert(len(real.columns),"index",[i for i in range(0,len(real["Dato"]))],True)
    
    # Comparación
    comparacion = pd.concat([real, predic], keys=["Real", "Prediccion"]).reset_index()
    comparacion.drop(['level_1'], axis=1, inplace = True)
    comparacion.columns = ['Tipo', 'Dato', "Index"]

    sns.catplot(data = comparacion, kind = "bar", x = "Index", y = "Dato", hue = "Tipo", estimator = np.median, height = 10, aspect = 5)


def metricas(modelo, y_real, y_pred):
    
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    # MAE: el error se calcula como un promedio de diferencias absolutas entre los valores objetivo y las predicciones. Todas las diferencias individuales se ponderan por igual en el promedio.
    mae = mean_absolute_error(y_real, y_pred)

    # MSE: mide el error cuadrado promedio de las predicciones. Para cada punto, calcula la diferencia cuadrada entre las predicciones y el objetivo y luego promedia esos valores.
    mse = mean_squared_error(y_real, y_pred, squared = False)
    
    # RMSE: es la raíz cuadrada de MSE. Tiene la escala de la variable objetivo.
    rmse = np.sqrt(mean_squared_error(y_real, y_pred))
    
    # R^2: está estrechamente relacionada con la MSE, pero tiene la ventaja de estar libre de escala. Está siempre entre -∞ y 1.
    r2 = r2_score(y_real, y_pred)
    
    
    
    print('MODEL: ', modelo)
    print('MAE: ', mae)
    print('MSE: ', mse)
    print('RMSE: ', rmse)
    print('R2 : ', r2)


    return modelo, mae, mse, rmse, r2

def compracion_metricas(lista_modelos):
    
    plt.style.use('ggplot')
    
    # Creamos dataframes para albergar las métricas
    df_mae = pd.DataFrame(columns = ['mae', "modelo"])
    df_mse = pd.DataFrame(columns = ['mse', "modelo"])
    df_rmse = pd.DataFrame(columns = ['rmse', "modelo"])
    df_r2 = pd.DataFrame(columns = ['r2', "modelo"])

    # Se llenan los dataframes con las métricas
    for modelo in lista_modelos:
        
        df_mae = df_mae.append({'mae': modelo[1], "modelo": modelo[0]}, ignore_index=True)
        df_mse = df_mse.append({'mse': modelo[2], "modelo": modelo[0]}, ignore_index=True)
        df_rmse = df_rmse.append({'rmse': modelo[3], "modelo": modelo[0]}, ignore_index=True)
        df_r2 = df_r2.append({'r2': modelo[4], "modelo": modelo[0]}, ignore_index=True)
        #df_mape = df_mape.append({'mape': modelo[5], "modelo": modelo[0]}, ignore_index=True)
    
    # Se crea la figura y añado los subplots de cada métrica
    fig = plt.figure(figsize = (15, len(lista_modelos*4)))
    ax1 = fig.add_subplot(5,1,1)
    ax2 = fig.add_subplot(5,1,2)
    ax3 = fig.add_subplot(5,1,3)
    ax4 = fig.add_subplot(5,1,4)
    
    #MAE
    fig = sns.barplot(x = "mae", y = "modelo", data = df_mae, ax = ax1, orient = "h", color = 'green').set_title("Comparación de métricas")
    ax1.tick_params(labelbottom = False, bottom = False)
    ax1.set_xlabel("MAE")
    ax1.set_ylabel(" ")
    for pa in ax1.patches:
        ax1.annotate("%.4f" % pa.get_width(), xy = (pa.get_width(), pa.get_y() + pa.get_height()/2),
            xytext = (5, 0), textcoords = 'offset points', ha = "left", va = "center")
    
    #MSE
    fig = sns.barplot(x = "mse", y = "modelo", data = df_mse, ax = ax2, orient = "h", color = 'red')
    ax2.tick_params(labelbottom = False, bottom = False)
    ax2.set_xlabel("MSE")
    ax2.set_ylabel(" ")
    for pa in ax2.patches:
        ax2.annotate("%.4f" % pa.get_width(), xy = (pa.get_width(), pa.get_y() + pa.get_height()/2),
            xytext = (5, 0), textcoords = 'offset points', ha = "left", va = "center")
        
    #RMSE
    fig = sns.barplot(x = "rmse", y = "modelo", data = df_rmse, ax = ax3, orient = "h", color = 'blue')
    ax3.tick_params(labelbottom = False, bottom = False)
    ax3.set_xlabel("RMSE")
    ax3.set_ylabel(" ")
    for pa in ax3.patches:
        ax3.annotate("%.4f" % pa.get_width(), xy = (pa.get_width(), pa.get_y() + pa.get_height()/2),
            xytext = (5, 0), textcoords = 'offset points', ha = "left", va = "center")

    #R2
    fig = sns.barplot(x = "r2", y = "modelo", data = df_r2, ax = ax4, orient = "h", color = 'yellow')
    ax4.set_xlabel("R2")
    ax4.set_ylabel(" ")
    ax4.tick_params(labelbottom = False, bottom = False)
    for pa in ax4.patches:
        ax4.annotate("%.4f" % pa.get_width(), xy = (pa.get_width(), pa.get_y() + pa.get_height()/2),
            xytext = (5, 0), textcoords = 'offset points', ha = "left", va = "center")

def api_ree(indicador, token):
    
    url = "https://api.esios.ree.es/indicators"
    hoy = fecha
    dia_ant = fecha_ayer
    dia_ant_ant = fecha_anteayer    
    try:
        url = "https://api.esios.ree.es/indicators/" + str(indicador) + "?start_date=" + dia_ant + "T22%3A00%3A00Z&end_date=" + hoy + "T23%3A59%3A59Z"

        headers = {
            'Accept': 'application/json; application/vnd.esios-api-v1+json',
            'Host': 'api.esios.ree.es',
            'Content-Type': 'application/json',
            'Authorization': 'Token token="{}"'.format(token)
        }

        response = requests.request("GET", url, headers = headers)
        
    except:
        url = "https://api.esios.ree.es/indicators/" + str(indicador) + "?start_date=" + dia_ant_ant + "T22%3A00%3A00Z&end_date=" + dia_ant + "T23%3A59%3A59Z"

        headers = {
            'Accept': 'application/json; application/vnd.esios-api-v1+json',
            'Host': 'api.esios.ree.es',
            'Content-Type': 'application/json',
            'Authorization': 'Token token="{}"'.format(token)
        }

        response = requests.request("GET", url, headers = headers)

    precios = response.json()
    precios = precios['indicator']['values']
    precios_datos = pd.DataFrame(precios)
    precios_datos['datetime'] = pd.to_datetime(precios_datos['datetime'])
    precios_datos['dia'] = precios_datos['datetime'].dt.strftime('%m/%d/%Y')

    return precios_datos

def descarga(df, nombre):
    
    csv = df.to_csv(index = False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()
    
    if nombre == "prediccion":
        return f'<a href="data:file/csv;base64,{b64}" download="prediccion.csv">Download csv file</a>'
    if nombre == "compensacion":
        return f'<a href="data:file/csv;base64,{b64}" download="compensacion.csv">Download csv file</a>'

########################################### Se define la fecha

fecha_a_usar = date.today()
fecha = fecha_a_usar
fecha = "{}-{}-{}".format(fecha.year, str(fecha.month).zfill(2), str(fecha.day).zfill(2))

fecha_ant = date.today() + timedelta(days = -1)
fecha_ayer = "{}-{}-{}".format(fecha_ant.year, str(fecha_ant.month).zfill(2), str(fecha_ant.day).zfill(2))

fecha_ant_ant = date.today() + timedelta(days = -2)
fecha_anteayer = "{}-{}-{}".format(fecha_ant_ant.year, str(fecha_ant_ant.month).zfill(2), str(fecha_ant_ant.day).zfill(2))


########################################### Si se guardan coordenadas:


st.text("\n")
html_temp = """
<p style="text-align: center;"><span style="font-size: 26px; font-family: Tahoma, Geneva, sans-serif;
rgba(255, 240, 36, 0) 3px 3px 2px; color: rgb(250, 197, 28);">Predicci&oacute;n de la producci&oacute;n el&eacute;ctrica ☀️</span></p>
"""
st.markdown(html_temp, unsafe_allow_html = True)

coord_guardadas = 0
if st.button("Guardar coordenadas y características"):
    
    ppico = potencia
    
    
    if hay_coord == 0:
        html_temp = """
        <p style="text-align: center;"><span style="font-size: 19px;
        font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);">Por favor, seleccione una ubicaci&oacute;n ‼️‼️</span></p>
        """
        st.markdown(html_temp, unsafe_allow_html = True)
    else:
        
        lat = hay_coord["lat"]
        lon = hay_coord["lng"]


        fuera_spain = 0
        # se comprueba que las coordenadas sean aproximadamente de España
        if (lat > 43.866218) or (lat < 27.44979) or (lat < 35.119909 and lat > 29.343875):
            fuera_spain = 1
        if (lat < 29.343875 and lat > 27.44979):
            if (lon > -13.117676 or lon < -16.787109):
                fuera_spain = 1
        if (lon > 4.394531) or (lat < -18.457031):
            fuera_spain = 1
        if (lat < 41.738528 and lat > 35.119909):
            if (lon < -7.756348):
                fuera_spain = 1
        if (lat > 35.119909):
            if (lon < -9.689941):
                fuera_spain = 1
        
        if fuera_spain == 1:
            html_temp = """
            <p style="text-align: center;"><span style="font-size: 19px;
            font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);">Por favor, seleccione una ubicaci&oacute;n v&aacute;lida (en España) ‼️‼️</span></p>
            """
            st.markdown(html_temp, unsafe_allow_html = True)
        
    if potencia == 0:
        html_temp = """
        <p style="text-align: center;"><span style="font-size: 19px;
        font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);">Por favor, introduzca una potencia pico v&aacute;lida ‼️‼️</span></p>
        """
        st.markdown(html_temp, unsafe_allow_html = True)
        
    if falta_comp == 1:
        html_temp = """
        <p style="text-align: center;"><span style="font-size: 19px;
        font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);">Por favor, introduzca una potencia contratada v&aacute;lida ‼️‼️</span></p>
        """
        st.markdown(html_temp, unsafe_allow_html = True)
        
    if hay_coord != 0 and potencia != 0 and falta_comp == 0 and fuera_spain == 0:
        coord_guardadas = 1
        st.success("Coordenadas guardadas")
        lat = hay_coord["lat"]
        lon = hay_coord["lng"]        
        
        col1, mid, col2 = st.beta_columns([4,4,1])
        with col1:
            html_temp = """
            <p style="text-align: center;"><em><strong><span style="font-size:
            20px; color: rgb(250, 197, 28);">Sus coordenadas son: </span></strong></em></p>
            """
            st.markdown(html_temp, unsafe_allow_html = True)
        with mid:
            st.text("{},{}".format(lat, lon))
    

        ya = 0
        while ya == 0:
            if coord_guardadas == 1:
                st.text("Este proceso puede tardar unos minutos, por favor, espere")
                ya = 1

        ########################################### Se obtienen los datos de clima
        try:

            # Contraseña API
            api_key = "f21448c171f8f0584b48b3c51c9b6cd6"
            df_clima_ow_total = pd.DataFrame()

            # Para cada día histórico (5 días anteriores)
            for retardo in range(0,5):


                dia = date.today() + timedelta(days = -retardo)
                dia = "{}-{}-{}".format(dia.year, str(dia.month).zfill(2), str(dia.day).zfill(2))

                dia = datetime.strptime(dia, "%Y-%m-%d")

                # Convierto datetime a timestamp
                dia_unix = int(datetime.timestamp(dia))


                time = dia_unix

                url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}".format(lat, lon, time, api_key)

                response = get_response_OW(url)


                # Obtengo datos de la respuesta
                response = json.loads(response)
                df_clima_ow = pd.json_normalize(response["hourly"])

                # Genero columnas extra

                # Indicador de clima
                df_we = []
                # Fecha del día de los datos
                df_time = []
                # Hora
                df_hour = []
                # ID de estacion
                df_estacion = []
                # Fecha de obtención de datos
                df_fecha = []
                for m in range(0,24):
                    df_we.append(df_clima_ow["weather"][m][0]["id"])
                    df_estacion.append(str(str(lat)+str(lon)))
                    df_time.append(datetime.utcfromtimestamp(int(df_clima_ow["dt"][m])).strftime('%Y-%m-%d'))
                    df_hour.append(datetime.utcfromtimestamp(int(df_clima_ow["dt"][m])).strftime('%H:%M')) 
                    df_fecha.append(fecha)

                df_we = pd.DataFrame(df_we, columns=['we']) 
                df_estacion = pd.DataFrame(df_estacion, columns=['estacion'])
                df_time = pd.DataFrame(df_time, columns=['date']) 
                df_hour = pd.DataFrame(df_hour, columns=['hour']) 
                df_fecha = pd.DataFrame(df_fecha, columns=['fecha prediccion']) 

                # Añado la columna con el indicador de clima
                df_clima_ow = pd.concat([df_clima_ow, df_we], axis=1)
                # Elimino la fila de weather, con más indicadores
                df_clima_ow = df_clima_ow.drop("weather", axis = 1)

                # Añado la columna con el ID de estacion
                df_clima_ow = pd.concat([df_estacion, df_clima_ow], axis=1)

                # Añado la columna con la fecha del día que obtengo los datos y del día y hora al que corresponde cada uno
                # Elimino la dt de la que las obtuve
                df_time = pd.concat([df_time, df_hour, df_fecha], axis=1)
                df_clima_ow = pd.concat([df_time, df_clima_ow], axis=1)
                df_clima_ow = df_clima_ow.drop("dt", axis = 1)

                df_clima_ow_total = df_clima_ow_total.append(df_clima_ow, ignore_index = True)

            df_clima_ow = df_clima_ow_total
            
        except:
            pass

        ########################################### Se obtienen los datos de predicción de clima
        try:

            api_key= "f21448c171f8f0584b48b3c51c9b6cd6"

            exclude = "current,minutely,daily,alerts"

            url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(lat, lon, exclude, api_key)


            response = get_response_OW(url)
            response = json.loads(response)
            df_pred_ow = pd.json_normalize(response["hourly"])


            # Genero columnas extra

            # Indicador de clima
            df_we = []
            # Fecha del día de los datos
            df_time = []
            # Hora
            df_hour = []
            # ID de estacion
            df_estacion = []
            # Fecha de obtención de datos
            df_fecha = []
            for m in range(0,48):
                df_we.append(df_pred_ow["weather"][m][0]["id"])
                df_estacion.append(str(str(lat)+str(lon)))
                df_time.append(datetime.utcfromtimestamp(int(df_pred_ow["dt"][m])).strftime('%Y-%m-%d'))
                df_hour.append(datetime.utcfromtimestamp(int(df_pred_ow["dt"][m])).strftime('%H:%M'))
                df_fecha.append(fecha)
            df_we = pd.DataFrame(df_we, columns=['we'])  
            df_estacion = pd.DataFrame(df_estacion, columns=['estacion'])
            df_time = pd.DataFrame(df_time, columns=['date']) 
            df_hour = pd.DataFrame(df_hour, columns=['hour'])
            df_fecha = pd.DataFrame(df_fecha, columns=['fecha prediccion']) 

            # Añado el indicador de clima y elimino la columna weather, con más valores
            df_pred_ow = pd.concat([df_pred_ow, df_we], axis = 1)
            df_pred_ow = df_pred_ow.drop("weather", axis = 1)

            # Añado el ID de estación
            df_pred_ow = pd.concat([df_estacion, df_pred_ow], axis=1)

            # Añado la fecha del día de la petición de los datos y el día y hora al que correpsonden
            # Elimino la columna dt, del que obtengo los valores
            df_time = pd.concat([df_time, df_hour, df_fecha], axis=1)
            df_pred_ow = pd.concat([df_time, df_pred_ow], axis=1)
            df_pred_ow = df_pred_ow.drop("dt", axis = 1)


        except:
            pass

        ########################################### Se obtienen los datos de radiación del día anterior (AEMET)
        try:
            import csv

            api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbGVqYW5kcm8ucnVpei5iZXJjaWFub0BnbWFpbC5jb20iLCJqdGkiOiI2NDNmZjZmMi04OTQyLTQ1YzYtODIxNC0yZGU4NmQzMDU0NWYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYxMzQ3NjEwNywidXNlcklkIjoiNjQzZmY2ZjItODk0Mi00NWM2LTgyMTQtMmRlODZkMzA1NDVmIiwicm9sZSI6IiJ9.CCEfI4NjKp9kiTCFsNLQFB-u_oLhcXJTEtdHluoToe8"

            url_base = "https://opendata.aemet.es/opendata/api"

            estaciones_url = "red/especial/radiacion"

            resp = get_response_aemet(url_base, estaciones_url, api_key)

            # Se procesan los datos
            datos_rad = resp[32:]

            lines = datos_rad.splitlines()
            fecha_lines = (resp.splitlines()[1])
            fecha_lines = fecha_lines[1:len(fecha_lines)-1]

            reader = csv.reader(lines)
            parsed_csv = list(reader)

            titulos = [palabra.strip() for palabra in parsed_csv[0][0].replace(';', ', ').replace("\"", "").split(",")]
            filas = [[palabra.strip() for palabra in fila[0].replace(';', ', ').replace("\"", "").split(",")] for fila in parsed_csv[1:]]


            # Las estaciones 9 y 16 tienen el titulo partido, hay que unir los strings
            filas[15][0] = filas[15][0] + filas[15][1]
            filas[15].pop(1)


            # Se corrige un indicativo
            df_rad_aemet = pd.DataFrame(columns = titulos, data = filas)
            df_rad_aemet.loc[df_rad_aemet['Indicativo'] == '6156', 'Indicativo'] = '6156X'

            # Se añade la columna con la fecha a la que corresponden los datos
            # Además se asegura que los nombres de las estaciones que se encuentran también en la lista de estaciones sean los mismos
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

        except:
            pass

        ########################################### Se obtienen los datos de radiación (SODA)
        try:
            import math
            import time
            from bs4 import BeautifulSoup

            dia = date.today() + timedelta(days = -2)
            fecha_buscar = "{}-{}-{}".format(dia.year, str(dia.month).zfill(2), str(dia.day).zfill(2))
            print(fecha_buscar)
            fecha_ini = fecha_buscar
            fecha_fin = fecha_buscar    

            print(lat, lon)

            correo = 'alejandro.ruiz.berciano%2540gmail.com'

            url = 'http://www.soda-is.com/service/wps?Service=WPS&Request=Execute&Identifier=get_cams_radiation&version=1.0.0&DataInputs=latitude={};longitude={};altitude=-999;date_begin={};date_end={};time_ref=UT;summarization=PT01H;username={}&RawDataOutput=irradiation'.format(lat, lon, fecha_ini, fecha_fin, correo)
            print(url)

            response = requests.get(url)

            # Se convierte la respuesta en texto y se determina cuántas líneas hay hasta los datos
            soup = BeautifulSoup(response.content)

            f = soup.text
            nbTotalLines = 0
            nbLinesToSkip = 0
            nbTotalLines, nbLinesToSkip = openAndSkipLines(f, '#')

            if(nbTotalLines < 0):
                print('No hay datos')
                exit()
            sizeData = nbTotalLines - nbLinesToSkip

            # Se crea el data frame y se añade una columna con el ID de la estación
            df_soda = getCamsData(f, nbLinesToSkip)
            df_soda.insert(len(df_soda.columns),"estacion",list(np.repeat([str(str(lat)+str(lon))], len(df_soda["dateEnds"]))),True)

        except:
            pass

        ########################################### Se limpian los datos de clima
        def clima_ow_clean(df_datos):

            # Convierto las columnas a los tipos de dato correctos

            df_datos["hour"] = pd.to_numeric([np.nan if pd.isna(c) == True else str(c)[:2] for c in df_datos["hour"]])
            df_datos = df_datos[(df_datos["hour"] < hora_fin) & (df_datos["hour"] >= hora_ini)]
            df_datos.reset_index(drop=True, inplace=True)

            # Elimino Na's

            try:
                df_datos.fillna({'visibility': df_datos["visibility"].mean(), 'wind_gust': df_datos["wind_gust"].mean()}, inplace = True)
            except:
                df_datos.fillna({'visibility': 0, 'wind_gust': 0}, inplace = True)

            try:
                df_datos.drop(['rain.1h'], axis=1, inplace = True)
            except:
                pass

            try:
                df_datos.drop(['snow.1h'], axis=1, inplace = True)
            except:
                pass

            df_datos = df_datos.fillna(0)

            # Se eliminan filas reptidas

            df_datos = df_datos.drop_duplicates(['date', 'hour', "fecha prediccion", "estacion"],
                                keep = 'first')
            df_datos.reset_index(drop = True, inplace = True)

            return df_datos

        df_clima_clean = clima_ow_clean(df_clima_ow)
        

        ########################################### Se limpian los datos de predicción de clima
        def pred_clean(df_datos):

            # Convierto las columnas a los tipos de dato correctos

            df_datos["hour"] = pd.to_numeric([np.nan if pd.isna(c) == True else str(c)[:2] for c in df_datos["hour"]])
            df_datos = df_datos[(df_datos["hour"] < hora_fin) & (df_datos["hour"] >= hora_ini)]
            df_datos.reset_index(drop=True, inplace=True)

            # Elimino Na's

            try:
                df_datos.drop(['rain.1h'], axis=1, inplace = True)
            except:
                pass
            try:
                df_datos.drop(['snow.1h'], axis=1, inplace = True)
            except:
                pass

            df_datos = df_datos.fillna(0)

            # Se elimina posibles filas repetidas

            df_datos = df_datos.drop_duplicates(['date', 'hour', "fecha prediccion", "estacion"],
                                keep = 'first')
            df_datos.reset_index(drop = True, inplace = True)

            return df_datos

        df_pred_clean = pred_clean(df_pred_ow)


        ########################################### Se limpian los datos de radiación del día anterior (AEMET)
        def rad_aemet_clean(df_datos):

            # Cambio los nombres de columna como corresponde
            columnas = []
            for i in df_rad_aemet.columns:

                if (i+".3") in columnas:
                    columnas.append(i+".4")
                elif (i+".2") in columnas:
                    columnas.append(i+".3")
                elif (i+".1") in columnas:
                    columnas.append(i+".2")
                elif i in columnas:
                    columnas.append(i+".1")
                elif i not in columnas:
                    columnas.append(i) 
            df_datos.columns = columnas


            # Se genera el dataset por hora

            hora_ini_aemet = 5
            hora_fin_aemet = 21
            dif = int(int(hora_fin_aemet)-int(hora_ini_aemet))
            df_rad_horas = pd.DataFrame(columns = ["fecha", "hora", "estacion", "indicativo", "GL", "DF", "DT", "UVB", "IR"])

            for i, fila in df_datos.iterrows():

                for j in range(0, dif):
                    hora = 5+j
                    col_gl = str(hora)
                    col_df = str(hora) + ".1"
                    col_dt = str(hora) + ".2"
                    col_uvb = str(hora) + ".3"
                    col_uvb_2 = str(hora-1) + ".5"
                    col_ir = str(hora) + ".4"
                    df_rad_horas = df_rad_horas.append({'fecha' : fila["fecha"], 'estacion' : fila["Estación"], 'indicativo' : fila["Indicativo"], 'GL' : fila[col_gl], 'DF' : fila[col_df], 'DT' : fila[col_dt], 'UVB' : (fila[col_uvb] + fila[col_uvb_2]), 'IR' : fila[col_ir], 'hora' : hora-1}, ignore_index = True)
            df_rad_horas.drop(['DF'], axis=1, inplace = True)
            df_rad_horas.drop(['DT'], axis=1, inplace = True)

            # Convierto las columnas a los tipos de dato correctos

            df_rad_horas["hora"] = pd.to_numeric([np.nan if pd.isna(c) == True else int(c) for c in df_rad_horas["hora"]])
            df_rad_horas["GL"] = pd.to_numeric([np.nan if (pd.isna(c) == True) or (c == "") else float(c) for c in df_rad_horas["GL"]])
            df_rad_horas["UVB"] = pd.to_numeric([np.nan if (pd.isna(c) == True) or (c == "") else float(c) for c in df_rad_horas["UVB"]])
            df_rad_horas["IR"] = pd.to_numeric([np.nan if (pd.isna(c) == True) or (c == "") else float(c) for c in df_rad_horas["IR"]])
            df_rad_horas["GL"] = df_rad_horas["GL"] *10/3.6
            df_rad_horas["UVB"] = df_rad_horas["UVB"] *1/(3.6*1000)
            df_rad_horas["IR"] = df_rad_horas["IR"] *10/3.6

            # Elimino Na's

            try:
                df_rad_horas.fillna({'IR': df_rad_horas["IR"].mean(), "UVB": df_rad_horas["UVB"].mean()}, inplace = True)
            except:
                df_rad_horas.fillna({'IR': 0, "UVB": 0}, inplace = True)

            df_rad_horas = df_rad_horas.fillna(0)

            # Se eliminan posibles filas repetidas

            df_rad_horas = df_rad_horas.drop_duplicates(['fecha', 'hora', "indicativo"], keep = 'first')
            df_rad_horas.reset_index(drop = True, inplace = True)

            return df_rad_horas

        df_aemet_clean = rad_aemet_clean(df_rad_aemet)


        ########################################### Se limpian los datos de radiación (SODA)
        def soda_clean(df_datos):

            # Quito columnas innecesarias

            df_datos.drop(['dateEnds'], axis=1, inplace = True)
            df_datos.drop(['toa'], axis=1, inplace = True)
            df_datos.drop(['cs_ghi'], axis=1, inplace = True)
            df_datos.drop(['cs_bhi'], axis=1, inplace = True)
            df_datos.drop(['cs_dhi'], axis=1, inplace = True)
            df_datos.drop(['cs_bni'], axis=1, inplace = True)
            df_datos.drop(['bhi'], axis=1, inplace = True)
            df_datos.drop(['dhi'], axis=1, inplace = True)
            df_datos.drop(['bni'], axis=1, inplace = True)
            df_datos.drop(['reliability'], axis=1, inplace = True)

            # Quito NAs
            df_datos = df_datos.fillna(0)

            # Convierto las columnas a los tipos de dato correctos

            df_datos['dateBegins'] = pd.to_datetime(df_datos['dateBegins'])
            df_datos = df_datos.rename(columns={'dateBegins':'date'})
            df_datos['hora'] = pd.to_datetime(df_datos['date']).dt.hour
            df_datos['fecha'] = [str(a)[0:10] for a in df_datos['date']]
            df_datos = df_datos[(df_datos["hora"] < hora_fin) & (df_datos["hora"] >= hora_ini)]
            df_datos.reset_index(drop = True, inplace = True)

            # Se eliminan posibles filas repetidas

            df_datos = df_datos.drop_duplicates(["date", 'fecha', 'hora', "estacion"], keep = 'first')
            df_datos.reset_index(drop = True, inplace = True)

            return df_datos

        df_soda_clean = soda_clean(df_soda)


        ########################################### Se organizan las observaciones de clima por filas según día de obtención de datos
        df_clima_total = df_clima_clean

        columnas_1 = [col for col in df_clima_total.columns[1:4]] + [str(col+"_d-1") for col in df_clima_total.columns[4:]]
        columnas_2 = [col for col in df_clima_total.columns[1:4]] + [str(col+"_d-2") for col in df_clima_total.columns[4:]]
        columnas_3 = [col for col in df_clima_total.columns[1:4]] + [str(col+"_d-3") for col in df_clima_total.columns[4:]]
        columnas_4 = [col for col in df_clima_total.columns[1:4]] + [str(col+"_d-4") for col in df_clima_total.columns[4:]]
        columnas_5 = [col for col in df_clima_total.columns[1:4]] + [str(col+"_d-5") for col in df_clima_total.columns[4:]]

        df_clima_dias_1 = pd.DataFrame(columns = columnas_1)
        df_clima_dias_2 = pd.DataFrame(columns = columnas_2)
        df_clima_dias_3 = pd.DataFrame(columns = columnas_3)
        df_clima_dias_4 = pd.DataFrame(columns = columnas_4)
        df_clima_dias_5 = pd.DataFrame(columns = columnas_5)

        for i, fila in df_clima_total.iterrows():


            # Para cada fila horaria, detecto de a que día pertenece y la adjunto al dataset correspondiente
            if (pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == 1:
                df_clima_dias_1.loc[len(df_clima_dias_1["fecha prediccion"])] = [elem for elem in fila][1:]

            if (pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == 2:
                df_clima_dias_2.loc[len(df_clima_dias_2["fecha prediccion"])] = [elem for elem in fila][1:]

            if (pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == 3:
                df_clima_dias_3.loc[len(df_clima_dias_3["fecha prediccion"])] = [elem for elem in fila][1:]

            if (pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == 4:
                df_clima_dias_4.loc[len(df_clima_dias_4["fecha prediccion"])] = [elem for elem in fila][1:]

            if (pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == 5:
                df_clima_dias_5.loc[len(df_clima_dias_5["fecha prediccion"])] = [elem for elem in fila][1:]

        df_total = pd.merge(df_clima_dias_1, df_clima_dias_2, how = "inner", on = ["hour", "fecha prediccion", "estacion"])
        df_total = pd.merge(df_total, df_clima_dias_3, how = "inner", on = ["hour", "fecha prediccion", "estacion"])
        df_total = pd.merge(df_total, df_clima_dias_4, how = "inner", on = ["hour", "fecha prediccion", "estacion"])
        df_total = pd.merge(df_total, df_clima_dias_5, how = "inner", on = ["hour", "fecha prediccion", "estacion"])

        df_clima_clean = df_total

        ########################################### Se organizan las observaciones de predicción de clima por filas según día de obtención de datos
        df_pred_total = df_pred_clean

        columnas_1 = [col for col in df_pred_total.columns[1:4]] + [str(col+"_pred_1") for col in df_pred_total.columns[4:]]
        columnas_2 = [col for col in df_pred_total.columns[1:4]] + [str(col+"_pred_2") for col in df_pred_total.columns[4:]]

        df_pred_dias_1 = pd.DataFrame(columns = columnas_1)
        df_pred_dias_2 = pd.DataFrame(columns = columnas_2)

        for i, fila in df_pred_total.iterrows():

            # Para cada fila horaria, detecto a que día pertenece y la adjunto al dataset correspondiente
            if ((pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == 0) | ((pd.to_datetime(fila["fecha prediccion"]) - pd.to_datetime(fila["date"])).days == -2):
                df_pred_dias_1.loc[len(df_pred_dias_1["fecha prediccion"])] = [elem for elem in fila][1:] 

            if (pd.to_datetime(fila["date"]) - pd.to_datetime(fila["fecha prediccion"])).days == 1:
                df_pred_dias_2.loc[len(df_pred_dias_2["fecha prediccion"])] = [elem for elem in fila][1:]

        df_pred_dias_1 = df_pred_dias_1.drop_duplicates(['hour', "fecha prediccion", "estacion"],
                                keep = 'first')
        df_pred_dias_1.reset_index(drop = True, inplace = True)
        df_pred_dias_2 = df_pred_dias_2.drop_duplicates(['hour', "fecha prediccion", "estacion"],
                                keep = 'first')
        df_pred_dias_2.reset_index(drop = True, inplace = True)

        df_total_previo = pd.merge(df_pred_dias_1, df_pred_dias_2, how = "inner", on = ["hour", "fecha prediccion", "estacion"])

        columnas_total = [col for col in df_pred_total.columns[1:4]] + [str(col+"_pred") for col in df_pred_total.columns[4:]]
        df_total = pd.DataFrame(columns = columnas_total)

        for i, fila in df_total_previo.iterrows():

            if (i in list(range(0,len(df_total_previo["hour"]),5000))) | (i == len(df_total_previo["hour"])-1):
                print("Procesando fila {} de {}".format(i, len(df_total_previo["hour"])))

            # Para cada hora, obtengo la media de los datos de las dos predichas
            fila_nueva = []
            df_new = pd.DataFrame()
            for j in range(0, len(columnas_total)):
                if j in [0,1,2]:
                    fila_nueva.append(fila[j]) 
                else:
                    fila_nueva.append(np.mean([fila[j], fila[j + (int((len(columnas_total)-3)))]]))
            df_new = pd.DataFrame([tuple(fila_nueva)], columns = columnas_total)
            df_total = df_total.append(df_new, ignore_index = True)

        df_pred_clean = df_total


        ########################################### Se unen los datasets

        def merge_datasets(df_estaciones_rad, df_clima, df_pred, df_aemet, df_soda):

            ## CLIMA ##

            # Se añade la columna de fechas del día a predecir al dataset de datos climatológicos
            import datetime
            fechas_atrasadas = ["{}-{}-{}".format(str((pd.to_datetime(f) + datetime.timedelta(days=1)).year), str((pd.to_datetime(f) + datetime.timedelta(days=1)).month).zfill(2), str((pd.to_datetime(f) + datetime.timedelta(days=1)).day).zfill(2)) for f in df_clima["fecha prediccion"]]
            df_clima.insert(0, "fecha_rad", fechas_atrasadas, True)

            # Se renombran columnas y se convierten las temperaturas a grados Cº
            df_clima = df_clima.rename(index = str, columns = {"hour": "hora", "estacion": "indicativo"})

            df_clima["temp_d-1"] = df_clima["temp_d-1"] - 273.15
            df_clima["temp_d-2"] = df_clima["temp_d-2"] - 273.15
            df_clima["temp_d-3"] = df_clima["temp_d-3"] - 273.15
            df_clima["temp_d-4"] = df_clima["temp_d-4"] - 273.15
            df_clima["temp_d-5"] = df_clima["temp_d-5"] - 273.15
            df_clima["feels_like_d-1"] = df_clima["feels_like_d-1"] - 273.15
            df_clima["feels_like_d-2"] = df_clima["feels_like_d-2"] - 273.15
            df_clima["feels_like_d-3"] = df_clima["feels_like_d-3"] - 273.15
            df_clima["feels_like_d-4"] = df_clima["feels_like_d-4"] - 273.15
            df_clima["feels_like_d-5"] = df_clima["feels_like_d-5"] - 273.15

            # Se crea el nuevo dataframe con las columnas objetivo de temperatura y velocidad de viento 
            df_objetivos = pd.DataFrame(columns = ["hora", "indicativo", "temp_objetivo"])
            df_objetivos["hora"] = df_clima["hora"]
            df_objetivos["indicativo"] = df_clima["indicativo"]
            df_objetivos["temp_objetivo"] = df_clima["temp_d-1"]

            # Se añade la columna de fechas del día a predecir al dataset de datos climatológicos
            fechas_atrasadas = ["{}-{}-{}".format(str((pd.to_datetime(f) - datetime.timedelta(days=1)).year), str((pd.to_datetime(f) - datetime.timedelta(days=1)).month).zfill(2), str((pd.to_datetime(f) - datetime.timedelta(days=1)).day).zfill(2)) for f in df_clima["fecha prediccion"]]
            df_objetivos.insert(0, "fecha_rad", fechas_atrasadas, True)

            # Se eliminan columnas innecesarias
            df_clima.drop(['fecha prediccion'], axis = 1, inplace = True)

            # Se añade la columna de indicativos de las estaciones de radiación más cercanas    
            df_clima["indicativo_rad"] = np.nan
            df_clima["lat"] = np.nan
            df_clima["lon"] = np.nan

            for i, fila in df_clima.iterrows():

                df_clima.loc[i, "lat"] = lat
                df_clima.loc[i, "lon"] = lon

                dist = 99999999999999999999

                # Para cada fila, busco la estacion de radiación más cercana
                for k in range(0, len(df_estaciones_rad["indicativo"])): 
                    lat_est = conversor_coordenadas(str(df_estaciones_rad["latitud"].loc[k]))
                    lon_est = conversor_coordenadas(str(df_estaciones_rad["longitud"].loc[k]))

                    distancia_prueba = distancia(lat, lon, lat_est, lon_est)
                    if(distancia_prueba < dist):
                        dist = distancia_prueba
                        df_clima.loc[i, "indicativo_rad"] = df_estaciones_rad.loc[k, "indicativo"]

            ## PREDICCION ##  

            # Se convierten las variables de temperatura a grados Cº        
            df_pred["temp_pred"] = df_pred["temp_pred"] - 273.15
            df_pred["feels_like_pred"] = df_pred["feels_like_pred"] - 273.15

            # Se añade la columna de fechas del día a predecir al dataset de predicciones climatológicos
            fechas_atrasadas = ["{}-{}-{}".format(str((pd.to_datetime(f) + datetime.timedelta(days=1)).year), str((pd.to_datetime(f) + datetime.timedelta(days=1)).month).zfill(2), str((pd.to_datetime(f) + datetime.timedelta(days=1)).day).zfill(2)) for f in df_pred["fecha prediccion"]]
            df_pred.insert(0, "fecha_rad", fechas_atrasadas, True)

            # Se renombran columnas y eliminan las innecesarias
            df_pred = df_pred.rename(index = str, columns = {"hour": "hora", "estacion": "indicativo"})
            df_pred.drop(['fecha prediccion'], axis = 1, inplace = True)

            ## RADIACION DIA ANTERIOR ##

            # Se añade la columna de fechas del día a predecir al dataset de radiación de AEMET
            df_aemet = df_aemet.rename(columns={'indicativo':'indicativo_rad'})
            fechas_atrasadas = ["{}-{}-{}".format(str((pd.to_datetime(f) + datetime.timedelta(days=1)).year), str((pd.to_datetime(f) + datetime.timedelta(days=1)).month).zfill(2), str((pd.to_datetime(f) + datetime.timedelta(days=1)).day).zfill(2)) for f in df_aemet["fecha"]]
            df_aemet.insert(0, "fecha_rad", fechas_atrasadas, True)

            # Se renombran columnas 
            df_aemet = df_aemet.rename(columns={'GL': 'rad_d-1', 'UVB': 'uvb_d-1', 'IR': 'ir_d-1'})

            # Se eliminan las columnas innecesarias
            df_aemet.drop(['fecha'], axis = 1, inplace = True)
            df_aemet.drop(['estacion'], axis = 1, inplace = True)

            ## RADIACION ##

            # Se renombran columnas y eliminan las innecesarias
            df_soda = df_soda.rename(index = str, columns = {"estacion": "indicativo", "fecha": "fecha_rad"})
            df_soda.drop(['date'], axis=1, inplace = True)

            # Se crea un dataset que contenga la variable de radiación de tres días antes
            df_rad_2 = pd.DataFrame(columns = ["indicativo", "hora", "rad_d-2"])
            df_rad_2["indicativo"] = df_soda["indicativo"]
            df_rad_2["hora"] = df_soda["hora"]
            df_rad_2["rad_d-2"] = df_soda["ghi"]

            # Se añade la columna de fechas del día a predecir al dataset de radiación de tres días antes
            fechas_atrasadas = ["{}-{}-{}".format(str((pd.to_datetime(f) + datetime.timedelta(days=3)).year), str((pd.to_datetime(f) + datetime.timedelta(days=3)).month).zfill(2), str((pd.to_datetime(f) + datetime.timedelta(days=3)).day).zfill(2)) for f in df_soda["fecha_rad"]]
            df_rad_2.insert(0, "fecha_rad", fechas_atrasadas, True)

            ## MERGE ##

            # Se unen los datasets
            df_total = pd.merge(df_clima, df_pred, how = "inner", on = ["fecha_rad", "hora", "indicativo"])
            df_total = pd.merge(df_total, df_aemet, how = "inner", on = ["fecha_rad", "hora", "indicativo_rad"])
            df_total = pd.merge(df_total, df_rad_2, how = "inner", on = ["fecha_rad", "hora", "indicativo"])

            df_total.drop(['indicativo_rad'], axis = 1, inplace = True)

            df_total.columns = [str(i) for i in df_total.columns]


            return df_total


        df_clima = df_clima_clean
        df_pred = df_pred_clean
        df_aemet = df_aemet_clean
        df_soda = df_soda_clean

        df_total = merge_datasets(df_estaciones_rad, df_clima, df_pred, df_aemet, df_soda)
        df_total["hora"] = pd.to_numeric([int(c) for c in df_total["hora"]])
        for i in range(3, len(df_total.columns)):
            df_total[df_total.columns[i]] = pd.to_numeric([float(c) for c in df_total[df_total.columns[i]]])
    
        
        
        ########################################### Predicción de producción eléctrica
        
        
        df_datos = df_total
        df_datos = df_datos[["hora"] + list(df_datos.columns)[3:]]


        st.text("Si cambia alguna característica de su instalación, deberá pulsar el botón de nuevo")
        
        ppico = potencia
        
        scalar = pk.load(open(directorio + 'data/Modelo_2/scaler_rad.pkl','rb'))
        pca = pk.load(open(directorio + 'data/Modelo_2/pca_rad.pkl','rb'))
        model = pk.load(open(directorio + 'data/Modelo_2/modelo_2_rad.pkl','rb'))

        pipeline = Pipeline([('transformer', scalar), ('pca', pca), ('estimator', model)])
        pred = pipeline.predict(df_datos)
        pred_rad = []
        for i in range(0, len(pred)):
            pred_rad.append(pred.tolist()[i][0])
        scalar = pk.load(open(directorio + 'data/Modelo_2/scaler_temp.pkl','rb'))
        pca = pk.load(open(directorio + 'data/Modelo_2/pca_temp.pkl','rb'))
        model = pk.load(open(directorio + 'data/Modelo_2/modelo_2_temp.pkl','rb'))    
    
    
        pipeline = Pipeline([('transformer', scalar), ('pca', pca), ('estimator', model)])

        pred = pipeline.predict(df_datos)
        pred_temp = []
        for i in range(0, len(pred)):
            pred_temp.append(pred.tolist()[i][0])
        
        dia_Gh = pred_rad
        temperatura_ambiente = pred_temp
        try:
            produccion = calcularEnergia(lat, lon, orient, incl, ppico, fecha, dia_Gh, temperatura_ambiente)
        except:
            html_temp = """
            <p style="text-align: center;"><span style="font-size: 19px; font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);
            "><strong>Ha ocurrido alg&uacute;n error, por favor, int&eacute;ntelo de nuevo </strong></span></p>
            """
            st.markdown(html_temp, unsafe_allow_html = True)
            
        
        if compens == 0:
            try:
                
                st.text("\n")
                col1, mid, col2 = st.beta_columns([3,6,1])
                with mid:
                    st.image(directorio + 'images/prediction.png', width = 300)
                

                html_temp = """
                <p style="text-align: center;"><span style="20px; color: rgb(250, 197, 28);"><strong><span style='font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
                font-size: 20px;'>Producci&oacute;n fotovoltaica (Wh) predicha para ma&ntilde;ana</span></strong></span></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
                
                html_temp = """
                <p><font color="#efefef" face="Calibri, sans-serif"><span style="font-size: 10px;">Se muestra a continuaci&oacute;n
                una representaci&oacute;n gr&aacute;fica de los valores horarios (Wh para cada una de las 24 horas del d&iacute;a
                de ma&ntilde;ana) de la producci&oacute;n fotovoltaica que se predicque que generar&aacute; su
                instalaci&oacute;n de paneles solares</span></font></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
    
                prod = pd.DataFrame({'Producción por hora (Wh)': produccion})
                st.area_chart(prod)
                
                # Imagen 
                col1, mid, col2 = st.beta_columns([1,6,1])
                with col1:
                    st.image(directorio + 'images/download.png', width = 65)
                with mid:
                    st.write('Descargar los datos:')
                st.markdown(descarga(prod, "prediccion"), unsafe_allow_html = True)
                
            except:
                
                html_temp = """
                <p style="text-align: center;"><span style="font-size: 19px; font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);
                "><strong>Ha ocurrido alg&uacute;n error, por favor, int&eacute;ntelo de nuevo </strong></span></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
            
            
        ########################################### Compensación de excedentes
        
        if compens == 1:
        

            # Definición del ID del indicador de precios de compensación de excedentes
            indicador = 1739

            # Token de acceso
            token = "27089f947b3e16a296875a0bc9dc387efa41acc7db6498676668e5150028cfdb"

            precios_excedente = api_ree(indicador, token)

            lista_precios = []
            for y in precios_excedente["value"]:
                lista_precios.append(y)

            perfiles = pd.read_csv(directorio + 'data/Perfiles_consumo.csv', sep=',')
            for i in range(0,24):
                perfiles[str(i)] = pd.to_numeric(perfiles[str(i)])

            pot_media = 4.5 #kW
            consumo_medio_casa = 3754/365 #kWh día
            consumo_medio_piso = 3373/365 #kWh día

            if casa == 1 and piso == 0:
                cons = consumo_medio_casa
            if piso == 1 and casa == 0:
                cons = consumo_medio_piso

            if tipo_1 == 1:
                perfil = [perfiles.loc[0][1+i]*cons*pot_c/pot_media*1000 for i in range(0,len(perfiles.loc[0])-1)] # En Wh
            elif tipo_2 == 1:
                perfil = [perfiles.loc[1][1+i]*cons*pot_c/pot_media*1000 for i in range(0,len(perfiles.loc[1])-1)]
            elif tipo_3 == 1:
                perfil = [perfiles.loc[2][1+i]*cons*pot_c/pot_media*1000 for i in range(0,len(perfiles.loc[2])-1)]
            elif tipo_4 == 1:
                perfil = [perfiles.loc[3][1+i]*cons*pot_c/pot_media*1000 for i in range(0,len(perfiles.loc[3])-1)]
            elif tipo_5 == 1:
                perfil = [perfiles.loc[4][1+i]*cons*pot_c/pot_media*1000 for i in range(0,len(perfiles.loc[4])-1)]
            elif tipo_6 == 1:
                perfil = [perfiles.loc[5][1+i]*cons*pot_c/pot_media*1000 for i in range(0,len(perfiles.loc[5])-1)]
            
            try:
                
                st.text("\n")
                col1, mid, col2 = st.beta_columns([3,6,1])
                with mid:
                    st.image(directorio + 'images/prediction.png', width = 300)
                

                
                html_temp = """
                <p style="text-align: center;"><span style="20px; color: rgb(250, 197, 28);"><strong><span style='font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif; font-size:
                20px;'>Perfil estimado de consumo y producci&oacute;n fotovoltaica predicha (Wh) para ma&ntilde;ana</span></strong></span></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
                
                html_temp = """
                <p><font color="#efefef" face="Calibri, sans-serif"><span style="font-size: 10px;">Se muestra a continuaci&oacute;n
                una representaci&oacute;n gr&aacute;fica de los valores horarios (Wh para cada una de las 24 horas del d&iacute;a
                de ma&ntilde;ana) del consumo estimado de la vivienda y la producci&oacute;n fotovoltaica que se ha predicho que generar&aacute; su
                instalaci&oacute;n de paneles solares</span></font></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
                predicc = pd.DataFrame({'Consumo por hora (Wh)': perfil, 'Producción fotovoltaica por hora (Wh)': produccion})
                st.area_chart(predicc)
                
                # Imagen 
                col1, mid, col2 = st.beta_columns([1,6,1])
                with col1:
                    st.image(directorio + 'images/download.png', width = 65)
                with mid:
                    st.write('Descargar los datos:')
                st.markdown(descarga(predicc, "prediccion"), unsafe_allow_html = True)
                st.text("\n")
                st.text("\n")
                
            except:
                
                html_temp = """
                <p style="text-align: center;"><span style="font-size: 19px; font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);
                "><strong>Ha ocurrido alg&uacute;n error, por favor, int&eacute;ntelo de nuevo </strong></span></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)

            diferencia = []
            for i in range(0, 24):
                diferencia.append(perfil[i]-produccion[i])

            compensacion = []
            for i in range(0, len(diferencia)):
                if diferencia[i] < 0:
                    compensacion.append((lista_precios[i]/1000000)*abs(diferencia[i]))
                else:
                     compensacion.append(0)

            try:
                
                st.text("\n")
                col1, mid, col2 = st.beta_columns([3,6,1])
                with mid:
                    st.image(directorio + 'images/compensation.png', width = 200)
                
                
                html_temp = """
                <p style="text-align: center;"><span style="20px; color: rgb(250, 197, 28);"><strong><span style='font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif; font-size:
                20px;'>Compensaci&oacute;n estimada de excedentes (&euro;) para cada hora de ma&ntilde;ana</span></strong></span></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)

                html_temp = """
                <p><font color="#efefef" face="Calibri, sans-serif"><span style="font-size:
                10px;">Se muestra a continuaci&oacute;n una representaci&oacute;n gr&aacute;fica de los valores
                horarios (&euro; para cada una de las 24 horas del d&iacute;a de ma&ntilde;ana) de la
                compensaci&oacute;n econ&oacute;mica que podr&aacute;&nbsp;recibir por el vertido de la electricidad
                producida por sus paneles solares que no vaya a ser consumida, siendo esta entregada a la red el&eacute;ctrica</span>
                </font></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
                comp = pd.DataFrame({'Compensacion por hora (€)': compensacion})
                st.area_chart(comp)
                
                # Imagen 
                col1, mid, col2 = st.beta_columns([1,6,1])
                with col1:
                    st.image(directorio + 'images/download.png', width = 65)
                with mid:
                    st.write('Descargar los datos:')
                
                st.markdown(descarga(comp, "compensacion"), unsafe_allow_html = True)
                
            except:
                
                html_temp = """
                <p style="text-align: center;"><span style="font-size: 19px; font-family: Tahoma, Geneva, sans-serif; color: rgb(209, 72, 65);
                "><strong>Ha ocurrido alg&uacute;n error, por favor, int&eacute;ntelo de nuevo </strong></span></p>
                """
                st.markdown(html_temp, unsafe_allow_html = True)
            
        
