def entrada():
    nota1 = float(input("Digite a primeira nota: "))
    nota2 = float(input("Digite a segunda nota: "))
    nota3 = float(input("Digite a terceira nota: "))
    nota4 = float(input("Digite a quarta nota: "))
    return nota1, nota2, nota3, nota4

def processamento(nota1, nota2, nota3, nota4):
    media = (nota1 + nota2 + nota3 + nota4) / 4
    return media
def saida(media):
    print(f"A média das notas é: {media:.2f}")

def main():
    nota1, nota2, nota3, nota4 = entrada()
    media = processamento(nota1, nota2, nota3, nota4)
    saida(media)
    
    
if __name__ == "__main__":
    main()