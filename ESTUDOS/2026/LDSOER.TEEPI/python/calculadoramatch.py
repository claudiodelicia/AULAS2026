operação = input("digite a operação que deseja realizar: +, -, * ou /?  ")
num1 = float(input("digite o primeiro numero  "))
num2 = float(input("digite o segundo numero  "))

match operação:
    case "+":
        resultado = num1 + num2
    case "-":
        resultado = num1 - num2
    case "*":
        resultado = num1 * num2 
    case "/":
        resultado = num1 / num2
    case _:
        print("operacao invalida")
        
print(f"o resultado da operacao {operação} entre {num1} e {num2} é {resultado}")