import libSTC
import math

'''  TESTA A ROTINA DE CALCULOS SEM A INTERFACE GRAFICA
Baseado nos algoritmos de Breno e Pedro ltda
'''

#Testing purposes
m=[1.3,1.3]
mi=[0.00031,0.00065]
kf=[0.180,0.154]
Pr=[3.97,7.34]
T1=35
T2=10
t1=1
t2=17.76
cp1=2803
cp2=4180
w=0.236
L=0.74
e=0.0007
k=17
Rd=(3*math.pow(10,-5))*2
dT1 = 35-10
dT2 = 1-17.76
Rcond=e/k
itmax=200
Npchute=50
Np=Npchute
tolerancia=0.00000001

Q=libSTC.calculaQ(m, cp1, dT1, cp2, dT2)[2]
dTln=libSTC.dtln(T1, T2, t1, t2)
Deq =libSTC.Diam_Eq(w,e)
ap=libSTC.Area_ap(w,e,Np)
h=libSTC.coef_convec(Pr,m,Deq,mi,ap,kf)
Ud=libSTC.coef_global(Rcond,h,Rd)

parametros = [w, e, Pr, m, Deq, mi, ap, kf, Rcond, h, Rd, Q, Ud, dTln, L]
Np = libSTC.iteracaoTrocadorPlacas(Np, itmax, tolerancia, parametros)
print("Numero de placas: %.0f\n" %Np)