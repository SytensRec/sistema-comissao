import streamlit as st
import sqlite3
from banco import conectar

def mostrar():
    st.header('📦 Cadastrar Produto')

    with st.form('Form_produto', clear_on_submit=True):
        nome = st.text_input('Nome do Produto')
        preco = st.number_input('Preço (R$)', min_value=0.0, step=0.01, format='%.2f')
        comissao_valor = st.number_input('Comissão por Unidade (R$)', min_value=0.0, max_value=100.0, step=0.5)
        enviar = st.form_submit_button('Salvar Produto')

    if enviar:
        if not nome.strip():
            st.error('Informe o nome do produto.')
        elif preco <= 0:
            st.error('O preço deve ser maior que zero.')
        else:
            try:
                with conectar() as conn:
                    conn.execute(
                        'INSERT INTO produtos (nome, preco, comissao_valor) VALUES (?, ?, ?)',
                        (nome.strip(), preco, comissao_valor)
                    )
                st.success('Produto cadastrado!')
            except sqlite3.IntegrityError:
                st.error('Já existe um produto com esse nome.')