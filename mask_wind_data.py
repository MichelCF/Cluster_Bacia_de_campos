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

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

def plot_points(data):
    for row in range(len(data)):
        row = data.iloc(row)
        
        
        

wind = xr.open_dataset('/media/ladsin/DATA/ERA5_wind/o_ERA5_wind_197901.nc') 

wind = wind.to_dataframe()
wind = wind.reset_index(['longitude','latitude','time'])
wind['teste'] = np.ones(85932)
#ind['teste'] = np.ones(124)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
ax.set_extent([-40,-50,-21,-29])
ax.scatter(wind.longitude,wind.latitude)
ax.stock_img()
ax.coastlines()