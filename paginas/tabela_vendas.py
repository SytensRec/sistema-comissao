import streamlit as st
import pandas as pd
from datetime import date                      
from banco import conectar


def mostrar():
    st.header('📋 Tabela de Vendas')

    if 'msg' in st.session_state:
        st.success(st.session_state.pop('msg'))

    
    nomes = pd.read_sql('SELECT nome FROM produtos ORDER BY nome', conectar())
    opcoes_produto = ['Todos'] + list(nomes['nome'])

    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    col_a, col_b = st.columns(2)
    produto_filtro = col_a.selectbox('Produto', opcoes_produto)
    periodo = col_b.date_input('Período', value=(inicio_mes, hoje))

    if len(periodo) != 2:
        st.info('Selecione a data inicial e a data final.')
        return

    data_ini, data_fim = periodo

    
    condicoes = ['v.data BETWEEN ? AND ?']
    params = [str(data_ini), str(data_fim)]

    if produto_filtro != 'Todos':
        condicoes.append('p.nome = ?')
        params.append(produto_filtro)

       
    qtd_min = st.number_input('Quantidade mínima', min_value=1, step=1)

        
    if qtd_min > 1:
        condicoes.append('v.quantidade >= ?')
        params.append(qtd_min)

    where = 'WHERE ' + ' AND '.join(condicoes)
    
    vendas = pd.read_sql(f'''
        SELECT
            v.id AS ID,
            v.data AS Data,
            p.nome AS Produto,
            v.quantidade AS Quantidade,
            v.valor_total AS "Valor Total (R$)",
            v.comissao AS "Comissão (R$)"
        FROM vendas v
        JOIN produtos p ON p.id = v.produto_id
        {where}
        ORDER BY v.data DESC, v.id DESC
    ''', conectar(), params=params)

   
    if vendas.empty:
        st.info('Nenhuma venda encontrada com esses filtros.')
    else:
        st.dataframe(vendas, use_container_width=True, hide_index=True)

        st.divider()
        st.subheader('🗑️ Excluir venda')

        opcoes = {
            f'#{r.ID} - {r.Data} - {r.Produto} ({r.Quantidade} un.)': r.ID
            for r in vendas.itertuples()
        }
        escolha = st.selectbox('Escolha a venda', list(opcoes.keys()))

        confirmar_venda = st.checkbox('Confirmo que desejo excluir essa venda',
                                      key=f'conf_venda_{opcoes[escolha]}')

        if st.button('Excluir Venda', disabled=not confirmar_venda):
            with conectar() as conn:
                conn.execute('DELETE FROM vendas WHERE id = ?', (int(opcoes[escolha]),))
            st.session_state['msg'] = 'Venda excluída!'
            st.rerun()

