import math
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from tkinter import messagebox, ttk
from typing import Dict, List, Optional, Sequence, Tuple


EPS_SIDE = 1e-6
EPS_ANGLE = 1e-3
EPS_ANGLE_SUM = 1e-2
ANIM_FRAMES = 20
ANIM_INTERVAL_MS = 16
AUTO_CALC_DELAY_MS = 320

Point = Tuple[float, float]


@dataclass
class TrianguloEntrada:
    lado1: float
    lado2: float
    lado3: float
    angulo1: float
    angulo2: float
    angulo3: float


@dataclass
class TrianguloAnalise:
    lados_validos: bool
    angulos_validos: bool
    msg_lados: str
    msg_angulos: str
    classificacao_lados: str = ""
    classificacao_angulos: str = ""
    classificacao_angulos_por_lados: str = ""
    consistencia: str = ""
    status_final: str = ""


def clamp(valor: float, minimo: float, maximo: float) -> float:
    return max(minimo, min(valor, maximo))


def cross2d(v1: Point, v2: Point) -> float:
    return v1[0] * v2[1] - v1[1] * v2[0]


def intersecao_retas(p: Point, d1: Point, q: Point, d2: Point) -> Optional[Point]:
    denom = cross2d(d1, d2)
    if math.isclose(denom, 0.0, abs_tol=1e-9):
        return None

    qp = (q[0] - p[0], q[1] - p[1])
    t = cross2d(qp, d2) / denom
    return (p[0] + t * d1[0], p[1] + t * d1[1])


def normalizar_pontos_para_canvas(
    pontos: Sequence[Point],
    largura_canvas: int,
    altura_canvas: int,
    margem: int = 30,
) -> List[Point]:
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    alcance_x = max(max_x - min_x, 1e-6)
    alcance_y = max(max_y - min_y, 1e-6)

    area_largura = largura_canvas - 2 * margem
    area_altura = altura_canvas - 2 * margem
    escala = min(area_largura / alcance_x, area_altura / alcance_y)

    desenho_largura = alcance_x * escala
    desenho_altura = alcance_y * escala
    offset_x = (largura_canvas - desenho_largura) / 2
    offset_y = (altura_canvas - desenho_altura) / 2

    pontos_canvas: List[Point] = []
    for ponto in pontos:
        x = (ponto[0] - min_x) * escala + offset_x
        y = (max_y - ponto[1]) * escala + offset_y
        pontos_canvas.append((x, y))

    return pontos_canvas


def classificar_lados(lado1: float, lado2: float, lado3: float) -> str:
    iguais_12 = math.isclose(lado1, lado2, abs_tol=EPS_SIDE)
    iguais_13 = math.isclose(lado1, lado3, abs_tol=EPS_SIDE)
    iguais_23 = math.isclose(lado2, lado3, abs_tol=EPS_SIDE)

    if iguais_12 and iguais_13:
        return "equilatero"
    if iguais_12 or iguais_13 or iguais_23:
        return "isosceles"
    return "escaleno"


def classificar_angulos(angulo1: float, angulo2: float, angulo3: float) -> str:
    angulos = [angulo1, angulo2, angulo3]
    if any(math.isclose(angulo, 90.0, abs_tol=EPS_ANGLE) for angulo in angulos):
        return "retangulo"
    if any(angulo > 90.0 + EPS_ANGLE for angulo in angulos):
        return "obtusangulo"
    return "acutangulo"


def classificar_angulos_por_lados(lado1: float, lado2: float, lado3: float) -> str:
    a, b, c = sorted([lado1, lado2, lado3])
    comparacao = c * c - (a * a + b * b)
    tolerancia = max(1e-3, 1e-4 * (a * a + b * b + c * c))

    if math.isclose(comparacao, 0.0, abs_tol=tolerancia):
        return "retangulo"
    if comparacao > 0:
        return "obtusangulo"
    return "acutangulo"


def triangulos(lado1: float, lado2: float, lado3: float) -> str:
    return classificar_lados(lado1, lado2, lado3)


def triangulos2(angulo1: float, angulo2: float, angulo3: float) -> str:
    return classificar_angulos(angulo1, angulo2, angulo3)


def validar_lados(lado1: float, lado2: float, lado3: float) -> Tuple[bool, str]:
    if lado1 <= 0 or lado2 <= 0 or lado3 <= 0:
        return False, "todos os lados devem ser maiores que zero"

    a, b, c = sorted([lado1, lado2, lado3])
    if a + b > c + EPS_SIDE:
        return True, "os lados formam um triangulo"

    return False, "os lados nao formam um triangulo"


def validar_angulos(angulo1: float, angulo2: float, angulo3: float) -> Tuple[bool, str]:
    angulos = [angulo1, angulo2, angulo3]

    if any(angulo <= 0 for angulo in angulos):
        return False, "todos os angulos devem ser maiores que zero"
    if any(angulo >= 180 for angulo in angulos):
        return False, "cada angulo deve ser menor que 180"

    soma = angulo1 + angulo2 + angulo3
    if math.isclose(soma, 180.0, abs_tol=EPS_ANGLE_SUM):
        return True, "os angulos formam um triangulo"

    return False, f"a soma dos angulos deve ser 180 (atual: {soma:.2f})"


def analisar_triangulo(entrada: TrianguloEntrada) -> TrianguloAnalise:
    lados_validos, msg_lados = validar_lados(entrada.lado1, entrada.lado2, entrada.lado3)
    angulos_validos, msg_angulos = validar_angulos(
        entrada.angulo1,
        entrada.angulo2,
        entrada.angulo3,
    )

    classificacao_lados = ""
    if lados_validos:
        classificacao_lados = classificar_lados(entrada.lado1, entrada.lado2, entrada.lado3)

    classificacao_angulos = ""
    if angulos_validos:
        classificacao_angulos = classificar_angulos(
            entrada.angulo1,
            entrada.angulo2,
            entrada.angulo3,
        )

    classificacao_angulos_por_lados = ""
    if lados_validos:
        classificacao_angulos_por_lados = classificar_angulos_por_lados(
            entrada.lado1,
            entrada.lado2,
            entrada.lado3,
        )

    consistencia = ""
    status_final = ""

    if lados_validos and angulos_validos:
        if classificacao_angulos == classificacao_angulos_por_lados:
            consistencia = "lados e angulos parecem coerentes"
            status_final = "triangulo valido e consistente"
        else:
            consistencia = (
                "lados e angulos sao validos separadamente, "
                "mas nao representam o mesmo triangulo"
            )
            status_final = "triangulo com dados inconsistentes"
    elif lados_validos or angulos_validos:
        status_final = "triangulo parcialmente valido"
    else:
        status_final = "triangulo invalido"

    return TrianguloAnalise(
        lados_validos=lados_validos,
        angulos_validos=angulos_validos,
        msg_lados=msg_lados,
        msg_angulos=msg_angulos,
        classificacao_lados=classificacao_lados,
        classificacao_angulos=classificacao_angulos,
        classificacao_angulos_por_lados=classificacao_angulos_por_lados,
        consistencia=consistencia,
        status_final=status_final,
    )


def pontos_por_lados(lado1: float, lado2: float, lado3: float) -> Tuple[List[Point], bool, str]:
    l1 = max(abs(lado1), 1.0)
    l2 = max(abs(lado2), 1.0)
    l3 = max(abs(lado3), 1.0)

    ponto_a = (0.0, 0.0)
    ponto_b = (l1, 0.0)
    x_c = (l1 * l1 + l3 * l3 - l2 * l2) / (2 * l1)
    y_quadrado = l3 * l3 - x_c * x_c

    lados_validos, _ = validar_lados(lado1, lado2, lado3)
    aproximado = (not lados_validos) or y_quadrado < 0

    if y_quadrado > 0:
        y_c = math.sqrt(y_quadrado)
    else:
        y_c = 0.0

    if aproximado:
        if y_c < 1e-6:
            y_c = max(l1, l2, l3) * 0.24
        x_c = clamp(x_c, l1 * 0.08, l1 * 0.92)
        legenda = "representacao aproximada por lados"
    else:
        legenda = "desenho em escala por lados"

    ponto_c = (x_c, y_c)
    return [ponto_a, ponto_b, ponto_c], aproximado, legenda


def pontos_por_angulos(
    angulo1: float,
    angulo2: float,
    angulo3: float,
) -> Tuple[List[Point], bool, str]:
    ponto_a = (0.0, 0.0)
    ponto_b = (1.0, 0.0)
    angulos_validos, _ = validar_angulos(angulo1, angulo2, angulo3)

    if angulos_validos:
        alpha = math.radians(angulo1)
        beta = math.radians(angulo2)

        direcao_a = (math.cos(alpha), math.sin(alpha))
        direcao_b = (-math.cos(beta), math.sin(beta))
        ponto_c = intersecao_retas(ponto_a, direcao_a, ponto_b, direcao_b)

        if ponto_c is not None and ponto_c[1] > EPS_SIDE:
            legenda = "triangulo construido pelos angulos"
            return [ponto_a, ponto_b, ponto_c], False, legenda

    a1 = max(abs(angulo1), 1.0)
    a2 = max(abs(angulo2), 1.0)
    a3 = max(abs(angulo3), 1.0)
    soma = a1 + a2 + a3

    x_c = clamp(0.15 + 0.70 * (a1 / soma), 0.08, 0.92)
    y_c = 0.24 + 1.00 * (a3 / soma)
    ponto_c = (x_c, y_c)

    legenda = "representacao aproximada por angulos"
    return [ponto_a, ponto_b, ponto_c], True, legenda


class TrianguloApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Triangulo Lab")
        self.root.geometry("1180x760")
        self.root.minsize(960, 620)
        self.root.configure(bg="#eaf1fb")

        self.campos: Dict[str, ttk.Entry] = {}
        self.presets = self._obter_presets()
        self.nome_campo = {
            "lado1": "o primeiro lado",
            "lado2": "o segundo lado",
            "lado3": "o terceiro lado",
            "angulo1": "o primeiro angulo",
            "angulo2": "o segundo angulo",
            "angulo3": "o terceiro angulo",
        }

        self.auto_calcular_var = tk.BooleanVar(value=True)
        self.animar_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Pronto. Preencha os campos e clique em Calcular.")
        self.preset_var = tk.StringVar()
        self.info_lados_var = tk.StringVar(value="Aguardando calculo por lados.")
        self.info_angulos_var = tk.StringVar(value="Aguardando calculo por angulos.")

        self._auto_calc_after_id: Optional[str] = None
        self._resize_after_ids: Dict[str, str] = {}
        self._animacao_after_ids: Dict[str, str] = {}
        self._cache_desenho: Dict[str, Dict[str, object]] = {}

        self._configurar_estilo()
        self._criar_layout()
        self.root.bind("<Return>", lambda _evento: self.calcular())
        self.root.bind("<Control-Return>", lambda _evento: self.calcular())
        self.root.bind("<Control-l>", lambda _evento: self.limpar())
        self.root.bind("<Control-e>", lambda _evento: self.carregar_exemplo())
        self.root.bind("<Control-c>", lambda _evento: self.copiar_resumo())
        self._atualizar_status("Atalhos: Enter calcula, Ctrl+L limpa, Ctrl+E exemplo, Ctrl+C copia resumo.")

    def _configurar_estilo(self) -> None:
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure(".", font=("DejaVu Sans", 10))
        style.configure("App.TFrame", background="#eaf1fb")
        style.configure(
            "Title.TLabel",
            background="#eaf1fb",
            foreground="#0f172a",
            font=("DejaVu Sans", 19, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#eaf1fb",
            foreground="#334155",
            font=("DejaVu Sans", 10),
        )
        style.configure("Card.TFrame", background="#f8fbff")
        style.configure("Card.TLabelframe", background="#f8fbff")
        style.configure(
            "Card.TLabelframe.Label",
            background="#f8fbff",
            foreground="#1e293b",
            font=("DejaVu Sans", 10, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background="#f8fbff",
            foreground="#475569",
            font=("DejaVu Sans", 9),
        )
        style.configure(
            "Section.TLabel",
            background="#f8fbff",
            foreground="#0f172a",
            font=("DejaVu Sans", 11, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background="#dfe8f5",
            foreground="#1f2937",
            font=("DejaVu Sans", 9),
        )
        style.configure("Accent.TButton", font=("DejaVu Sans", 10, "bold"))

    def _criar_layout(self) -> None:
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        container = ttk.Frame(self.root, style="App.TFrame", padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        header = ttk.Frame(container, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        ttk.Label(header, text="Triangulo Lab", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text=(
                "Valida, classifica e desenha triangulos por lados e por angulos. "
                "Animacao e interface responsiva para facilitar a leitura do resultado."
            ),
            style="Subtitle.TLabel",
        ).pack(anchor="w")

        painel_principal = ttk.Panedwindow(container, orient="horizontal")
        painel_principal.grid(row=1, column=0, sticky="nsew")

        coluna_esquerda = ttk.Frame(painel_principal, style="App.TFrame")
        coluna_esquerda.rowconfigure(1, weight=1)
        coluna_esquerda.columnconfigure(0, weight=1)
        painel_principal.add(coluna_esquerda, weight=1)

        coluna_direita = ttk.Frame(painel_principal, style="App.TFrame")
        coluna_direita.rowconfigure(0, weight=1)
        coluna_direita.columnconfigure(0, weight=1)
        painel_principal.add(coluna_direita, weight=2)

        painel_dados = ttk.LabelFrame(
            coluna_esquerda,
            text="Entradas",
            style="Card.TLabelframe",
            padding=12,
        )
        painel_dados.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        painel_resultado = ttk.LabelFrame(
            coluna_esquerda,
            text="Analise",
            style="Card.TLabelframe",
            padding=12,
        )
        painel_resultado.grid(row=1, column=0, sticky="nsew")
        painel_resultado.rowconfigure(0, weight=1)
        painel_resultado.columnconfigure(0, weight=1)

        painel_visual = ttk.LabelFrame(
            coluna_direita,
            text="Visualizacao",
            style="Card.TLabelframe",
            padding=12,
        )
        painel_visual.grid(row=0, column=0, sticky="nsew")
        painel_visual.columnconfigure(0, weight=1)
        painel_visual.rowconfigure(0, weight=1)
        painel_visual.rowconfigure(1, weight=1)

        self._criar_campos_entrada(painel_dados)
        self._criar_area_resultado(painel_resultado)
        self._criar_area_desenho(painel_visual)

        status = ttk.Label(
            container,
            textvariable=self.status_var,
            style="Status.TLabel",
            anchor="w",
            padding=(10, 6),
        )
        status.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    def _criar_campos_entrada(self, parent: ttk.LabelFrame) -> None:
        grupos = [
            (
                "Lados",
                [
                    ("lado1", "Primeiro lado", "u"),
                    ("lado2", "Segundo lado", "u"),
                    ("lado3", "Terceiro lado", "u"),
                ],
            ),
            (
                "Angulos",
                [
                    ("angulo1", "Primeiro angulo", "graus"),
                    ("angulo2", "Segundo angulo", "graus"),
                    ("angulo3", "Terceiro angulo", "graus"),
                ],
            ),
        ]

        linha = 0
        for titulo, definicoes in grupos:
            ttk.Label(parent, text=titulo, style="Section.TLabel").grid(
                row=linha,
                column=0,
                columnspan=3,
                sticky="w",
                pady=(0, 4),
            )
            linha += 1

            for chave, texto, unidade in definicoes:
                ttk.Label(parent, text=texto + ":", style="Muted.TLabel").grid(
                    row=linha,
                    column=0,
                    sticky="w",
                    padx=(0, 8),
                    pady=4,
                )
                entrada = ttk.Entry(parent, width=16)
                entrada.grid(row=linha, column=1, sticky="ew", pady=4)
                ttk.Label(parent, text=unidade, style="Muted.TLabel").grid(
                    row=linha,
                    column=2,
                    sticky="w",
                    padx=(8, 0),
                    pady=4,
                )
                entrada.bind("<KeyRelease>", self._ao_digitar)
                entrada.bind("<FocusOut>", self._ao_digitar)
                self.campos[chave] = entrada
                linha += 1

            linha += 1

        botoes = ttk.Frame(parent, style="Card.TFrame")
        botoes.grid(row=linha, column=0, columnspan=3, sticky="ew", pady=(4, 0))

        ttk.Button(botoes, text="Calcular", style="Accent.TButton", command=self.calcular).pack(
            side="left"
        )
        ttk.Button(botoes, text="Exemplo", command=self.carregar_exemplo).pack(side="left", padx=8)
        ttk.Button(botoes, text="Copiar resumo", command=self.copiar_resumo).pack(side="left", padx=8)
        ttk.Button(botoes, text="Limpar", command=self.limpar).pack(side="left")

        linha += 1
        preset_frame = ttk.Frame(parent, style="Card.TFrame")
        preset_frame.grid(row=linha, column=0, columnspan=3, sticky="ew", pady=(8, 0))

        ttk.Label(preset_frame, text="Preset:", style="Muted.TLabel").pack(side="left")
        self.combo_preset = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            state="readonly",
            width=33,
            values=list(self.presets.keys()),
        )
        self.combo_preset.pack(side="left", padx=(6, 6), fill="x", expand=True)
        if self.presets:
            primeiro = next(iter(self.presets.keys()))
            self.combo_preset.set(primeiro)

        ttk.Button(preset_frame, text="Aplicar", command=self.aplicar_preset).pack(side="left")

        linha += 1
        opcoes = ttk.Frame(parent, style="Card.TFrame")
        opcoes.grid(row=linha, column=0, columnspan=3, sticky="ew", pady=(8, 0))

        ttk.Checkbutton(
            opcoes,
            text="Auto calcular enquanto digita",
            variable=self.auto_calcular_var,
        ).pack(side="left")
        ttk.Checkbutton(opcoes, text="Animar desenho", variable=self.animar_var).pack(
            side="left", padx=(10, 0)
        )

        ttk.Label(
            parent,
            text="Dica: use virgula ou ponto para decimal.",
            style="Muted.TLabel",
        ).grid(row=linha + 1, column=0, columnspan=3, sticky="w", pady=(8, 0))

        parent.columnconfigure(1, weight=1)

    def _criar_area_resultado(self, parent: ttk.LabelFrame) -> None:
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        self.texto_resultado = tk.Text(
            parent,
            height=14,
            wrap="word",
            relief="flat",
            bg="#f8fafc",
            fg="#0f172a",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            padx=10,
            pady=8,
        )
        scroll = ttk.Scrollbar(parent, orient="vertical", command=self.texto_resultado.yview)
        self.texto_resultado.configure(yscrollcommand=scroll.set)

        self.texto_resultado.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        self._escrever_resultado("Informe os valores e clique em Calcular.")

    def _criar_area_desenho(self, parent: ttk.LabelFrame) -> None:
        frame_lados = ttk.LabelFrame(
            parent,
            text="Desenho por lados",
            style="Card.TLabelframe",
            padding=8,
        )
        frame_lados.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        frame_lados.columnconfigure(0, weight=1)
        frame_lados.rowconfigure(0, weight=1)

        self.canvas_lados = tk.Canvas(
            frame_lados,
            width=520,
            height=260,
            bg="#ffffff",
            highlightthickness=0,
        )
        self.canvas_lados.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            frame_lados,
            textvariable=self.info_lados_var,
            style="Muted.TLabel",
            wraplength=520,
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        frame_angulos = ttk.LabelFrame(
            parent,
            text="Desenho por angulos",
            style="Card.TLabelframe",
            padding=8,
        )
        frame_angulos.grid(row=1, column=0, sticky="nsew")
        frame_angulos.columnconfigure(0, weight=1)
        frame_angulos.rowconfigure(0, weight=1)

        self.canvas_angulos = tk.Canvas(
            frame_angulos,
            width=520,
            height=260,
            bg="#ffffff",
            highlightthickness=0,
        )
        self.canvas_angulos.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            frame_angulos,
            textvariable=self.info_angulos_var,
            style="Muted.TLabel",
            wraplength=520,
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.canvas_lados.bind("<Configure>", lambda _evento: self._agendar_redesenho("lados"))
        self.canvas_angulos.bind("<Configure>", lambda _evento: self._agendar_redesenho("angulos"))

        self._desenhar_texto_no_canvas(self.canvas_lados, "Aguardando dados dos lados")
        self._desenhar_texto_no_canvas(self.canvas_angulos, "Aguardando dados dos angulos")

    def _obter_presets(self) -> Dict[str, Dict[str, str]]:
        return {
            "3-4-5 retangulo": {
                "lado1": "3",
                "lado2": "4",
                "lado3": "5",
                "angulo1": "37",
                "angulo2": "53",
                "angulo3": "90",
            },
            "equilatero perfeito": {
                "lado1": "6",
                "lado2": "6",
                "lado3": "6",
                "angulo1": "60",
                "angulo2": "60",
                "angulo3": "60",
            },
            "dados inconsistentes": {
                "lado1": "3",
                "lado2": "4",
                "lado3": "5",
                "angulo1": "60",
                "angulo2": "60",
                "angulo3": "60",
            },
            "invalido proposital": {
                "lado1": "1",
                "lado2": "2",
                "lado3": "10",
                "angulo1": "20",
                "angulo2": "20",
                "angulo3": "20",
            },
        }

    def _atualizar_status(self, mensagem: str) -> None:
        horario = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"[{horario}] {mensagem}")

    def _escrever_resultado(self, mensagem: str) -> None:
        self.texto_resultado.config(state="normal")
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, mensagem)
        self.texto_resultado.config(state="disabled")

    def _ler_float(self, chave: str) -> float:
        texto = self.campos[chave].get().strip().replace(",", ".")
        if not texto:
            raise ValueError(f"Preencha {self.nome_campo[chave]}.")

        try:
            return float(texto)
        except ValueError as erro:
            raise ValueError(f"Valor invalido em {self.nome_campo[chave]}.") from erro

    def _coletar_entrada(self) -> TrianguloEntrada:
        return TrianguloEntrada(
            lado1=self._ler_float("lado1"),
            lado2=self._ler_float("lado2"),
            lado3=self._ler_float("lado3"),
            angulo1=self._ler_float("angulo1"),
            angulo2=self._ler_float("angulo2"),
            angulo3=self._ler_float("angulo3"),
        )

    def _montar_relatorio(self, analise: TrianguloAnalise) -> str:
        linhas = [
            "RESUMO DA ANALISE",
            "",
            f"Lados: {analise.msg_lados}",
            f"Angulos: {analise.msg_angulos}",
        ]

        if analise.classificacao_lados:
            linhas.append(f"Classificacao por lados: {analise.classificacao_lados}")

        if analise.classificacao_angulos:
            linhas.append(f"Classificacao por angulos informados: {analise.classificacao_angulos}")

        if analise.classificacao_angulos_por_lados:
            linhas.append(
                "Classificacao angular inferida pelos lados: "
                f"{analise.classificacao_angulos_por_lados}"
            )

        if analise.consistencia:
            linhas.append(f"Consistencia: {analise.consistencia}")

        linhas.append("")
        linhas.append(f"STATUS FINAL: {analise.status_final}")
        return "\n".join(linhas)

    def _desenhar_texto_no_canvas(self, canvas: tk.Canvas, texto: str) -> None:
        canvas.delete("all")
        largura = max(int(canvas.winfo_width()), 120)
        altura = max(int(canvas.winfo_height()), 80)
        canvas.create_rectangle(4, 4, largura - 4, altura - 4, outline="#e2e8f0", width=1)
        self._desenhar_grade_fundo(canvas, largura, altura)
        canvas.create_text(
            largura / 2,
            altura / 2,
            text=texto,
            fill="#64748b",
            font=("DejaVu Sans", 10),
        )

    def _desenhar_grade_fundo(self, canvas: tk.Canvas, largura: int, altura: int) -> None:
        passo = 24
        for x in range(passo, largura, passo):
            cor = "#f4f7fb" if x % (passo * 4) else "#edf2f7"
            canvas.create_line(x, 0, x, altura, fill=cor)
        for y in range(passo, altura, passo):
            cor = "#f4f7fb" if y % (passo * 4) else "#edf2f7"
            canvas.create_line(0, y, largura, y, fill=cor)

    def _obter_cores_desenho(self, aproximado: bool) -> Tuple[str, str, Optional[Tuple[int, int]]]:
        if aproximado:
            return "#b91c1c", "#fee2e2", (7, 4)
        return "#166534", "#dcfce7", None

    def _registrar_e_desenhar(
        self,
        chave: str,
        canvas: tk.Canvas,
        pontos: Sequence[Point],
        aproximado: bool,
        titulo: str,
        subtitulo: str,
        info_extra: str,
        animar: bool,
    ) -> None:
        self._cache_desenho[chave] = {
            "canvas": canvas,
            "pontos": list(pontos),
            "aproximado": aproximado,
            "titulo": titulo,
            "subtitulo": subtitulo,
            "info_extra": info_extra,
        }

        if animar:
            self._animar_desenho(chave)
        else:
            self._renderizar_desenho(chave, progresso=1.0)

    def _renderizar_desenho(self, chave: str, progresso: float = 1.0) -> None:
        if chave not in self._cache_desenho:
            return

        item = self._cache_desenho[chave]
        canvas: tk.Canvas = item["canvas"]  # type: ignore[assignment]
        pontos: Sequence[Point] = item["pontos"]  # type: ignore[assignment]
        aproximado: bool = bool(item["aproximado"])
        titulo: str = str(item["titulo"])
        subtitulo: str = str(item["subtitulo"])
        info_extra: str = str(item["info_extra"])

        progresso = clamp(progresso, 0.0, 1.0)
        largura = max(int(canvas.winfo_width()), 120)
        altura = max(int(canvas.winfo_height()), 80)

        canvas.delete("all")
        canvas.create_rectangle(4, 4, largura - 4, altura - 4, outline="#e2e8f0", width=1)
        self._desenhar_grade_fundo(canvas, largura, altura)

        pontos_canvas = normalizar_pontos_para_canvas(pontos, largura, altura, margem=34)
        centro_x = sum(x for x, _ in pontos_canvas) / 3
        centro_y = sum(y for _, y in pontos_canvas) / 3

        pontos_animados: List[Point] = []
        for x, y in pontos_canvas:
            x_anim = centro_x + (x - centro_x) * progresso
            y_anim = centro_y + (y - centro_y) * progresso
            pontos_animados.append((x_anim, y_anim))

        (ax, ay), (bx, by), (cx, cy) = pontos_animados
        cor_borda, cor_fundo, dash = self._obter_cores_desenho(aproximado)

        canvas.create_polygon(
            ax + 2,
            ay + 2,
            bx + 2,
            by + 2,
            cx + 2,
            cy + 2,
            fill="#e2e8f0",
            outline="",
        )
        canvas.create_polygon(
            ax,
            ay,
            bx,
            by,
            cx,
            cy,
            fill=cor_fundo,
            outline=cor_borda,
            width=2,
            dash=dash,
        )
        canvas.create_line(ax, ay, bx, by, fill=cor_borda, width=2, dash=dash)
        canvas.create_line(bx, by, cx, cy, fill=cor_borda, width=2, dash=dash)
        canvas.create_line(cx, cy, ax, ay, fill=cor_borda, width=2, dash=dash)

        for nome, x, y in (("A", ax, ay), ("B", bx, by), ("C", cx, cy)):
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="#ffffff", outline=cor_borda)
            canvas.create_text(x, y, text=nome, fill=cor_borda, font=("DejaVu Sans", 9, "bold"))

        canvas.create_text(
            12,
            12,
            anchor="nw",
            text=info_extra,
            fill="#334155",
            font=("DejaVu Sans Mono", 9),
        )
        canvas.create_text(
            largura / 2,
            altura - 24,
            text=titulo,
            fill="#0f172a",
            font=("DejaVu Sans", 10, "bold"),
        )
        canvas.create_text(
            largura / 2,
            altura - 10,
            text=subtitulo,
            fill=cor_borda,
            font=("DejaVu Sans", 9),
        )

    def _cancelar_animacao(self, chave: str) -> None:
        after_id = self._animacao_after_ids.pop(chave, None)
        if after_id:
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass

    def _animar_desenho(self, chave: str) -> None:
        self._cancelar_animacao(chave)

        def passo(frame: int) -> None:
            progresso_linear = frame / ANIM_FRAMES
            progresso_suave = 1.0 - (1.0 - progresso_linear) ** 3
            self._renderizar_desenho(chave, progresso=progresso_suave)

            if frame < ANIM_FRAMES:
                after_id = self.root.after(ANIM_INTERVAL_MS, passo, frame + 1)
                self._animacao_after_ids[chave] = after_id
            else:
                self._animacao_after_ids.pop(chave, None)

        passo(0)

    def _agendar_redesenho(self, chave: str) -> None:
        anterior = self._resize_after_ids.pop(chave, None)
        if anterior:
            try:
                self.root.after_cancel(anterior)
            except tk.TclError:
                pass

        after_id = self.root.after(90, lambda: self._redesenhar_cache(chave))
        self._resize_after_ids[chave] = after_id

    def _redesenhar_cache(self, chave: str) -> None:
        self._resize_after_ids.pop(chave, None)
        if chave in self._cache_desenho:
            self._renderizar_desenho(chave, progresso=1.0)

    def _ao_digitar(self, _evento=None) -> None:
        if not self.auto_calcular_var.get():
            return

        if self._auto_calc_after_id:
            try:
                self.root.after_cancel(self._auto_calc_after_id)
            except tk.TclError:
                pass

        self._auto_calc_after_id = self.root.after(
            AUTO_CALC_DELAY_MS,
            lambda: self.calcular(mostrar_erros=False, origem_auto=True),
        )

    def calcular(self, mostrar_erros: bool = True, origem_auto: bool = False) -> bool:
        if self._auto_calc_after_id:
            try:
                self.root.after_cancel(self._auto_calc_after_id)
            except tk.TclError:
                pass
            self._auto_calc_after_id = None

        try:
            entrada = self._coletar_entrada()
        except ValueError as erro:
            if mostrar_erros:
                messagebox.showerror("Entrada invalida", str(erro))
            self._atualizar_status(str(erro))
            return False

        analise = analisar_triangulo(entrada)
        self._escrever_resultado(self._montar_relatorio(analise))

        pontos_lados, aprox_lados, legenda_lados = pontos_por_lados(
            entrada.lado1,
            entrada.lado2,
            entrada.lado3,
        )
        info_lados = (
            f"l1={entrada.lado1:.2f}  l2={entrada.lado2:.2f}  l3={entrada.lado3:.2f}"
        )
        self._registrar_e_desenhar(
            "lados",
            self.canvas_lados,
            pontos_lados,
            aprox_lados,
            "Construcao por lados",
            legenda_lados,
            info_lados,
            animar=self.animar_var.get() and not origem_auto,
        )

        if aprox_lados:
            self.info_lados_var.set(
                "Desenho por lados em modo aproximado: os valores nao fecham um triangulo real."
            )
        else:
            self.info_lados_var.set("Desenho por lados em escala real.")

        pontos_angulos, aprox_angulos, legenda_angulos = pontos_por_angulos(
            entrada.angulo1,
            entrada.angulo2,
            entrada.angulo3,
        )
        info_angulos = (
            f"a1={entrada.angulo1:.2f}g  a2={entrada.angulo2:.2f}g  a3={entrada.angulo3:.2f}g"
        )
        self._registrar_e_desenhar(
            "angulos",
            self.canvas_angulos,
            pontos_angulos,
            aprox_angulos,
            "Construcao por angulos",
            legenda_angulos,
            info_angulos,
            animar=self.animar_var.get() and not origem_auto,
        )

        if aprox_angulos:
            self.info_angulos_var.set(
                "Desenho por angulos em modo aproximado: a soma deve ser 180 para construir o triangulo real."
            )
        else:
            self.info_angulos_var.set("Desenho por angulos valido: forma definida pelos tres angulos.")

        if origem_auto:
            self._atualizar_status("Calculo atualizado automaticamente.")
        else:
            self._atualizar_status("Calculo concluido com sucesso.")
        return True

    def aplicar_preset(self) -> None:
        nome = self.preset_var.get().strip()
        if not nome or nome not in self.presets:
            self._atualizar_status("Selecione um preset valido.")
            return

        for chave, valor in self.presets[nome].items():
            self.campos[chave].delete(0, tk.END)
            self.campos[chave].insert(0, valor)

        self._atualizar_status(f"Preset aplicado: {nome}.")
        self.calcular(mostrar_erros=False)

    def carregar_exemplo(self) -> None:
        self.preset_var.set("3-4-5 retangulo")
        self.aplicar_preset()

    def copiar_resumo(self) -> None:
        texto = self.texto_resultado.get("1.0", tk.END).strip()
        if not texto:
            self._atualizar_status("Nao ha resumo para copiar.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        self._atualizar_status("Resumo copiado para a area de transferencia.")

    def limpar(self) -> None:
        for campo in self.campos.values():
            campo.delete(0, tk.END)

        self._cache_desenho.clear()
        self.info_lados_var.set("Aguardando calculo por lados.")
        self.info_angulos_var.set("Aguardando calculo por angulos.")
        self._escrever_resultado("Informe os valores e clique em Calcular.")
        self._desenhar_texto_no_canvas(self.canvas_lados, "Aguardando dados dos lados")
        self._desenhar_texto_no_canvas(self.canvas_angulos, "Aguardando dados dos angulos")
        self._atualizar_status("Campos limpos.")


if __name__ == "__main__":
    app_root = tk.Tk()
    TrianguloApp(app_root)
    app_root.mainloop()
