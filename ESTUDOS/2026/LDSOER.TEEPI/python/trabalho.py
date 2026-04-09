salario = float(input("quanto voce ganha por hora?"))
salario = salario * float(input("quantas horas voce trabalhou por mes?"))

print(f"o seu salario bruto e de:{salario}")

salario = salario - salario * 0.11

print(f"o seu salario bruto - o INSS e de:{salario}")

salario = salario - salario * 0.05

print(f"o seu salario liquido e de:{salario}")
