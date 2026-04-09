#exercicio 19 do livro main do olsen
#nao pode usar elif

idade = float(input("digite a idade"))

if idade <= 12:
    print("voce e uma crianca")
else:
    if idade <= 18:
        print("voce e um adolescente")
    else:
        if idade <= 30:
            print("voce e um adulto")
        else:
            if idade <= 60:
                print("voce e um adulto")
            else:
                print("voce e um idoso")
    
        
        
        
        
        
        
