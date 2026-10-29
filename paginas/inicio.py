import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta      
from banco import conectar


def mostrar():
    st.title('💸 Sistema de Comissão')

    # ---- DATAS ----
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    fim_mes_passado = inicio_mes - timedelta(days=1)          
    inicio_mes_passado = fim_mes_passado.replace(day=1)       

    st.caption(f"Hoje é {hoje.strftime('%d/%m/%Y')}")

    # ---- DADOS DO MÊS ATUAL ----
    resumo = pd.read_sql('''
        SELECT
            COUNT(*) AS qtd,
            COALESCE(SUM(valor_total), 0) AS vendido,
            COALESCE(SUM(comissao), 0) AS comissao
        FROM vendas
        WHERE data >= ?
    ''', conectar(), params=(str(inicio_mes),))

    # ---- DADOS DO MÊS PASSADO ---- 
    passado = pd.read_sql('''
        SELECT COALESCE(SUM(comissao), 0) AS comissao
        FROM vendas
        WHERE data BETWEEN ? AND ?
    ''', conectar(), params=(str(inicio_mes_passado), str(fim_mes_passado)))

    comissao_atual = float(resumo['comissao'][0])             
    comissao_passada = float(passado['comissao'][0])         
    diferenca = comissao_atual - comissao_passada             

    # ---- CARTÕES ----
    st.subheader('Este mês')
    col1, col2, col3 = st.columns(3)
    col1.metric('Vendas', int(resumo['qtd'][0]))
    col2.metric('Total vendido', f"R$ {resumo['vendido'][0]:.2f}")
    col3.metric('Comissão', f"R$ {comissao_atual:.2f}", delta=round(diferenca, 2))   

    st.divider()

    # ---- DUAS COLUNAS: TABELA E GRÁFICO ----
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader('Últimas vendas')
        ultimas = pd.read_sql('''
            SELECT v.data AS Data, p.nome AS Produto,
                   v.quantidade AS Quantidade, v.comissao AS "Comissão (R$)"
            FROM vendas v
            JOIN produtos p ON p.id = v.produto_id
            ORDER BY v.data DESC, v.id DESC
            LIMIT 5
        ''', conectar())

        if ultimas.empty:
            st.info('Nenhuma venda registrada ainda. Comece em "Cadastrar Venda".')
        else:
            st.dataframe(ultimas, use_container_width=True, hide_index=True)

    with col_dir:
        st.subheader('Comissão por dia (este mês)')
        por_dia = pd.read_sql('''
            SELECT data, SUM(comissao) AS comissao
            FROM vendas
            WHERE data >= ?
            GROUP BY data
            ORDER BY data
        ''', conectar(), params=(str(inicio_mes),))

        if por_dia.empty:
            st.info('Sem vendas neste mês.')
        else:
            por_dia['data'] = pd.to_datetime(por_dia['data']).dt.strftime('%d/%m')

            grafico = (
                alt.Chart(por_dia)
                .mark_bar(color='#2E8B57')
                .encode(
                    x=alt.X('data:N', title=None, sort=None, axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('comissao:Q', title='Comissão (R$)'),
                    tooltip=['data', 'comissao']
                )
            )
            st.altair_chart(grafico, use_container_width=True)