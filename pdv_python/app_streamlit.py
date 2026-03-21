import streamlit as st
import pandas as pd
from database import criar_tabelas, obter_vendas_do_dia
from pdv_core import registrar_venda
from comprovante import gerar_comprovante

st.set_page_config(page_title="PDV Pro - ADS", layout="wide")
criar_tabelas()

st.title("🚀 PDV com Relatórios")

aba1, aba2 = st.tabs(["🛒 Caixa", "📊 Gráficos"])

with aba1:
    if "itens" not in st.session_state:
        st.session_state.itens = []

    c1, c2 = st.columns([2, 1])
    with c1:
        with st.form("novo_item", clear_on_submit=True):
            col_a, col_b, col_c = st.columns([3, 1, 1])
            p = col_a.text_input("Produto")
            pr = col_b.number_input("Preço Unit.", min_value=0.0)
            q = col_c.number_input("Qtd", min_value=1)
            if st.form_submit_button("Adicionar"):
                if p and pr > 0:
                    st.session_state.itens.append({"Produto": p, "Preço Unit.": pr, "Qtd": q})
                    st.rerun()
        if st.session_state.itens:
            st.table(st.session_state.itens)

    with c2:
        total = sum(i["Preço Unit."] * i["Qtd"] for i in st.session_state.itens)
        st.metric("Total", f"R$ {total:.2f}")
        forma = st.selectbox("Pagamento", ["Dinheiro", "Pix", "Cartão"])
        if st.button("Finalizar Venda"):
            if st.session_state.itens:
                v_id, v_total, v_data = registrar_venda(st.session_state.itens, forma)
                st.success("Venda Realizada!")
                st.session_state.itens = []
                st.balloons()

with aba2:
    vendas = obter_vendas_do_dia()
    if vendas:
        df = pd.DataFrame(vendas, columns=['ID', 'Valor', 'Pagamento', 'Data'])
        st.subheader("Vendas por Forma de Pagamento")
        st.bar_chart(df.groupby('Pagamento')['Valor'].sum())
        st.dataframe(df, use_container_width=True)