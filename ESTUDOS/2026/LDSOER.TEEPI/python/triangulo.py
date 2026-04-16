#vai receber os 3 lados e os 3 angulos do triangulo, e tem que validar o triangulo por lado e por angulo,
#e classificar o triangulo por lado: equilatero, isosceles ou escaleno
#e classificar o triangulo por angulo: acutangulo, retangulo ou obtusangulo 

lado1 = float(input("digite o valor do primeiro lado do triangulo:"))
lado2 = float(input("digite o valor do segundo lado do triangulo:"))
lado3 = float(input("digite o valor do terceiro lado do triangulo:"))

angulo1 = float(input("digite o valor do primeiro angulo do triangulo:"))
angulo2 = float(input("digite o valor do segundo angulo do triangulo:"))
angulo3 = float(input("digite o valor do terceiro angulo do triangulo:"))

def triangulos(lado1, lado2, lado3):
        if lado1 == lado2 == lado3:
            print("o triangulo e equilatero")

        elif lado1 == lado2 or lado1 == lado3 or lado2 == lado3:
            print("o triangulo e isosceles")

        else:
            print("o triangulo e escaleno")

def triangulos2(angulo1, angulo2, angulo3):
        if angulo1 < 90 and angulo2 < 90 and angulo3 < 90:
            print("o triangulo e acutangulo")

        elif angulo1 == 90 or angulo2 == 90 or angulo3 == 90:
            print("o triangulo e retangulo")

        else:
            print("o triangulo e obtusangulo")




if (lado1 < lado2 + lado3) and (lado2 < lado1 + lado3) and (lado3 < lado1 + lado2):
    print("os lados formam um triangulo")
    if angulo1 + angulo2 + angulo3 == 180:
        print("os angulos formam um triangulo")
        triangulos(lado1, lado2, lado3)
        triangulos2(angulo1, angulo2, angulo3)
    else:
        print("mas, os angulos nao formam um triangulo")
       

else:
    print("os lados nao formam um triangulo")