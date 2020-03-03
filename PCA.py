#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:12:42 2020

@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF

"""


import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


matrix_u = pd.read_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/matrix_u_1994.csv')
matrix_v = pd.read_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/matrix_v_1994.csv')
matrix_v.set_index(['longitude', 'latitude'], inplace = True)
matrix_u.set_index(['longitude', 'latitude'],inplace = True)

scaler = StandardScaler()
matrix_u = scaler.fit_transform(matrix_u)


pca = PCA(n_components=2)
pca.fit_transform(matrix_u)
representatividade_u = pca.explained_variance_ratio_
componentes_u = pd.DataFrame(pca.components_)
pca.fit(matrix_v.transpose())
representatividade_v = pca.explained_variance_ratio_
componentes_v = pd.DataFrame(pca.components_)
componentes_u.to_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/componentes_u_1994.csv', sep =';')
componentes_u.to_csv('/home/ladsin/Área de Trabalho/Cluster_Bacia_de_campos/componentes_v_1994.csv', sep =';')