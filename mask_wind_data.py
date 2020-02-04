#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 09:51:15 2020
@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF
"""


import xarray as xr
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def arredonda_float(numero_float):
    numero = int(numero_float)
    caso = numero_float - numero
    if caso ==0:
        return numero_float
    elif caso >=-0.25:
        return numero - 0.25
    elif caso >=-0.50:
        return numero - 0.50
    elif caso >= -0.75:
        return numero - 0.75
    else:
        return numero -1

#Carrega os dados de vento
wind = xr.open_dataset('/home/caiafa/Desktop/3_anos_wind/D_ERA5_wind_198001.nc').to_dataframe()
#Carrega o arquivo de topografia
topografia = xr.open_dataset('/home/caiafa/Desktop/Cluster_Bacia_de_campos/topografia_santos.grd').to_dataframe()
#Separa o index
topografia = topografia.reset_index([0,1])
#Filtra todos os dados maiores que -100
topografia = topografia.loc[topografia['z'] < -100]
topografia.drop(columns =['z'], inplace = True)
topografia.columns = ['longitude','latitude']

#separa o index
wind = wind.reset_index(['longitude','latitude','time'])
topografia['longitude'] = topografia['longitude'].apply(lambda x: arredonda_float(x))
topografia['latitude'] = topografia['latitude'].apply(lambda x: arredonda_float(x))
#remove os arquivos replicados
topografia.drop_duplicates(inplace = True)

#Apenas os dados de vento sobre o oceano
wind = pd.merge(wind,topografia, how='inner', on = ['longitude','latitude'])

wind['norm_u10'] = wind['u10'] / np.linalg.norm(wind['u10'])
wind['norm_v10'] = wind['v10'] / np.linalg.norm(wind['v10'])

#Prepara o k means e roda
kmeans = KMeans(n_clusters=3)
wind['categoria'] = kmeans.fit_predict(wind[['norm_u10','norm_v10']])


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.set_extent([-40,-50,-22,-29])
ax.scatter(wind.longitude,wind.latitude, c=wind.categoria)
ax.coastlines()
ax.gridlines()

plt.show()




