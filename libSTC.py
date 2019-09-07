import pandas as pd
import numpy as np
import os
import math

def tabela_fluidos(nome_fluido,t1,t2):
	'''
	Descr: Retorna as propriedades fisicas (rho, cp, kf, mi, pr) de um fluido selecionado um banco de dados

	Inputs: 
			- nome_fluido: string com o nome do fluido. ex: 'agua';
			- t1: temperatura de entrada do fluido [ºC];
			- t2: temperatura de saida do fluido [ºC];

	Outputs: 
			- list de dimensao (1,5) contendo rho, cp, kf, mi, pr [S.I.] nesta ordem.
	Author: Vinicius e Andre
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
	Author: Vinicius e Andre
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

def dtln(T1, T2, t1, t2):
    '''
	Descr: Calcula a variação de temperatura deltaTln

	Inputs: 
			- T1: Temperatura de entrada do fluido quente; [Qualquer unidade]
            - T2: Temperatura de saida do fluido quente
            - t1: Temperatura de entrada do fluido frio
            - t2: Temperatura de saida do fluido frio

	Outputs: 
			- deltaTln
	'''

    if T1 > T2 and t1 < t2 :
        dt1 = T1 - t2
        dt2 = T2 - t1
        if dt1 > 0 and dt2 > 0 :
            if dt1 == dt2 :
                dtln = dt1
                return dtln
            else :
                dtln = (dt1-dt2)/np.log(dt1/dt2)
                return dtln
        else :
            print ("Temperaturas inconsistentes!")
    else :
        print ("Temperaturas inconsistentes!")

def Diam_Eq(w,e):
	''' Descr: Calcula o diametro equivalente
	Input: 
			- w: 
			- e: 
	Outputs:
			- De: diametro equivalente
	Author: - Breno'''
	De = 4*w*e/(2*(w+e))
	return De

def Area_ap(w,e,Np):
	'''Descr: Calcula a area aparente
	Input: 
			- w: 
			- e: 
			- Np: Numero de placas
	Outputs:
			- De: Area aparente
	Author: - Breno'''
	a = w*e*((Np+1)/2)
	return a

def coef_convec(Pr,m,Deq,mi,ap,kf):   
	''' Descr: Calcula os coeficientes de transferencia de calor do fluido frio e quente
		   Obs: foi utilizada a correlação de Sinnot p/ o Nusselt
	Inputs: 
			- Pr: Numero de Prantl de ambos os fluidos em vetor [fluido 1, fluido 2];
			- m: Vazão mássica [fluido 1, fluido 2];
			- Deq: Diâmetro equivalente;
			- mi: Viscosidade dinamica [fluido 1, fluido 2];
			- ap: Area aparente
			- kf: Condutividade térmica do fluido [fluido 1, fluido 2].

	Outputs: 
			- h: Coeficiente de transferencia de calor [fluido 1, fluido 2].
	Author: Breno'''

	h= np.zeros(2)
	h[0] = 0.26 * math.pow(Pr[0],0.4)* math.pow((m[0]*Deq/(mi[0]*ap)),0.65) * (kf[0]/Deq)
	h[1] = 0.26 * math.pow(Pr[1],0.4)* math.pow((m[1]*Deq/(mi[1]*ap)),0.65) * (kf[1]/Deq)
	
	return h

def tabela_condutividade(nome_material):
    '''
    Descr: Retorna a condutividade termica do material desejado selecionado
    de um banco de dados

    Inputs:
                -nome_material: string com o nome do material. ex: 'cobre';
    Output:
                -k: valor da constante da condutividade
    Author: Matheus e Pedro
    Apoio Moral: Matheus
    '''
    db = pd.read_csv("database/materiais/k.csv", sep = ";") #Carrega o arquivo csv
    print(db)

    Material = db.iloc[0:db.shape[0],0]
    k = db.iloc[0:db.shape[0],1]

    material_list = Material.values.tolist()        # Cria uma lista a partir do dataframe

    index = material_list.index(nome_material)      # Indentifica uma string específica na lista
    return k[index]     # retorna o valor corresponde de k ao index da string

def area_troca_termica(Q, Ud, dTln, Aef):
    '''
	Descr: Calcula a area de troca térmica e o numero de placas

	Inputs: 
            - Q    : Calor
            - Ud   : Coeficiente global
            - dTln : deltaTln
            - Aef  : Area efetiva (w*L)

	Outputs: 
			-[A, Np]: list com a ara de troca termica necessaria e o numero de placas
	Author: Vinicius
	'''
    #Calculo do A
    A = Q/(Ud*dTln)
    Np = A/Aef

    return [A,Np]