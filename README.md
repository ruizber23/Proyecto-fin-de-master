# KSOL - Prediction platform for the electricity production of a photovoltaic installation
![Portada](/images/fondo.jpg)

This project has been developed by [Alejandro Ruiz Berciano](https://www.linkedin.com/in/alejandroruizber/).  
*Kschool - Master in Data Science*

* [1_Introduction](#1_Introduction)
* [2_Preparation](#2_Preparation)
   * [2_1_Requirements](#2_1_Requirements)
   * [2_2_Structure and instructions](#2_2_Structure-and-instructions)
* [3_Project](#3_Project)
   * [3_1_Project development](3_1_Project-development)
   * [3_2_Operation](3_2_Operation)
* [4_Interface guide](#4_Interface-guide)


# 1_Introduction

This work will aim to develop a model that allows domestic owners of photovoltaic installations to know in advance a reliable estimation of the electricity production that they will be able to have at each hour of the next day, with the aim that they can take advantage of this generation of electricity to the maximum. These types of prediction systems are usually expensive and developed *ad hoc* for the characteristics of a specific installation, or dependent on the connection to the investor of each plant.

Thus, it is intended to provide in this work a free tool focused on the prediction of the electrical production of a photovoltaic panel system for any location in Spain. It is about encouraging the domestic consumer to make more efficient use of the available generation resources, in order to save on his electricity bill, and reduce the cost of electricity production in the market for the rest of the network users, while reducing the emission of greenhouse effect gases.

**Please read the project report, attached to the repository, for more details**

# 2_Preparation
## 2_1_Requirements

This project has been developed in the Linux operating system (Ubuntu), specifically in the kernel **xubuntu 20.04**. 
To execute this project it will be necesary to have installed the last version of Anaconda. 
Most libraries used by this project are included by this distribution.
In order to have the same libraries and versions necessary for the execution of the project,
you can update your environment ("env_name") with the attached file **envirnonment.yml**:
``conda env update --name <env_name> --file environment.yml``

Beyond the base package of *Conda*, the following installations have been executed:
``pip install ipynb``
``pip install python-crontab``
``conda install croniter -y``
``pip install --upgrade tensorflow``
``pip install streamlit-drawable-canvas``
``pip install streamlit``
``pip install geopandas``
``pip install streamlit_folium``


## 2_2_Structure-and-instructions

In order to replicate the project on another machine, this GitHub repository must be cloned.
The folder structure is as follows:

![Estructura1](/images/Esquema-carpetas-1.jpg)
![Estructura2](/images/Esquema-carpetas.jpg)


*	[notebooks](https://github.com/ruizber23/TFM/tree/main/notebooks): contains the jupyter notebooks (.ipynb) needed to run the project. 
*	[data](https://github.com/ruizber23/TFM/tree/main/data): contains the data necessary for training the model. These will need to be downloaded from the attached shared folder and extracted in *data*.
* [images](https://github.com/ruizber23/TFM/tree/main/images): contains the images used in the Streamlit interface and in the README file.
*	[envirnonment.yml](https://github.com/ruizber23/TFM/blob/main/environment.yml): File generated to be able to quickly reproduce the project environment, with all its packages and versions.

All of this must be in a folder called TFM. In the case of the machine where the project was developed, the directory was: /home/dsc/git/TFM/.
At the beginning of the different notebooks the following commands are executed:
``%cd /home/dsc/git/TFM/``
``directorio = '/home/dsc/git/TFM/'``
If you want to run a notebook, just change this directory in these cells, replacing it with the one where everything is downloaded (TFM folder).


# 3_Project
## 3_1_Project-development

![EsquemaTFM](/images/Esquema-TFM.jpg)

The process that has been followed for the development of this TFM is as follows:

*	In the first place, the necessary data for the elaboration of the models have been obtained.
- On the notebook [Estaciones](https://github.com/ruizber23/TFM/blob/main/notebooks/Estaciones.ipynb) lists of meteorological and radiation stations are downloaded from [AEMET](https://opendata.aemet.es/centrodedescargas/productosAEMET). To obtain the data and for the training of the models, the meteorological stations locations have been used as example locations within the national territory.
-	In [Obtencion datos periodica](https://github.com/ruizber23/TFM/blob/main/notebooks/Obtencion_datos_periodica.ipynb) daily data are obtained for the prediction models. It is run daily via notebook [Lanzador_cron](https://github.com/ruizber23/TFM/blob/main/notebooks/Lanzador_cron.ipynb), in its *.py* form, to generate, through the accumulation of these daily files, a historical database for the training of the models. 
*	Afterwards, the data from the models has been cleaned up and prepared for training. Notebooks: [Data_cleaning](https://github.com/ruizber23/TFM/blob/main/notebooks/Data_cleaning.ipynb)
and [Data_preparation](https://github.com/ruizber23/TFM/blob/main/notebooks/Data_preparation.ipynb).
*	Once these data are obtained, two models are generated, tested and trained, which will predict the
hourly solar radiation and ambient temperature at the desired location, in [Modelo_rad](https://github.com/ruizber23/TFM/blob/main/notebooks/Modelo_rad.ipynb) and [Modelo_temp](https://github.com/ruizber23/TFM/blob/main/notebooks/Modelo_temp.ipynb).
*	Finally, there is a series of notebooks that allow the user interface to be displayed locally through a Streamlit app, where any owner of a photovoltaic installation can enter its data and get a prediction of electricity production for the next day. Notebooks: [Script_funcional](https://github.com/ruizber23/TFM/blob/main/notebooks/Script_funcional.ipynb), [Requisitos_streamlit](https://github.com/ruizber23/TFM/blob/main/notebooks/Requisitos_streamlit.ipynb), [Funciones_solares](https://github.com/ruizber23/TFM/blob/main/notebooks/Funciones_solares.ipynb), [Interfaz](https://github.com/ruizber23/TFM/blob/main/notebooks/Interfaz.ipynb), [Streamlit_app_1](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_1.ipynb) and [Streamlit_app_2](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_2.ipynb).  


## 3_2_Operation

When the user requests the prediction of their electricity production for the next day, the following data will be downloaded:
*	Solar radiation data from two days before: Will be obtained from [CAMS Radiation Service](http://www.soda-pro.com/web-services/radiation/cams-radiation-service), a photovoltaic information system of the European Commission.
*	Hourly weather data for the last 5 days: Obtained from [OpenWeather](https://openweathermap.org/api/one-call-api#history).
*	Weather forecast data for the next 48 hours: Obtained from [OpenWeather](https://openweathermap.org/api/one-call-api).
*	Hourly radiation data of the previous day for the different radiation stations of [AEMET](https://opendata.aemet.es/centrodedescargas/productosAEMET): Obtained from Aemet Open Data.

These data are processed to later generate the predictions of ambient temperature and solar radiation per hour for a specific location, using previously trained *machine learning* models. Then, taking into account the characteristics of the installation (orientation, inclination and peak power) and its location, the electricity production for each hour of the following day will be returned by means of a photovoltaic installation model. In addition, if the user enters data about their consumption profile, an estimate of the surplus compensation that they may receive will also be generated.
 
![Esquema-funcionamiento](/images/Estructura_funcionamiento.jpg)


# 4_Interface-guide

![Tarot](/images/prediction.png) 


First, the notebook must be run (only once) [Requisitos_streamlit](https://github.com/ruizber23/TFM/blob/main/notebooks/Requisitos_streamlit.ipynb). Once this is done, in order to run the Streamlit app locally, the following steps must be followed:
*	1-The notebook [Interfaz](https://github.com/ruizber23/TFM/blob/main/notebooks/Interfaz.ipynb) should be running, so that the .py file that defines the interface exists.
*	2-[Streamlit_app_1](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_1.ipynb) is executed. 
*	3-After **a couple of minutes** with this notebook running (after the last cell shows: *Compiled successfully!*), [Streamlit_app_2](https://github.com/ruizber23/TFM/blob/main/notebooks/Streamlit_app_2.ipynb) is executed. The last cells of both scripts must be kept running at the same time. 
*	A tab will open in the browser with the Streamlit app.

If an error appears, it will be enough to refresh the page until it disappears, or repeat the process, waiting for more time between the execution of both notebooks.

An example video of the use of the app is attached below: [Tutorial app](https://youtu.be/fr-S27TEnqg)




