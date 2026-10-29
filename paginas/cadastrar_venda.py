import streamlit as st
import pandas as pd
from datetime import date
from banco import conectar


def mostrar():
    st.header('🛒 Cadastrar Venda')

    produtos = pd.read_sql('SELECT * FROM produtos', conectar())

    if produtos.empty:
        st.warning('Cadastre um produto antes de registrar vendas.')
    else:
        with st.form('form_venda', clear_on_submit=True):
            data_venda = st.date_input('Data da Venda', value=date.today())
            nome_produto = st.selectbox('Produto', produtos['nome'])
            quantidade = st.number_input('Quantidade', min_value=1, step=1)
            enviar_venda = st.form_submit_button('Registrar Venda')

        if enviar_venda:
            produto = produtos[produtos['nome'] == nome_produto].iloc[0]
            valor_total = produto['preco'] * quantidade
            comissao = produto['comissao_valor'] * quantidade

            with conectar() as conn:
                conn.execute(
                    '''INSERT INTO vendas (data, produto_id, quantidade, valor_total, comissao)
                       VALUES (?, ?, ?, ?, ?)''',
                    (str(data_venda), int(produto['id']), int(quantidade), valor_total, comissao)
                )
            st.success(f'Venda registrada! Comissão: R$ {comissao:.2f}')