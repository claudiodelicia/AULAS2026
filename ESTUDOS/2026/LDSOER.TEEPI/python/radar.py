#exercicio de um sistema de radar e multas
#objetivo: ler a velocidade de um carro e o tipo de via: escolar, rodovia ou escolar
#se a velocidade for maior que o limite permitido, o programa deve informar a multa correspondente
#urbana 60km/h
#rodovia 110km/h
#escolar 30km/h
#se ela passar do limite verifique o percentual
#20% multa leve
#de 21 para 50% multa grave
#acima de 50% multa gravissima
velocidade = float(input("digite a velocidade do carro? "))   
tipo_via = input("digite o tipo de via: urbana, rodovia ou escolar? ")

if tipo_via == "urbana":
    limite = 60

elif tipo_via == "rodovia":
    limite = 110

elif tipo_via == "escolar":
    limite = 30

else:
    print("tipo de via invalida")   
    exit() 


if velocidade > limite:
    percentual = (velocidade - limite) / limite * 100
    
    if percentual <= 20:
        print("multa leve")

    elif percentual <= 50:
        print("multa grave")

    else:
        print("multa gravissima")

else:
    print("velocidade dentro do limite permitido")

