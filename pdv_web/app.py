import streamlit as st
import sqlite3
from database import criar_tabelas, conectar
from pdf import gerar_pdf

criar_tabelas()

st.set_page_config(page_title="PDV Web", layout="wide")

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []


# ======================
# FUNÇÕES
# ======================

def adicionar_carrinho(nome, preco, qtd):
    st.session_state.carrinho.append({
        "nome": nome,
        "preco": preco,
        "qtd": qtd
    })


def total_carrinho():
    return sum(i["preco"] * i["qtd"] for i in st.session_state.carrinho)


def salvar_venda(total, pagamento):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("INSERT INTO vendas(total,pagamento) VALUES(?,?)",
                (total, pagamento))

    venda_id = cur.lastrowid

    for i in st.session_state.carrinho:
        cur.execute("""
        INSERT INTO itens_venda VALUES (?,?,?,?)
        """, (venda_id, i["nome"], i["qtd"], i["preco"]))

        conn.commit()
        conn.close()


# ======================
# INTERFACE
# ======================

st.title("🛒 PDV Web")

tab1, tab2, tab3 = st.tabs(["Venda", "Produtos", "Histórico"])


# ======================
# ABA VENDA
# ======================
with tab1:

    conn = conectar()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()

    nomes = [p[1] for p in produtos]

    col1, col2, col3 = st.columns(3)

    with col1:
        produto = st.selectbox("Produto", nomes)

    with col2:
        qtd = st.number_input("Quantidade", 1, 100, 1)

    with col3:
        if st.button("Adicionar"):
            for p in produtos:
                if p[1] == produto:
                    adicionar_carrinho(p[1], p[2], qtd)

    st.divider()

    st.subheader("Carrinho")

    for item in st.session_state.carrinho:
        st.write(item)

    total = total_carrinho()

    st.markdown(f"## Total: R$ {total:.2f}")

    pagamento = st.selectbox(
        "Pagamento", ["Dinheiro", "Crédito", "Débito", "Pix"])

    if st.button("Finalizar Venda"):
        salvar_venda(total, pagamento)

        arquivo = gerar_pdf(st.session_state.carrinho, total, pagamento)

        st.success("Venda salva!")

        with open(arquivo, "rb") as f:
            st.download_button("Baixar Cupom PDF", f, file_name="cupom.pdf")

        st.session_state.carrinho = []

# ======================
# ABA PRODUTOS
# ======================
with tab2:

    nome = st.text_input("Nome do produto")
    preco = st.number_input("Preço", 0.0, 10000.0, step=0.5)

    if st.button("Cadastrar"):
        conn = conectar()
        conn.execute("INSERT INTO produtos(nome,preco) VALUES (?,?)",
                     (nome, preco))
        conn.commit()
        conn.close()
        st.success("Produto cadastrado")


        # ======================
# ABA HISTÓRICO
# ======================
with tab3:

    conn = conectar()
    vendas = conn.execute("SELECT * FROM vendas ORDER BY id DESC").fetchall()
    conn.close()

    for v in vendas:
        st.write(v)

