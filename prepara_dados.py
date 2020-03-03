#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 13:59:10 2020

@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF

"""


import xarray as xr
import pandas as pd

vento = xr.open_mfdataset('/media/ladsin/DATA/ERA5_wind/D_ERA5_wind_1994*.nc').to_dataframe()
vento = vento.reset_index(['longitude','latitude','time'])
topografia = pd.read_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/topografia_oceano.csv')
vento = pd.merge(vento,topografia, how='inner', on = ['longitude','latitude'])

time = vento.time.drop_duplicates()

matrix_v = topografia[['longitude','latitude']]
matrix_v.set_index(['longitude', 'latitude'], inplace = True)
matrix_u = topografia[['longitude','latitude']]
matrix_u.set_index(['longitude', 'latitude'],inplace = True)
for i in range(len(time)):
    dia = vento[(vento['time'] == time[i])]
    matrix_v['v' + str(i+1)] = dia['v10'].values
    matrix_u['u' + str(i+1)] = dia['u10'].values
  

matrix_v.to_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/matrix_v_1994.csv', sep=';')

matrix_u.to_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/matrix_u_1994.csv', sep=';')