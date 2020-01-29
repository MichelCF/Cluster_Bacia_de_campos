#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 09:51:15 2020

@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF

"""


import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.ticker as mticker

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
wind = xr.open_dataset('/media/ladsin/DATA/ERA5_wind/D_ERA5_wind_197901.nc') 
topografia = xr.open_dataset('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/topografia_santos.grd').to_dataframe()
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



fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.set_extent([-40,-50,-22,-29])
ax.scatter(teste.longitude,teste.latitude)
ax.coastlines()
ax.gridlines()

plt.show()




