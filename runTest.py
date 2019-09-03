import libSTC as stc

print("Fluidos disponiveis\n")
fluidos = stc.Nome_fluidos()

print(fluidos)
f_selecionado = int(input("\n\nSelecione o indice do fluido desejado (1 a %d): " %(len(fluidos))))

nomeFluido_selecionado = fluidos[f_selecionado-1]
print(nomeFluido_selecionado)

t1= float(input("Temperatura de entrada: "))
t2= float(input("Temperatura de saída: "))

resultados = stc.tabela_fluidos(nomeFluido_selecionado,t1,t2)

print("Rho = %.2f " %resultados[0])
print("Cp = %.2f " %resultados[1])
print("Kf = %.2f " %resultados[2])
print("Mi = %.2f " %resultados[3])
print("Pr = %.2f " %resultados[4])

print("Calculo de deltaTln")
print("T1 = 200   T2 = 100")
print("t1 = 50    t2 = 51")
print("deltaTln=%.2f\n" %stc.dtln(200, 100, 50, 51))

print("Diametro equivalente")
print("w = 5   e = 8")
print("Deq = %f\n" %stc.Diam_Eq(0.236,0.0007))

print("Area aparente")
print("w = 5 e = 8  Np=70")
print("Ap = %f\n" %stc.Area_ap(0.236,0.0007,35))

print("Pr=[2,268.2]")
print("m = [1, 1.5]")
print("mi=[2,1.308*10**(-3)]")
print("kf=[1,0.02]\n")
mi=[2,1.308*10**(-3)]
kf=[1,0.02]
Pr=[2,268.2]
m = [1,1.5]
Deq = stc.Diam_Eq(0.236,0.0007)
ap = stc.Area_ap(0.236,0.0007,35)

h = stc.coef_convec(Pr, m,Deq,mi,ap, kf)

print("h = [%.2f, %.2f]" %(h[0], h[1]))