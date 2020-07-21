import numpy as np
from scipy import linalg


def matrix_complexa(dados_u, dados_v):
	'''


	Parameters
	----------
	dados_u : numpy array
		Uma matriz com as componentes u do vento.
		Cada coluna é um tempo
		Cada linha é uma lon lat
	dados_v : numpy array
		Uma matriz com as componentes u do vento.
		Cada coluna é um tempo
		Cada linha é uma lon lat
	Returns
	-------
	TYPE: Numpy array
		Retorna uma matriz complexa na forma u + v*1j
		Cada coluna é um tempo
		Cada linha é uma lon lat

	'''
	return dados_u+dados_v*1j


def ceof(dados, componentes=10):
	'''
	

	Parameters
	----------
	dados : numpy array
		Recebe uma matriz com dados complexos
	componentes : int
		Numero de componentes do CPCA, por padrão são 10

	Returns
	-------
	pcs : numpy array
		Retorna um matriz com as componentes complexas
	porcentagem : numpy array
		Retorna uma matriz com as porcentagens de cda componente
	auto_vetores : numpy array
		Retorna os auto vetores
	auto_valores : numpy array
		retorna os auto valores

	'''  
	linhas, _ = dados.shape
	
	matriz_convarianca =np.dot(np.conj(dados).T,dados)/linhas
	
	#Calcula os auto valores e auto valores
	auto_valores, auto_vetores = linalg.eig(matriz_convarianca)
	#Cria um index para ordenar os auto valores e auto vetores
	indx = auto_valores.argsort()[::-1] 
	auto_valores = auto_valores[indx]
	auto_vetores = auto_vetores[:,indx]
	
    #Calcula a porcentagem de cada componente
	porcentagem = (np.dot(auto_valores,100)/(np.sum(auto_valores))).real
    
	pcs = np.dot(dados,auto_vetores)
	return pcs,porcentagem[:componentes], auto_vetores[:,0:componentes], auto_valores[:componentes]




