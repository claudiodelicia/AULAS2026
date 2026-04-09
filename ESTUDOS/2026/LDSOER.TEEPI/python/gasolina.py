inicial = float(input("valor inical do odometro"))
final = float(input("valor final do odometro"))
gasto = float(input("quantos litros voce gastou?"))
ganho = float(input("quantos reais voce recebeu no dia?"))
media = (final - inicial) / gasto
salario_liquido = ganho - (gasto * 1.9 )
print(f"a sua media de consumo foi {media}Km/L")
print(f"voce recebeu {ganho} e seu salario liquido depois de pagar a gasolina e de {salario_liquido}")
