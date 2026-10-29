import streamlit as st
import pandas as pd
from datetime import date
from banco import conectar

def mostrar():
    st.header('💰 Comissão a Receber')

    hoje = date.today()
    inicio_mes = hoje.replace(day=1)

    periodo = st.date_input('Período', value=(inicio_mes, hoje))

    if len(periodo) != 2:
        st.info('Selecione a data inicial e a data final')
    else:
        data_ini, data_fim = periodo

        resumo = pd.read_sql('''
            SELECT
                COUNT(*) AS qtd_vendas,
                COALESCE(SUM(valor_total), 0) AS total_vendido,
                COALESCE(SUM(comissao), 0) AS total_comissao
            FROM vendas
            WHERE data BETWEEN ? AND ?
        ''', conectar(), params=(str(data_ini), str(data_fim)))
        col1, col2, col3 = st.columns(3)
        col1.metric('Vendas', int(resumo['qtd_vendas'][0]))
        col2.metric('Total vendido', f'R$ {resumo['total_vendido'][0]:.2f}')
        col3.metric('Comissão', f'R$ {resumo['total_comissao'][0]:.2f}')

        st.subheader('Comissão por Produto')

        por_produto = pd.read_sql('''
                SELECT
                    p.nome AS Produto,
                    SUM(v.quantidade) AS Unidades,
                    SUM(v.comissao) AS "Comissão (R$)"
                FROM vendas v
                JOIN produtos p ON p.id = v.produto_id
                WHERE v.data BETWEEN ? AND ?
                GROUP BY p.nome
                ORDER BY SUM(v.comissao) DESC
            ''', conectar(), params=(str(data_ini), str(data_fim)))

        if por_produto.empty:
            st.info('Nenhuma venda nesse período.')
        else:
            st.dataframe(por_produto, use_container_width=True, hide_index=True)
