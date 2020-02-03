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

wind = xr.open_dataset('/home/caiafa/Desktop/3_anos_wind/D_ERA5_wind_198001.nc')
topografia = xr.open_dataset('/home/caiafa/Desktop/Cluster_Bacia_de_campos/topografia_santos.grd').to_dataframe()
topografia = topografia.reset_index([0,1])
topografia1 = topografia.loc[topografia['z'] < -100]
topografia1.columns = ['longitude','latitude','altura']
topografia1.drop(columns =['altura'], inplace = True)
wind = wind.to_dataframe()
wind = wind.reset_index(['longitude','latitude','time'])
topografia1['longitude'] = topografia1['longitude'].apply(lambda x: arredonda_float(x))
topografia1['latitude'] = topografia1['latitude'].apply(lambda x: arredonda_float(x))
teste = pd.merge(wind,topografia1, how='inner', on = ['longitude','latitude'])
teste.drop_duplicates(inplace = True)
teste['norm_u10'] = teste['u10'] / np.linalg.norm(teste['u10'])
teste['norm_v10'] = teste['v10'] / np.linalg.norm(teste['v10'])

cluster = teste[['latitude','longitude','norm_u10','norm_v10']]
kmeans = KMeans(n_clusters=3)
cluster['categoria'] = kmeans.fit_predict(cluster)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.set_extent([-40,-50,-22,-29])
ax.scatter(cluster.longitude,cluster.latitude, c=cluster.categoria)
ax.coastlines()
ax.gridlines()

plt.show()




