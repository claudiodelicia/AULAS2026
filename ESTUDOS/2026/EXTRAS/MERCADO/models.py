import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mercado.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL DEFAULT 0,
            imagem_url TEXT,
            categoria_id INTEGER,
            ativo INTEGER NOT NULL DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );

        CREATE TABLE IF NOT EXISTS usuarios_admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        );
    """)

    # Inserir categorias padrão se não existirem
    categorias_padrao = [
        "Frutas e Verduras", "Laticínios", "Carnes", "Bebidas",
        "Padaria", "Limpeza", "Higiene", "Mercearia", "Congelados", "Outros"
    ]
    for cat in categorias_padrao:
        cursor.execute(
            "INSERT OR IGNORE INTO categorias (nome) VALUES (?)", (cat,)
        )

    # Criar admin padrão (usuario: admin, senha: admin123)
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios_admin (usuario, senha) VALUES (?, ?)",
        ("admin", "admin123")
    )

    # Inserir alguns produtos de exemplo se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        produtos_exemplo = [
            ("Banana Prata (kg)", "Banana prata fresca", 5.99, 100, "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=300", 1),
            ("Leite Integral 1L", "Leite integral longa vida", 6.49, 80, "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300", 2),
            ("Peito de Frango (kg)", "Peito de frango resfriado", 17.90, 50, "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=300", 3),
            ("Refrigerante Cola 2L", "Refrigerante sabor cola", 8.99, 60, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300", 4),
            ("Pão Francês (kg)", "Pão francês quentinho", 12.90, 40, "https://images.unsplash.com/photo-1549931319-a545753d62ce?w=300", 5),
            ("Detergente 500ml", "Detergente líquido neutro", 2.99, 120, "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300", 6),
            ("Sabonete 90g", "Sabonete em barra perfumado", 1.99, 200, "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=300", 7),
            ("Arroz 5kg", "Arroz branco tipo 1", 27.90, 70, "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300", 8),
            ("Feijão Preto 1kg", "Feijão preto selecionado", 8.49, 90, "https://images.unsplash.com/photo-1551462147-ff29053bfc14?w=300", 8),
            ("Pizza Congelada", "Pizza mussarela congelada", 15.90, 30, "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=300", 9),
            ("Maçã Gala (kg)", "Maçã gala nacional", 9.90, 60, "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=300", 1),
            ("Queijo Mussarela (kg)", "Queijo mussarela fatiado", 39.90, 25, "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=300", 2),
        ]
        cursor.executemany(
            "INSERT INTO produtos (nome, descricao, preco, estoque, imagem_url, categoria_id) VALUES (?, ?, ?, ?, ?, ?)",
            produtos_exemplo
        )

    conn.commit()
    conn.close()


# ---- Funções CRUD para Produtos ----

def listar_produtos(categoria_id=None, busca=None):
    conn = get_db()
    query = """
        SELECT p.*, c.nome as categoria_nome
        FROM produtos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.ativo = 1
    """
    params = []
    if categoria_id:
        query += " AND p.categoria_id = ?"
        params.append(categoria_id)
    if busca:
        query += " AND (p.nome LIKE ? OR p.descricao LIKE ?)"
        params.extend([f"%{busca}%", f"%{busca}%"])
    query += " ORDER BY p.nome"
    produtos = conn.execute(query, params).fetchall()
    conn.close()
    return produtos


def obter_produto(produto_id):
    conn = get_db()
    produto = conn.execute(
        "SELECT p.*, c.nome as categoria_nome FROM produtos p LEFT JOIN categorias c ON p.categoria_id = c.id WHERE p.id = ?",
        (produto_id,)
    ).fetchone()
    conn.close()
    return produto


def criar_produto(nome, descricao, preco, estoque, imagem_url, categoria_id):
    conn = get_db()
    conn.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, imagem_url, categoria_id) VALUES (?, ?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, imagem_url, categoria_id)
    )
    conn.commit()
    conn.close()


def atualizar_produto(produto_id, nome, descricao, preco, estoque, imagem_url, categoria_id):
    conn = get_db()
    conn.execute(
        "UPDATE produtos SET nome=?, descricao=?, preco=?, estoque=?, imagem_url=?, categoria_id=? WHERE id=?",
        (nome, descricao, preco, estoque, imagem_url, categoria_id, produto_id)
    )
    conn.commit()
    conn.close()


def deletar_produto(produto_id):
    conn = get_db()
    conn.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()


# ---- Funções para Categorias ----

def listar_categorias():
    conn = get_db()
    categorias = conn.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
    conn.close()
    return categorias


# ---- Funções para Pedidos ----

def criar_pedido(cliente_nome, cliente_email, itens_carrinho):
    """itens_carrinho = [{"produto_id": int, "quantidade": int}, ...]"""
    conn = get_db()
    cursor = conn.cursor()

    # Criar ou obter cliente
    cliente = cursor.execute("SELECT id FROM clientes WHERE email = ?", (cliente_email,)).fetchone()
    if cliente:
        cliente_id = cliente["id"]
    else:
        cursor.execute(
            "INSERT INTO clientes (nome, email, senha) VALUES (?, ?, ?)",
            (cliente_nome, cliente_email, "")
        )
        cliente_id = cursor.lastrowid

    # Calcular total e criar pedido
    total = 0
    itens_detalhes = []
    for item in itens_carrinho:
        produto = cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],)).fetchone()
        if produto and produto["estoque"] >= item["quantidade"]:
            subtotal = produto["preco"] * item["quantidade"]
            total += subtotal
            itens_detalhes.append({
                "produto_id": produto["id"],
                "quantidade": item["quantidade"],
                "preco_unitario": produto["preco"]
            })
            # Atualizar estoque
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], produto["id"])
            )

    cursor.execute(
        "INSERT INTO pedidos (cliente_id, total, status) VALUES (?, ?, ?)",
        (cliente_id, total, "pendente")
    )
    pedido_id = cursor.lastrowid

    for detalhe in itens_detalhes:
        cursor.execute(
            "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
            (pedido_id, detalhe["produto_id"], detalhe["quantidade"], detalhe["preco_unitario"])
        )

    conn.commit()
    conn.close()
    return pedido_id


def listar_pedidos():
    conn = get_db()
    pedidos = conn.execute("""
        SELECT p.*, c.nome as cliente_nome, c.email as cliente_email
        FROM pedidos p
        LEFT JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.criado_em DESC
    """).fetchall()
    conn.close()
    return pedidos


def obter_pedido_detalhes(pedido_id):
    conn = get_db()
    pedido = conn.execute("""
        SELECT p.*, c.nome as cliente_nome, c.email as cliente_email
        FROM pedidos p
        LEFT JOIN clientes c ON p.cliente_id = c.id
        WHERE p.id = ?
    """, (pedido_id,)).fetchone()

    itens = conn.execute("""
        SELECT ip.*, pr.nome as produto_nome
        FROM itens_pedido ip
        JOIN produtos pr ON ip.produto_id = pr.id
        WHERE ip.pedido_id = ?
    """, (pedido_id,)).fetchall()

    conn.close()
    return pedido, itens


def atualizar_status_pedido(pedido_id, status):
    conn = get_db()
    conn.execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id))
    conn.commit()
    conn.close()


# ---- Admin ----

def verificar_admin(usuario, senha):
    conn = get_db()
    admin = conn.execute(
        "SELECT * FROM usuarios_admin WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    ).fetchone()
    conn.close()
    return admin is not None
