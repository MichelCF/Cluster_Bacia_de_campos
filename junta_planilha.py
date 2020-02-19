#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:55:29 2020

@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF

"""


import pandas as pd
tabelas_juntas = pd.DataFrame()
media_u = pd.read_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/media_mes_v_1994_1996.csv', sep =',')
media_v = pd.read_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/media_mes_u_1994_1996.csv', sep =',')

for i in range(12):
    coluna_u = media_u.columns[i]
    coluna_v = media_v.columns[i]
    tabelas_juntas[coluna_u] = media_u.iloc[:,i]
    tabelas_juntas[coluna_v] = media_v.iloc[:,i]

tabelas_juntas.to_csv('/home/ladsin/Downloads/drive-download-20200219T173523Z-001/tabelas_juntas.csv', sep=',')