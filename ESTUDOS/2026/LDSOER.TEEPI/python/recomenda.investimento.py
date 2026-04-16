#Sistema de Recomendação de Investimentos: O programa deve classificar o perfil de um investidor (Conservador, Moderado ou Arrojado).

#Primeiro, pergunte o valor que ele deseja investir e seu tempo de experiência (em anos).
#Se o investidor tiver menos de 2 anos de experiência, ele é automaticamente "Conservador", independentemente do valor.
#Se tiver mais de 2 anos, verificar o valor investido:
    #* Até R$ 10.000: Moderado.
    #* Acima de R$ 10.000: Arrojado.
#Ao final, sugira um produto:
    #* Conservador -> Tesouro Direto;
    #* Moderado -> Fundos Imobiliários;
    #* Arrojado -> Ações.

valor_de_investimento = float(input("digite o valor que voce quer investir: "))
experiencia = int(input("digite quanto tempo em anos voce tem de experiencia com investimentos: "))

if experiencia < 2:
    perfil = "Conservador"

elif valor_de_investimento <= 10000:
    perfil = "Moderado"

else:
    perfil = "Arrojado"

if perfil == "Conservador":
    produto = "Tesouro Direto"
elif perfil == "Moderado":
    produto = "Fundos Imobiliários"
else:
    produto = "Ações"

print(f"seu perfil de investidor é {perfil} e o produto recomendado é {produto}")
