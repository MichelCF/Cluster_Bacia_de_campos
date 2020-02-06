#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 09:51:15 2020
@author: Michel Caiafa
@Email:  Michel.Caiafa@gmail.com
@Github: MichelCF
"""


import xarray as xr
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from collections import Counter

    
def media_cluster(dados):
    '''
    Calcula a maior frequencia das categorias em um periodo
    Input dataframe com longitude,latitude,categoria 
    Output um dataframe, com a maior frequencia de cada categoria, para cada lon lat
    '''
    saida = pd.DataFrame(columns = ['longitude','latitude','categoria'])
    pontos = dados.drop_duplicates(subset = ['longitude','latitude'])
    for i in range(len(pontos)):
        ponto = pontos.iloc[i]
        media = dados[(dados['latitude'].values == ponto.latitude) & (dados['longitude'].values == ponto.longitude)]
        ponto = [ponto.longitude,ponto.latitude,media['categoria'].mode()[0]]
        saida.loc[i] = ponto
    return saida

def prepara_dados_vento(caminho_dados, caminho_mascara):
    '''
    Mascara o dados de vento
    Input Caminho para seus dados e caminho para mascara que filtra a costa
    Output um dataframe com seus dados filtrados dentro do oceano
    '''
    vento = xr.open_mfdataset(caminho_dados).to_dataframe()
    topografia = pd.read_csv(caminho_mascara)
    vento = vento.reset_index(['longitude','latitude','time'])
    vento = pd.merge(vento,topografia, how='inner', on = ['longitude','latitude'])
    return vento[['longitude','latitude','time','u10','v10']]


def kmeans_bacia(dados, numero_k = 3):
    '''
    Gera as categorias e os centroides
    Input os dados que vão ser clusterizados e o numero de cluster
    Output o primeiro parametro é a lista com as categorias, o segundo parametro são os centroides
    '''
    kmeans = KMeans(n_clusters=numero_k)
    kmeans = kmeans.fit(dados)
    return [kmeans.fit_predict(dados)]#,  kmeans.cluster_centers_]

def plot_bacia(dados, localizacao = [-39,-51,-21,-30], salvar =None):
    '''
    Cria as imagens da bacia com pontos
    input dataframe com longitude,latitude e categoria, uma lista da com o tamanho da região
    caminho para salvar a imagem
    Output uma imagem e uma copia salva dela casa tenha passado um caminho no salvar
    '''
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.PlateCarree())
    ax.set_extent(localizacao)
    ax.scatter(dados.longitude,dados.latitude, c=dados.categoria)
    ax.coastlines()
    ax.gridlines()
    if salvar !=None:
        plt.savefig(salvar, format='png')
    plt.show()


def conta_frequencia_todas_linhas(data):
	mais_comum_linha = pd.DataFrame()
	for i in range(len(data)):
		mais_comum_linha[str(i)] = [Counter(data.iloc[i].values).most_common(1)[0][0]]
		print( Counter(data.iloc[i].values).most_common(1)[0][0])
	return mais_comum_linha.transpose()

def kmeans_dia(dados, numero_k = 3):
	rodadas = dados['time'].drop_duplicates()
	resultados_cluster = pd.DataFrame()
	resultados_centroide = pd.DataFrame()
	for rodada in range(len(rodadas)):
		print(type(rodadas.iloc[rodada]))
		dia = dados.loc[dados['time'] == rodadas[rodada]]
		dia.drop(columns = ['time'], inplace=True)
		dia = kmeans_bacia(dia)
		resultados_cluster['dia_'+str(rodada)] = dia[0]
		#resultados_centroide['dia_'+str(rodada)] = dia[1]
		
	return conta_frequencia_todas_linhas(resultados_cluster),resultados_cluster