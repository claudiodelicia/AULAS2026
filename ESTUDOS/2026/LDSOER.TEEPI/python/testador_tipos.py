"""
╔═══════════════════════════════════════════════════════════════╗
║   🔍 TESTADOR DE TIPOS DE VARIÁVEIS                         ║
║                                                               ║
║   Digite qualquer valor e o programa vai te dizer:           ║
║   • Qual tipo de variável esse valor DEVERIA ser             ║
║   • Para quais tipos ele PODE ser convertido                 ║
║   • Para quais tipos ele NÃO pode ser convertido             ║
║                                                               ║
║   Digite 'sair' para encerrar o programa.                    ║
╚═══════════════════════════════════════════════════════════════╝
"""

def analisar_valor(texto):
    """
    Recebe o texto digitado pelo usuário e analisa qual tipo
    de variável ele deveria ser em Python.
    """

    # ─── 1. Verificar se é BOOL ───
    # Em Python, True e False (com letra maiúscula) são bool
    if texto == 'True' or texto == 'False':
        valor_real = True if texto == 'True' else False
        tipo_ideal = 'bool'
        explicacao = (
            f"'{texto}' é um valor booleano (verdadeiro/falso).\n"
            f"     Em Python, escrevemos: x = {texto}\n"
            f"     ⚠️  Cuidado: 'true' (minúsculo) NÃO funciona! Sempre use '{texto}'."
        )
        return valor_real, tipo_ideal, explicacao

    # ─── 2. Verificar se é INT (número inteiro) ───
    # Tenta converter para int. Se funcionar, é um número inteiro.
    try:
        valor_int = int(texto)
        # Verifica se não tem ponto decimal (senão seria float)
        if '.' not in texto:
            valor_real = valor_int
            tipo_ideal = 'int'
            explicacao = (
                f"'{texto}' é um número INTEIRO (sem casas decimais).\n"
                f"     Em Python, escrevemos: x = {valor_int}\n"
                f"     💡 Use int quando o valor nunca terá casas decimais\n"
                f"        (idade, quantidade, ano, etc)."
            )
            return valor_real, tipo_ideal, explicacao
    except ValueError:
        pass

    # ─── 3. Verificar se é FLOAT (número decimal) ───
    # Tenta converter para float. Se funcionar, é um número decimal.
    try:
        valor_float = float(texto)
        valor_real = valor_float
        tipo_ideal = 'float'
        explicacao = (
            f"'{texto}' é um número DECIMAL (com casas decimais).\n"
            f"     Em Python, escrevemos: x = {valor_float}\n"
            f"     💡 Use float para valores com vírgula/ponto\n"
            f"        (preço, peso, altura, nota, etc)."
        )
        return valor_real, tipo_ideal, explicacao
    except ValueError:
        pass

    # ─── 4. Se não é nada acima, é STR (texto) ───
    valor_real = texto
    tipo_ideal = 'str'
    explicacao = (
        f"'{texto}' é um TEXTO (string).\n"
        f"     Em Python, escrevemos: x = '{texto}'\n"
        f"     💡 Use str para nomes, frases, endereços, etc.\n"
        f"        Strings sempre vão entre aspas '' ou \"\"."
    )
    return valor_real, tipo_ideal, explicacao


def testar_conversoes(valor_real):
    """
    Testa para quais tipos o valor pode ser convertido
    e mostra os resultados.
    """
    conversoes = {
        'int':   int,
        'float': float,
        'str':   str,
        'bool':  bool,
    }

    resultados = []
    for nome, func in conversoes.items():
        try:
            resultado = func(valor_real)
            resultados.append((nome, True, resultado))
        except (ValueError, TypeError):
            resultados.append((nome, False, None))

    return resultados


def mostrar_resultado(valor_real, tipo_ideal, explicacao, conversoes):
    """Exibe o resultado completo da análise de forma bonita."""

    print()
    print("  ┌─────────────────────────────────────────────────────┐")
    print(f"  │  📊 RESULTADO DA ANÁLISE                            │")
    print("  └─────────────────────────────────────────────────────┘")
    print()

    # Tipo identificado
    emojis = {'int': '🔢', 'float': '🔢', 'str': '📝', 'bool': '✅'}
    emoji = emojis.get(tipo_ideal, '❓')

    print(f"  {emoji} TIPO IDEAL: {tipo_ideal}")
    print(f"     {explicacao}")
    print()

    # Tabela de conversões possíveis
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  🔄 CONVERSÕES POSSÍVEIS                            │")
    print("  └─────────────────────────────────────────────────────┘")
    print()

    for nome, sucesso, resultado in conversoes:
        if sucesso:
            print(f"     ✅ {nome:>5}({repr(valor_real)})  =  {repr(resultado)}")
        else:
            print(f"     ❌ {nome:>5}({repr(valor_real)})  =  ERRO! Não é possível converter.")

    print()

    # Dica extra baseada no tipo
    print("  ┌─────────────────────────────────────────────────────┐")
    print("  │  💡 DICA EXTRA                                      │")
    print("  └─────────────────────────────────────────────────────┘")
    print()

    if tipo_ideal == 'int':
        print("     Se você colocar aspas, vira string: '4' é str, não int!")
        print("     Para declarar em Python:  x = " + str(valor_real))
    elif tipo_ideal == 'float':
        print("     Se você colocar aspas, vira string: '3.14' é str, não float!")
        print("     Para declarar em Python:  x = " + str(valor_real))
    elif tipo_ideal == 'str':
        print("     Para declarar em Python:  x = '" + str(valor_real) + "'")
        # Verifica se parece número mas é string
        try:
            float(valor_real)
            print("     ⚠️  ATENÇÃO: Se você quer usar como NÚMERO, tire as aspas!")
        except (ValueError, TypeError):
            pass
    elif tipo_ideal == 'bool':
        print("     bool só tem 2 valores: True ou False")
        print("     Para declarar em Python:  x = " + str(valor_real))
        print("     ⚠️  Lembre: true/false (minúsculo) NÃO funciona!")

    print()


# ══════════════════════════════════════════════════════════════
#  🚀 PROGRAMA PRINCIPAL - LOOP INTERATIVO
# ══════════════════════════════════════════════════════════════

print()
print("  ╔═══════════════════════════════════════════════════════╗")
print("  ║   🔍 TESTADOR DE TIPOS DE VARIÁVEIS EM PYTHON       ║")
print("  ║                                                       ║")
print("  ║   Digite qualquer valor para descobrir:              ║")
print("  ║   → Qual tipo ele deveria ser                        ║")
print("  ║   → Para quais tipos pode ser convertido             ║")
print("  ║                                                       ║")
print("  ║   Exemplos: 42, 3.14, ola, True, 100, Maria          ║")
print("  ║   Digite 'sair' para encerrar.                       ║")
print("  ╚═══════════════════════════════════════════════════════╝")
print()

while True:
    print("  ─" * 30)
    entrada = input("  ✏️  Digite um valor para testar: ").strip()

    # Verificar se quer sair
    if entrada.lower() == 'sair':
        print()
        print("  👋 Até a próxima! Continue praticando!")
        print()
        break

    # Verificar se digitou algo vazio
    if entrada == '':
        print("  ⚠️  Você não digitou nada! Tente novamente.")
        continue

    # Analisar o valor
    valor_real, tipo_ideal, explicacao = analisar_valor(entrada)

    # Testar conversões
    conversoes = testar_conversoes(valor_real)

    # Mostrar resultado
    mostrar_resultado(valor_real, tipo_ideal, explicacao, conversoes)
