"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                    ATIVIDADE - TIPOS DE VARIÁVEIS EM PYTHON                          ║
╠════════════════╦════════╦══════════╦════════════╦══════════╦═══════════╗             ║
║  Declaração    ║  Tipo  ║ int(x)?  ║  float(x)? ║  str(x)? ║  bool(x)? ║             ║
╠════════════════╬════════╬══════════╬════════════╬══════════╬═══════════╣             ║
║  x = 4        ║  int   ║   Sim    ║    Sim     ║   Sim    ║    Sim    ║              ║
║  x = '3'      ║  str   ║   Sim    ║    Sim     ║   Sim    ║    Sim    ║              
║  x = 'ola'    ║  str   ║   Não    ║    Não     ║   Sim    ║    Sim    ║              ║
║  x = 3.14     ║  float ║   Sim    ║    Sim     ║   Sim    ║    Sim    ║              ║
║  x = '3.14'   ║  str   ║   Não    ║    Sim     ║   Sim    ║    Sim    ║              ║
║  x = True     ║  bool  ║   Sim    ║    Sim     ║   Sim    ║    Sim    ║              ║
╚════════════════╩════════╩══════════╩════════════╩══════════╩═══════════╝             ║
╚══════════════════════════════════════════════════════════════════════════════════════╝





































EXPLICAÇÃO DAS CORREÇÕES:
─────────────────────────

1) x = 4       (int)   → int(4)=4 ✔ | float(4)=4.0 ✔ | str(4)='4' ✔ | bool(4)=True ✔

2) x = '3'     (str)   → int('3')=3 ✔ | float('3')=3.0 ✔ | str('3')='3' ✔ | bool('3')=True ✔
   ⚠ CORREÇÃO: '3' PODE ser convertido para int e float, pois é uma string numérica válida!

3) x = 'ola'   (str)   → int('ola')=ERRO ✘ | float('ola')=ERRO ✘ | str('ola')='ola' ✔ | bool('ola')=True ✔
   ⚠ CORREÇÃO: bool('ola') = True (qualquer string não vazia é True)

4) x = 3.14    (float) → int(3.14)=3 ✔ | float(3.14)=3.14 ✔ | str(3.14)='3.14' ✔ | bool(3.14)=True ✔
   ⚠ CORREÇÃO: int(3.14) funciona! Apenas trunca o decimal (vira 3).
              str(3.14) também funciona! E bool(3.14) = True.

5) x = '3.14'  (str)   → int('3.14')=ERRO ✘ | float('3.14')=3.14 ✔ | str('3.14')='3.14' ✔ | bool('3.14')=True ✔
   ⚠ CORREÇÃO: float('3.14') FUNCIONA! E bool('3.14') = True.

6) x = True    (bool)  → int(True)=1 ✔ | float(True)=1.0 ✔ | str(True)='True' ✔ | bool(True)=True ✔
   ⚠ CORREÇÃO: O correto é "True" (com T maiúsculo). "true" dá erro!
              int(True)=1, float(True)=1.0, str(True)='True' — TUDO funciona!

REGRA GERAL:
────────────
• str(x)  → SEMPRE funciona com qualquer tipo
• bool(x) → SEMPRE funciona com qualquer tipo
• int(x)  → Funciona com: int, float, bool, e strings que contenham apenas números inteiros
• float(x)→ Funciona com: int, float, bool, e strings que contenham números válidos
"""

# ╔═══════════════════════════════════════════════════════════════╗
# ║          🧪 TESTES PRÁTICOS - TIPOS DE VARIÁVEIS             ║
# ╚═══════════════════════════════════════════════════════════════╝

# ──────────────────────────────────────────────────────────────
# 📌 TESTE 1: Descobrindo o tipo de cada variável com type()
# ──────────────────────────────────────────────────────────────
print("=" * 60)
print("  TESTE 1: Qual é o tipo de cada variável?")
print("=" * 60)

a = 4
b = '3'
c = 'ola'
d = 3.14
e = '3.14'
f = True

# type() revela o tipo original da variável
print(f"  a = 4       → tipo: {type(a).__name__}")    # int
print(f"  b = '3'     → tipo: {type(b).__name__}")    # str
print(f"  c = 'ola'   → tipo: {type(c).__name__}")    # str
print(f"  d = 3.14    → tipo: {type(d).__name__}")    # float
print(f"  e = '3.14'  → tipo: {type(e).__name__}")    # str
print(f"  f = True    → tipo: {type(f).__name__}")    # bool

# ──────────────────────────────────────────────────────────────
# 📌 TESTE 2: Tentando converter para INT
# Explicação: int() transforma o valor em número inteiro.
#   - float vira int (corta as casas decimais)
#   - string só funciona se tiver APENAS dígitos (ex: '3')
#   - bool funciona: True=1, False=0
# ──────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  TESTE 2: Convertendo para INT")
print("=" * 60)

# Função auxiliar que tenta converter e mostra o resultado ou o erro
def tentar_converter(valor, tipo_destino):
    """Tenta converter 'valor' para 'tipo_destino' e mostra o resultado."""
    try:
        resultado = tipo_destino(valor)
        return f"✅ {tipo_destino.__name__}({repr(valor):>10}) = {repr(resultado)}"
    except (ValueError, TypeError) as erro:
        return f"❌ {tipo_destino.__name__}({repr(valor):>10}) = ERRO! ({type(erro).__name__})"

valores = [4, '3', 'ola', 3.14, '3.14', True, False]

for v in valores:
    print(f"  {tentar_converter(v, int)}")

# ──────────────────────────────────────────────────────────────
# 📌 TESTE 3: Tentando converter para FLOAT
# Explicação: float() transforma o valor em número decimal.
#   - int vira float (adiciona .0)
#   - string funciona se tiver número válido (ex: '3', '3.14')
#   - bool funciona: True=1.0, False=0.0
# ──────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  TESTE 3: Convertendo para FLOAT")
print("=" * 60)

for v in valores:
    print(f"  {tentar_converter(v, float)}")

# ──────────────────────────────────────────────────────────────
# 📌 TESTE 4: Tentando converter para STR
# Explicação: str() SEMPRE funciona! Transforma qualquer coisa
# em texto. Nunca dá erro.
# ──────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  TESTE 4: Convertendo para STR (sempre funciona!)")
print("=" * 60)

for v in valores:
    print(f"  {tentar_converter(v, str)}")

# ──────────────────────────────────────────────────────────────
# 📌 TESTE 5: Tentando converter para BOOL
# Explicação: bool() SEMPRE funciona! Regras:
#   - Números: 0 e 0.0 = False, qualquer outro = True
#   - Strings: '' (vazia) = False, qualquer outra = True
#   - None = False
# ──────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  TESTE 5: Convertendo para BOOL (sempre funciona!)")
print("=" * 60)

valores_bool = [4, 0, '3', '', 'ola', 3.14, 0.0, True, False, None]

for v in valores_bool:
    resultado = bool(v)
    emoji = "🟢" if resultado else "🔴"
    print(f"  {emoji} bool({repr(v):>10}) = {resultado}")

# ──────────────────────────────────────────────────────────────
# 📌 TESTE 6: Curiosidades e pegadinhas!
# ──────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  TESTE 6: 🤔 Curiosidades e Pegadinhas!")
print("=" * 60)

# 🔹 Pegadinha 1: True e False são números disfarçados!
print()
print("  🔹 True e False são números disfarçados:")
print(f"     True + True   = {True + True}")      # 2 (porque True = 1)
print(f"     True + False  = {True + False}")      # 1
print(f"     True * 10     = {True * 10}")          # 10
print(f"     False * 100   = {False * 100}")        # 0

# 🔹 Pegadinha 2: String vazia vs string com espaço
print()
print("  🔹 String vazia vs string com espaço:")
print(f"     bool('')      = {bool('')}")          # False (vazia)
print(f"     bool(' ')     = {bool(' ')}")          # True  (tem espaço!)
print(f"     bool('0')     = {bool('0')}")          # True  (não é o número 0!)

# 🔹 Pegadinha 3: int() trunca, não arredonda!
print()
print("  🔹 int() trunca, NÃO arredonda:")
print(f"     int(3.14)     = {int(3.14)}")         # 3 (cortou)
print(f"     int(3.99)     = {int(3.99)}")         # 3 (cortou, não arredondou!)
print(f"     int(-3.7)     = {int(-3.7)}")         # -3 (cortou em direção ao zero)

# 🔹 Pegadinha 4: type() vs isinstance()
print()
print("  🔹 Checando tipos com isinstance():")
x = 42
print(f"     x = 42")
print(f"     isinstance(x, int)   = {isinstance(x, int)}")    # True
print(f"     isinstance(x, float) = {isinstance(x, float)}")  # False
print(f"     isinstance(x, str)   = {isinstance(x, str)}")    # False

# ──────────────────────────────────────────────────────────────
# 📌 RESUMO FINAL
# ──────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("  📋 RESUMO FINAL - TABELA DE CONVERSÕES")
print("=" * 60)
print()
print("  Valor       │ int()  │ float() │ str()  │ bool()")
print("  ────────────┼────────┼─────────┼────────┼───────")
print("  4           │  ✅    │   ✅    │  ✅    │  ✅")
print("  '3'         │  ✅    │   ✅    │  ✅    │  ✅")
print("  'ola'       │  ❌    │   ❌    │  ✅    │  ✅")
print("  3.14        │  ✅    │   ✅    │  ✅    │  ✅")
print("  '3.14'      │  ❌    │   ✅    │  ✅    │  ✅")
print("  True        │  ✅    │   ✅    │  ✅    │  ✅")
print("  0           │  ✅    │   ✅    │  ✅    │  🔴 False!")
print("  ''          │  ❌    │   ❌    │  ✅    │  🔴 False!")
print()
print("  💡 DICA: str() e bool() NUNCA dão erro!")
print("  💡 DICA: int() não aceita strings com ponto ('3.14')")
print("  💡 DICA: float() aceita qualquer string numérica")