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