import streamlit as st
from database import criar_tabelas
from pdv_core import registrar_venda
from comprovante import gerar_comprovante

from database import criar_tabelas
criar_tabelas()

st.title("PDV Simples")
st.subheader("Registrar Venda")

if "itens" not in st.session_state:
    st.session_state.itens = []

produto = st.text_input("Produto")
preco = st.number_input("Preço", min_value=0.0, step=0.5)
qtd = st.number_input("Quantidade", min_value=1, step=1)


if st.button("Adicionar item"):
    if produto and preco > 0:
        st.session_state.itens.append({
            "nome": produto,
            "preco": preco,
            "qtd": qtd
        })

if st.session_state.itens:
    st.subheader("Itens do carrinho")
    st.table(st.session_state.itens)

pagamento = st.selectbox("Forma de pagamento", ["Débito", "Crédito", "Pix", "Dinheiro"])

if st.button("Finalizar venda") and st.session_state.itens:
    venda_id, total, data = registrar_venda(st.session_state.itens, pagamento)
    comprovante = gerar_comprovante(venda_id, data, st.session_state.itens, total, pagamento)

    st.text_area("Comprovante", comprovante, height=300)

    st.session_state.itens = []
