#se o historico for "ruim", o credito e negado
#se for "bom", verifique a idade
#se tiver entre 18 e 30 anos, ele pode finaciar em ate 35 anos.
#se tiver entre 31 e 60 anos, ele pode financiar em ate 25 anos
#se tiver mais de 60 anos, ele nao pode financiar por risco de idade
#dentro das faixas aprovadas, verifique se a parcela(calculada sobre o valor total/meses ) compromete mais 25% da renda mensal do cliente, se sim, o credito e negado, se nao, o credito e aprovado

historico = input("digite o historico do cliente: bom ou ruim?")
if historico == "ruim":
    print("credito negado")
elif historico == "bom":
    idade = int(input("digite a idade do cliente?  "))
    if idade < 18:
        print("credito negado por idade")
    elif idade < 30:
        meses = 35 * 12
        valor_total = float(input("digite o valor total do emprestimo?  "))
        parcela = valor_total / meses
        renda_mensal = float(input("digite a renda mensal do cliente?  "))
        if parcela > renda_mensal * 0.25:
            print("credito negado por comprometimento de renda")
        else:
            print("credito aprovado, mas com prazo de financiamento reduzido para 35 anos")

    elif idade < 60:
        meses = 25 * 12
        valor_total = float(input("digite o valor total do emprestimo?  "))
        parcela = valor_total / meses
        renda_mensal = float(input("digite a renda mensal do cliente?  "))
        if parcela > renda_mensal * 0.25:
            print("credito negado por comprometimento de renda")
            
        else:
            print("credito aprovado, mas com prazo de financiamento reduzido para 25 anos")

    else:
        print("credito negado por idade")
        exit()
 
