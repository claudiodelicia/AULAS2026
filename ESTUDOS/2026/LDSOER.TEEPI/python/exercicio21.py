#exercicio 21 do livro main do olsen
#implementar um programa que recebe um numero e informe se o numero e:
#par ou impar, positivo zero ou negativo, multiplo de 2, multiplo de 3, multiplo de 5 
#sem usar %, pode usar elif

numero = int(input("digite um numero"))

if numero % 2 == 0:
    print("o numero e par")
else:  
     print("o numero e impar")
if numero > 0:
    print("o numero e positivo")
elif numero == 0:
    print("o numero e zero")
else:
    print("o numero e negativo")
if numero % 2 == 0:
    print("o numero e multiplo de 2")
elif numero % 3 == 0:
    print("o numero e multiplo de 3")
elif numero % 5 == 0:
    print("o numero e multiplo de 5")   
