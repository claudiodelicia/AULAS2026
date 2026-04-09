from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import (
    init_db, listar_produtos, obter_produto, criar_produto,
    atualizar_produto, deletar_produto, listar_categorias,
    criar_pedido, listar_pedidos, obter_pedido_detalhes,
    atualizar_status_pedido, verificar_admin
)

app = Flask(__name__)
app.secret_key = "mercado_olsen_secret_key_2026"

# Inicializar banco de dados
init_db()


# ===================== SITE DO MERCADO (CLIENTE) =====================

@app.route("/")
def index():
    categoria_id = request.args.get("categoria", type=int)
    busca = request.args.get("busca", "")
    produtos = listar_produtos(categoria_id=categoria_id, busca=busca)
    categorias = listar_categorias()
    return render_template(
        "index.html",
        produtos=produtos,
        categorias=categorias,
        categoria_selecionada=categoria_id,
        busca=busca
    )


@app.route("/produto/<int:produto_id>")
def detalhe_produto(produto_id):
    produto = obter_produto(produto_id)
    if not produto:
        flash("Produto não encontrado.", "error")
        return redirect(url_for("index"))
    return render_template("produto_detalhe.html", produto=produto)


# ===================== CARRINHO DE COMPRAS =====================

@app.route("/carrinho")
def ver_carrinho():
    carrinho = session.get("carrinho", {})
    itens = []
    total = 0
    for prod_id, qtd in carrinho.items():
        produto = obter_produto(int(prod_id))
        if produto:
            subtotal = produto["preco"] * qtd
            total += subtotal
            itens.append({
                "produto": produto,
                "quantidade": qtd,
                "subtotal": subtotal
            })
    return render_template("carrinho.html", itens=itens, total=total)


@app.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
def adicionar_carrinho(produto_id):
    quantidade = request.form.get("quantidade", 1, type=int)
    carrinho = session.get("carrinho", {})
    prod_key = str(produto_id)

    if prod_key in carrinho:
        carrinho[prod_key] += quantidade
    else:
        carrinho[prod_key] = quantidade

    session["carrinho"] = carrinho
    flash("Produto adicionado ao carrinho!", "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/carrinho/remover/<int:produto_id>", methods=["POST"])
def remover_carrinho(produto_id):
    carrinho = session.get("carrinho", {})
    prod_key = str(produto_id)
    if prod_key in carrinho:
        del carrinho[prod_key]
    session["carrinho"] = carrinho
    flash("Produto removido do carrinho.", "info")
    return redirect(url_for("ver_carrinho"))


@app.route("/carrinho/atualizar/<int:produto_id>", methods=["POST"])
def atualizar_carrinho(produto_id):
    quantidade = request.form.get("quantidade", 1, type=int)
    carrinho = session.get("carrinho", {})
    prod_key = str(produto_id)
    if quantidade > 0:
        carrinho[prod_key] = quantidade
    else:
        carrinho.pop(prod_key, None)
    session["carrinho"] = carrinho
    return redirect(url_for("ver_carrinho"))


@app.route("/carrinho/quantidade")
def carrinho_quantidade():
    carrinho = session.get("carrinho", {})
    total = sum(carrinho.values())
    return jsonify({"quantidade": total})


# ===================== FINALIZAR PEDIDO =====================

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    carrinho = session.get("carrinho", {})
    if not carrinho:
        flash("Seu carrinho está vazio!", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not email:
            flash("Preencha todos os campos.", "error")
            return redirect(url_for("checkout"))

        itens = []
        for prod_id, qtd in carrinho.items():
            itens.append({"produto_id": int(prod_id), "quantidade": qtd})

        pedido_id = criar_pedido(nome, email, itens)
        session["carrinho"] = {}
        flash(f"Pedido #{pedido_id} realizado com sucesso!", "success")
        return redirect(url_for("pedido_confirmado", pedido_id=pedido_id))

    # GET - mostrar formulário
    itens = []
    total = 0
    for prod_id, qtd in carrinho.items():
        produto = obter_produto(int(prod_id))
        if produto:
            subtotal = produto["preco"] * qtd
            total += subtotal
            itens.append({"produto": produto, "quantidade": qtd, "subtotal": subtotal})

    return render_template("checkout.html", itens=itens, total=total)


@app.route("/pedido/<int:pedido_id>")
def pedido_confirmado(pedido_id):
    pedido, itens = obter_pedido_detalhes(pedido_id)
    if not pedido:
        flash("Pedido não encontrado.", "error")
        return redirect(url_for("index"))
    return render_template("pedido_confirmado.html", pedido=pedido, itens=itens)


# ===================== PAINEL ADMIN =====================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")
        if verificar_admin(usuario, senha):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Usuário ou senha inválidos.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    produtos = listar_produtos()
    pedidos = listar_pedidos()
    return render_template("admin/dashboard.html", produtos=produtos, pedidos=pedidos)


@app.route("/admin/produto/novo", methods=["GET", "POST"])
def admin_novo_produto():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    categorias = listar_categorias()
    if request.method == "POST":
        criar_produto(
            nome=request.form["nome"],
            descricao=request.form.get("descricao", ""),
            preco=float(request.form["preco"]),
            estoque=int(request.form["estoque"]),
            imagem_url=request.form.get("imagem_url", ""),
            categoria_id=int(request.form["categoria_id"])
        )
        flash("Produto criado com sucesso!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/produto_form.html", categorias=categorias, produto=None)


@app.route("/admin/produto/editar/<int:produto_id>", methods=["GET", "POST"])
def admin_editar_produto(produto_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    categorias = listar_categorias()
    produto = obter_produto(produto_id)
    if request.method == "POST":
        atualizar_produto(
            produto_id=produto_id,
            nome=request.form["nome"],
            descricao=request.form.get("descricao", ""),
            preco=float(request.form["preco"]),
            estoque=int(request.form["estoque"]),
            imagem_url=request.form.get("imagem_url", ""),
            categoria_id=int(request.form["categoria_id"])
        )
        flash("Produto atualizado!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("admin/produto_form.html", categorias=categorias, produto=produto)


@app.route("/admin/produto/deletar/<int:produto_id>", methods=["POST"])
def admin_deletar_produto(produto_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    deletar_produto(produto_id)
    flash("Produto removido!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/pedido/<int:pedido_id>")
def admin_pedido_detalhe(pedido_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    pedido, itens = obter_pedido_detalhes(pedido_id)
    return render_template("admin/pedido_detalhe.html", pedido=pedido, itens=itens)


@app.route("/admin/pedido/<int:pedido_id>/status", methods=["POST"])
def admin_atualizar_status(pedido_id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    status = request.form.get("status", "pendente")
    atualizar_status_pedido(pedido_id, status)
    flash("Status atualizado!", "success")
    return redirect(url_for("admin_pedido_detalhe", pedido_id=pedido_id))


# ===================== CONTEXT PROCESSOR =====================

@app.context_processor
def carrinho_info():
    carrinho = session.get("carrinho", {})
    return {"carrinho_qtd": sum(carrinho.values()) if carrinho else 0}


if __name__ == "__main__":
    print("=" * 50)
    print("  MERCADO OLSEN - Sistema de Mercado Online")
    print("=" * 50)
    print("  Site:  http://localhost:5000")
    print("  Admin: http://localhost:5000/admin")
    print("  (Usuário: admin | Senha: admin123)")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
