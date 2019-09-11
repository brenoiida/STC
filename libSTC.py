import pandas as pd
import numpy as np
from scipy import interpolate
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
			- list de dimensao (1,5) contendo rho, cp, kf, mi, pr, aviso [S.I.] nesta ordem.
	Author: Vinicius e Andre
	'''

	#print(nome_fluido)
	db = pd.read_csv("database/fluidos/%s.csv" %nome_fluido, sep = ";") #Carrega arquivo csv
	db = db.sort_values(by=['Temperatura'])   #Ordena os dados p/ nao dar pau no interp

	aviso = 0
	#aviso = 0: Valor de temperatura avaliada dentro do intervalo do banco de dados
	#aviso = 1: Valor de temperatura avaliada abaixo do intervalo do banco de dados
	#aviso = 2: Valor de temperatura avaliada acima do intervalo do banco de dados


	T=db.iloc[0 : db.shape[0] ,0]        					# Corta matriz db da linha 0 até ultima linha
	Rho=db.iloc[0 : db.shape[0] ,1]							# (db.shape[0]) na coluna respectiva
	Cp=db.iloc[0: db.shape[0] ,2]
	Kf=db.iloc[0 : db.shape[0] ,3]
	Mi=db.iloc[0 : db.shape[0] ,4]
	Pr=db.iloc[0 : db.shape[0] ,5]
	#print (T)
	Tmin = T.min()			# Pega a menor e a maior temperatura do banco de dados
	Tmax = T.max()
	#print (Tmin,Tmax)
	tm = (t1+t2)/2

	#Valores extrapolados
	if tm<Tmin or tm>Tmax:
		f_rho = interpolate.interp1d(T, Rho, fill_value='extrapolate')
		f_cp = interpolate.interp1d(T, Cp, fill_value='extrapolate')
		f_kf = interpolate.interp1d(T, Kf, fill_value='extrapolate')
		f_mi = interpolate.interp1d(T, Mi, fill_value='extrapolate')
		f_pr = interpolate.interp1d(T, Pr, fill_value='extrapolate')

		rho = f_rho(tm)
		cp = f_cp(tm)
		kf = f_kf(tm)
		mi = f_mi(tm)
		pr = f_pr(tm)

		#Avisos paroquiais
		if tm<Tmin:
			#print("T médio (%.2f) abaixo de T minimo (%.2f)\n" %(tm, Tmin))
			aviso = 1
		elif tm>Tmax:
			#print("T médio (%.2f) acima de T máximo (%.2f)\n" %(tm, Tmax))
			aviso = 2
	
	#Valores interpolados
	else:
		rho=np.interp(tm,T,Rho)	#Interpola no valor tm, nos dados Rho vs T
		cp=np.interp(tm,T,Cp)
		kf=np.interp(tm,T,Kf)
		mi=np.interp(tm,T,Mi)
		pr=np.interp(tm,T,Pr)
	
	return [rho,cp,kf,mi,pr, aviso]   #Fim da funcao

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
	Authors: Pedro e Matheus
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

def calculaQ(m1, cp1, dT1, m2, cp2, dT2):
    '''
	Descr: Calcula a taxa de troca de calor Q p/ fluido quente e frio( ou fluido 1 e 2)
    Ainda verifica se ambos os fluidos estao esquentando ou esfrianddo, evitando bugs

	Inputs: 
			- m1: Vazao massica do fluido 1
			- cp1: Calor especifico do fluido 1
			- dT1: Variação de temperatura do fluido 1
            - m2: Vazao massica do fluido 2
            - cp2: Calor especifico do fluido 2
            - dT2: Variação de temperatura do fluido 2
	Outputs: 
			- list contendo [Q1, Q2, menorQ, porc]:
                - Q1: Q do fluido 1
                - Q2: Q do fluido 2
                - menorQ: menorQ entre Q1 e Q2
                - porc: Porcentagem da diferença entre ambos Q1 e Q2
	Author: Vinicius
	'''

    Q1 = m1*cp1*dT1
    Q2 = m2*cp2*dT2

    if dT1>=0 and dT2>=0:
        print("Erro, ambos os fluidos estão esquentando")
        return "Erro Q1"
    elif dT1<0 and dT2<0:
        print("Erro, ambos os fluido estão esfriando")
        return "Erro Q2"


    dif = abs(Q1+Q2) #Nao precisa subtrair, um dos Qs ja vai ter sinal de menos   

    vetor = np.array([Q1, Q2])
    menorQ = np.min(vetor)

    porc = abs(dif/(menorQ))

    print("Afastamento de %.2f %% no balanço de energia" %(porc*100))

    #Retorna o pior caso (menor troca de temperatura) e a porcentagem do desvio entre os Qs
    return [Q1, Q2, menorQ, porc]

def ConverterTemperatura(esc, num):
    ''' Descr: Converte o valor de temperatura de qualquer unidade p/ ºC p/ ser utilizado na busca do banco de dados
	Input: 
			- esc: string contendo a unidade de medida [ºC, K, ºF, R]
			- num: Valor da temperatura na unidade fornecida
	Outputs:
			- temp: Temperatura convertida em ºC
	Author: - Thenysson'''

    if esc == 'ºC':
      temp = num  
    elif esc == 'K':
      temp = num-273.15
    elif esc == 'ºF':
      temp = (num - 32)*(5/9)
    elif esc == 'R':
      temp = (num - 491.67)*(5/9)

    return(temp)

def ConverterVazão(mod, uni,rho):
	''' Descr: Converte o valor da vazão fornecida para vazão massica no S.I. 
	Input: 
			- mod: Valor da vazão fornecida (magnitude)
			- uni: Unidade da vazão fornecida
			- rho: Massa específica do fluído
	Outputs:
			- vaz: Vazão convertida em kg/s
	Author: - Thenysson'''

	if uni == 'kg/s':
		vaz = mod
	elif uni =='kg/h':
		vaz = mod/3600
	elif uni == 'g/s':
		vaz = mod/1000
	elif uni =='L/s':
		vaz = (mod*rho)/1000
	elif uni =='m3/h':
	    vaz = (mod*rho)/3600
	return vaz
