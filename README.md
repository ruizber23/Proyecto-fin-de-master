# KSOL - Plataforma de predicción de la producción eléctrica de una instalación fotovoltaica
[taxi image](/img/manhattan_taxis_image.jpg)
# IMAGEN PORTADA

This project has been developed by [Alejandro Ruiz Berciano](https://www.linkedin.com/in/alejandroruizber/).  
*Kschool - Master in Data Science*

* [1_Introduction](#1_Introduction)
* [2_Preparación](#2_Preparación)
   * [2_1_Requerimientos](#2_1_Requerimientos)
   * [2_2_Estructura e instrucciones](#2_2_Estructura-e-instrucciones)
* [3_Proyecto](#3_Proyecto)
   * [3_1_Desarrollo del proyecto](3_1_Desarrollo-del-proyecto)
   * [3_2_Funcionamiento](3_2_Funcionamiento)
* [4_Guia de interfaz](#4_Guia-de-interfaz)


# 1_Introduction

Este trabajo tendrá como objeto el desarrollar un modelo que permita a los propietarios domésticos de 
instalaciones fotovoltaicas conocer con antelación una estimación fiable de la producción de energía
eléctrica de la que podrán disponer a cada hora del día siguiente, con el objetivo de que puedan aprovechar
esta generación de electricidad al máximo. Este tipo de sistemas de predicción suelen ser de pago y 
desarrollados *ad hoc* para las características de una estación concreta, o dependientes de la conexión 
al inversor de cada planta. 

Así, se pretende aportar en este trabajo una herramienta gratuita enfocada en la predicción de la 
producción eléctrica de un sistema de placas fotovoltaicas para cualquier localización en España. Se trata
de alentar de este modo al consumidor doméstico a hacer un uso más eficiente de los recursos de generación
disponibles, de modo que ahorre en su factura eléctrica , y se reduzca el coste de la producción eléctrica
en el mercado para el resto de usuarios de la red, reduciendo al mismo tiempo la emisión de gases de
efecto invernadero.

**Por favor, consulte la memoria del proyecto, adjunta en el repositorio, para mayor detalle**

#2_Preparación
##2_1_Requerimientos

Este proyecto ha sido desarrollado en sistema operativo Linux (Ubuntu), concretamente en el kernel **xubuntu 20.04**. 
To execute this project it will be necesary to have installed the last version of Anaconda. 
Most libraries used by this project are included by this distribution.
Para poder tener las mismas librerías y versiones necesarias para la ejecución del proyecto, 
puede actualizar su environment (“env_name”) con el archivo **envirnonment.yml** adjunto:
``conda env update --name <env_name> --file environment.yml``

Más allá del paquete base de *Conda*, se han ejecutado las siguientes instalaciones:
``pip install ipynb``
``pip install python-crontab``
``conda install croniter -y``
``pip install --upgrade tensorflow``
``pip install streamlit-drawable-canvas``
``pip install streamlit``
``pip install geopandas``
``pip install streamlit_folium``


##2_2_Estructura-e-instrucciones

Para poder replicar el proyecto en otra máquina, se debe clonar este repositorio de GitHub.
La estructura de carpetas es la siguiente:

 IMAGEN ESTRUCTURA

*	[notebooks](https://github.com/ruizber23/TFM/tree/main/notebooks): contiene los notebooks de jupyter (.ipynb) necesarios para ejecutar el proyecto. 
*	[data](https://github.com/ruizber23/TFM/tree/main/data): contiene los datos necesarios para el entrenamiento del modelo. Estos deberán descargarse 
de la carpeta compartida adjunta y extraerse en esta.
* [images](https://github.com/ruizber23/TFM/tree/main/images): contiene las imágenes utilizadas en la interfaz de Streamlit y en el archivo README.
*	[envirnonment.yml](https://github.com/ruizber23/TFM/blob/main/environment.yml): Archivo generado para poder reproducir rápidamente el entorno del proyecto, 
con todos sus paquetes y versiones.

Todo ello debe encontrarse en una carpeta llamada TFM. En el caso de la máquina donde se ha desarrollado el proyecto, el directorio era: /home/dsc/git/TFM/.
Al comienzo de los diferentes notebooks se ejecutan los siguientes comandos:
``%cd /home/dsc/git/TFM/``
``directorio = '/home/dsc/git/TFM/'``
Si se desea ejecutar algún notebook, basta con cambiar este directorio en estas celdas, 
sustituyéndolo por aquel donde se encuentre todo descargado (folder TFM).


#3_Proyecto
##3_1_Desarrollo-del-proyecto

IMAGEN ESQUEMA FUNCIONAMIENTO

El proceso que se ha seguido para el desarrollo de este TFM es el siguiente:

*	En primer lugar, se han obtenido los datos necesarios para la elaboración de los modelos.
-	En el notebook [Estaciones](https://github.com/ruizber23/TFM/blob/main/notebooks/Estaciones.ipynb) se descargan las listas de estaciones 
meteorológicas y de radiación de [AEMET](https://opendata.aemet.es/centrodedescargas/productosAEMET). 
Para la obtención de los datos y los entrenamientos de los modelos se han utilizado las estaciones 
meteorológicas como localizaciones ejemplo dentro del territorio nacional.
-	En [Obtencion datos periodica](https://github.com/ruizber23/TFM/blob/main/notebooks/Obtencion_datos_periodica.ipynb) se obtienen los datos diarios para 
los modelos de predicción. Se ejecuta diariamente mediante el notebook [Lanzador_cron](https://github.com/ruizber23/TFM/blob/main/notebooks/Lanzador_cron.ipynb), 
en su forma *.py*, para generar, mediante la acumulación de estos archivos diarios, una base de datos históricos para el entrenamiento de los modelos. 
*	Después, los datos de los modelos se han limpiado y preparado para el entrenamiento. Notebooks: [Data_cleaning](https://github.com/ruizber23/TFM/blob/main/notebooks/Data_cleaning.ipynb)
y [Data_preparation](https://github.com/ruizber23/TFM/blob/main/notebooks/Data_preparation.ipynb).
*	Una vez obtenidos estos datos, se generan, prueban y entrenan dos modelos, que predecirán de forma 
horaria la radiación solar y la temperatura ambiente en la localización deseada, en [Modelo_rad](https://github.com/ruizber23/TFM/blob/main/notebooks/Modelo_rad.ipynb) 
y [Modelo_temp](https://github.com/ruizber23/TFM/blob/main/notebooks/Modelo_temp.ipynb).
*	Finalmente existe una serie de notebooks que permiten desplegar en modo local la interfaz de usuario 
mediante una app de Streamlit, donde cualquier propietario de una instalación fotovoltaica podrá 
introducir sus datos y obtener su predicción de producción eléctrica para el día siguiente. 
Notebooks: [Script_funcional](https://github.com/ruizber23/TFM/blob/main/notebooks/Script_funcional.ipynb), 
[Requisitos_streamlit](https://github.com/ruizber23/TFM/blob/main/notebooks/Requisitos_streamlit.ipynb), 
[Funciones_solares](https://github.com/ruizber23/TFM/blob/main/notebooks/Funciones_solares.ipynb),
[Interfaz](https://github.com/ruizber23/TFM/blob/main/notebooks/Interfaz.ipynb), 
[Streamlit_app_1](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_1.ipynb) 
y [Streamlit_app_2](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_2.ipynb).  


##3_2_Funcionamiento

Cuando el usuario solicite la predicción de su producción eléctrica para el día siguiente, se descargarán:
*	Datos de radiación solar de dos días antes: Se obtendrán 
de [CAMS Radiation Service](http://www.soda-pro.com/web-services/radiation/cams-radiation-service), 
un sistema de información fotovoltaica de la Comisión Europea.
*	Datos meteorológicos horarios de los últimos 5 días: Obtenidos de [OpenWeather](https://openweathermap.org/api/one-call-api#history).
*	Datos de predicción meteorológica de las siguientes 48 horas: Obtenidos 
de [OpenWeather](https://openweathermap.org/api/one-call-api).
*	Datos de radiación horaria del día anterior para las diferentes estaciones de radiación 
de [AEMET](https://opendata.aemet.es/centrodedescargas/productosAEMET):
Obtenidos de Aemet Open Data.

Estos datos se procesan para después generar las predicciones de temperatura ambiente y radiación solar por hora para una ubicación 
concreta, utilizando los modelos de *machine learning* entrenados previamente. Después, teniendo en cuenta las características 
de la instalación (orientación, inclinación y potencia pico) y la ubicación de esta, se devolverá la producción eléctrica para 
cada hora del día siguiente mediante un modelo de instalación fotovoltaica. Además, si el usuario introduce datos sobre su perfil de 
consumo, se generará también una estimación de la compensación de excedentes que podrá recibir.
 
IMAGEN FUNCIONAMIENTO REGULAR


#4_Guia-de-interfaz

En primer lugar, se debrá ejecutar (una única vez) el notebook [Requisitos_streamlit](https://github.com/ruizber23/TFM/blob/main/notebooks/Requisitos_streamlit.ipynb). Una vez hecho esto, 
para poder ejecutar de forma local la app de Streamlit, se deben seguir los siguientes pasos:
*	1-Se debe ejecutar el notebook [Interfaz](https://github.com/ruizber23/TFM/blob/main/notebooks/Interfaz.ipynb), para que exista el archivo .py que define la interfaz.
*	2-Se ejecuta [Streamlit_app_1](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_1.ipynb). 
*	3-Pasados **un par de minutos** con este notebook en ejecución (cuando la última celda muestre: *Compiled successfully!*), se ejecuta [Streamlit_app_2](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_2.ipynb). 
Las últimas celdas de ambos scripts deben mantenerse en ejecución al mismo tiempo. 
*	Se abrirá una pestaña en el navegador con la app de Streamlit.

Si aparece algún error, bastará con actualizar la página hasta que desaparezca.

Se adjunta a continuación un vídeo ejemplo del uso de la app:
[Turorial app](https://youtu.be/fr-S27TEnqg)




