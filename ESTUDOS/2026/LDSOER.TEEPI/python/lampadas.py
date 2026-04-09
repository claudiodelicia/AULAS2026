lampada = float(input("qual a potencia das lampadas em (WATTS)?"))
dimensoes = float(input("digite primeiro uma das dimensões do comodo em metros "))
dimensoes = dimensoes * float(input("digite a outra dimensão "))
valor = dimensoes * 18 #18 e o valor de watts por metro quadrado
valor = valor / lampada
print(f" a area de: {dimensoes}m² precisa de {valor} lampadas de {lampada}watts")