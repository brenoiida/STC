import pandas as pd
import numpy as np
import os

def tabela_fluidos(nome_fluido,t1,t2):
	'''
	Descr: Retorna as propriedades fisicas (rho, cp, kf, mi, pr) de um fluido selecionado um banco de dados

	Inputs: 
			- nome_fluido: string com o nome do fluido. ex: 'agua';
			- t1: temperatura de entrada do fluido [ºC];
			- t2: temperatura de saida do fluido [ºC];

	Outputs: 
			- list de dimensao (1,5) contendo rho, cp, kf, mi, pr [S.I.] nesta ordem.
	'''

	print(nome_fluido)
	db = pd.read_csv("database/fluidos/%s.csv" %nome_fluido, sep = ";") #Carrega arquivo csv

	T=db.iloc[0 : db.shape[0] ,0]        					# Corta matriz db da linha 0 até ultima linha
	Rho=db.iloc[0 : db.shape[0] ,1]							# (db.shape[0]) na coluna respectiva
	Cp=db.iloc[0: db.shape[0] ,2]
	Kf=db.iloc[0 : db.shape[0] ,3]
	Mi=db.iloc[0 : db.shape[0] ,4]
	Pr=db.iloc[0 : db.shape[0] ,5]
	#print (T)
	Tmin = T.iloc[0]			# Pega a menor e a maior temperatura do banco de dados
	Tmax = T.iloc[-1]
	#print (Tmin,Tmax)
	tm = (t1+t2)/2

	# anti-anta

	if tm< Tmin:
		print("Valor de T médio abaixo do T mín do banco de dados: %.2f °C "%Tmin)
	elif tm> Tmax:
		print("Valor de T médio acima do T máx do banco de dados: %.2f °C "%Tmax)

	print("Temperatura média: %.2f °C"%tm)
	rho=np.interp(tm,T,Rho)								#Interpola no valor tm, nos dados Rho vs T
	cp=np.interp(tm,T,Cp)
	kf=np.interp(tm,T,Kf)
	mi=np.interp(tm,T,Mi)
	pr=np.interp(tm,T,Pr)
	
	return [rho,cp,kf,mi,pr]   #Fim da funcao

def Nome_fluidos():

	'''
	Descr: Retorna os nomes dos fluidos disponiveis

	Inputs: 

	Outputs: 
			- list com os nomes do fluidos de dimensao (1,n), onde n é o número de arquivos de 
			  extensão ".csv" contidos na pasta database. 
	'''

	files = os.listdir("database/fluidos")  # Carrega todos os arquivos contidos em database e salva em files

	filesDB = [] 
	Nomefluidos =[]

	# Salva em filesDB os arquivos com extensão ".csv"

	for nome in files:
		if '.csv' in nome:
			filesDB.append(nome)

	# Salva em Nomefluidos os nomes dos fluidos sem os caracteres ".csv"

	for nome in filesDB:
		Nomefluidos.append(nome[0:-4])
	
	return Nomefluidos     # Fim da função	