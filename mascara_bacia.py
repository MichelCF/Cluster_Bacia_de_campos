#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:18:58 2020

@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF

"""


import xarray as xr
import pandas as pd

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
def mascara_oceano(c_dados = '/home',c_salvar='/home',n_arquivo='output.csv'):
    topografia = xr.open_dataset(c_dados).to_dataframe()
#Separa o index
    topografia = topografia.reset_index([0,1])
#Filtra todos os dados maiores que -100
    topografia = topografia.loc[topografia['z'] < -100]
    topografia.drop(columns =['z'], inplace = True)
    topografia.columns = ['longitude','latitude']

#separa o index
    topografia['longitude'] = topografia['longitude'].apply(lambda x: arredonda_float(x))
    topografia['latitude'] = topografia['latitude'].apply(lambda x: arredonda_float(x))
    topografia.drop_duplicates(inplace = True)
    topografia.to_csv(c_salvar+'/'+n_arquivo,index=False)
    return topografia 
    