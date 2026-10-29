import streamlit as st
import sqlite3
import pandas as pd
from banco import conectar

def mostrar():
    st.header('📋 Tabela de Produtos')

    if 'msg' in st.session_state:
        st.success(st.session_state.pop('msg'))

    produtos = pd.read_sql('''
        SELECT
            nome AS Produto,
            preco AS "Preço (R$)",
            comissao_valor AS "Comissão por Unidade (R$)"
        FROM produtos
        ORDER BY nome
    ''', conectar())

    if produtos.empty:
        st.info('Nenhum produto cadastrado ainda.')
    else:
        st.dataframe(produtos, use_container_width=True, hide_index=True)

        lista = pd.read_sql(
        'SELECT id, nome, preco, comissao_valor FROM produtos ORDER BY nome', conectar()
    )

        if not lista.empty:
            st.divider()
            st.subheader('✏️ Editar ou excluir produto')

            nome_escolhido = st.selectbox('Escolha o produto', lista['nome'])
            p = lista[lista['nome'] == nome_escolhido].iloc[0]
            pid = int(p['id'])

    # EDITAR
        with st.form('form_editar'):
            novo_nome = st.text_input('Nome', value=p['nome'], key=f'nome_{pid}')
            novo_preco = st.number_input('Preço (R$)', min_value=0.0, step=0.1, 
                                         format='%.2f', value=float(p['preco']), key=f'preco_{pid}')
            nova_comissao = st.number_input('Comissão por unidade (R$)', min_value=0.0, step=0.1, 
                                        format='%.2f', value=float(p['comissao_valor']), key=f'com_{pid}')
            salvar = st.form_submit_button('Salvar alterações')

        if salvar: 
            if not novo_nome.strip():
                st.error('Informe o nome do produto')
            elif novo_preco <= 0:
                st.error('O preço deve ser maior que zero.')
            else:
                try:
                    with conectar() as conn:
                        conn.execute(
                            'UPDATE produtos SET nome = ?, preco = ?, comissao_valor = ? WHERE id = ?',
                            (novo_nome.strip(), novo_preco, nova_comissao, pid)
                        )
                    st.session_state['msg'] = 'Produto atualizado!'
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error('Já existe um produto com esse nome.')

        # EXCLUIR
        confirmar_prod = st.checkbox('Confirmo que desejo excluir esse produto',
                                     key=f'conf_prod_{pid}')

        if st.button('🗑️ Excluir este produto', disabled=not confirmar_prod):
            with conectar() as conn:
                qtd = conn.execute(
                    'SELECT COUNT(*) FROM vendas WHERE produto_id = ?', (pid,)
                ).fetchone()[0]

                if qtd == 0:
                    conn.execute('DELETE FROM produtos WHERE id = ?', (pid,))

            if qtd > 0:
                st.error(f'Não é possível excluir: este produto tem {qtd} venda(s) registrada(s).')
            else:
                st.session_state['msg'] = 'Produto excluído!'
                st.rerun()