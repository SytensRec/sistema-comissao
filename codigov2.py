import streamlit as st
from banco import criar_tabelas
from login import tela_login
from paginas import inicio, cadastrar_venda, cadastrar_produto, tabela_vendas, tabela_produtos, comissao

# confg inial
st.set_page_config(
    page_title='Sistema de Comissão', page_icon=':money_with_wings:', layout='wide', initial_sidebar_state='expanded'
)

# banco de dados
criar_tabelas()
# tela login
tela_login()

# logoff
if st.sidebar.button("Sair da Conta", use_container_width=True):
    st.session_state["autenticando"] = False
    st.rerun()

# menu
st.sidebar.title('MENU')
pagina = st.sidebar.radio(
    'Escolha uma opção',
    ['Início', 'Cadastrar Venda', 'Cadastrar Produto', 'Tabela de Vendas', 'Tabela de Produtos', 'Comissão a Receber']
)

# TELAS
if pagina == 'Início':
    inicio.mostrar()
elif pagina == 'Cadastrar Venda':
    cadastrar_venda.mostrar()
elif pagina == 'Cadastrar Produto':
    cadastrar_produto.mostrar()
elif pagina == 'Tabela de Vendas':
    tabela_vendas.mostrar()
elif pagina == 'Tabela de Produtos':
    tabela_produtos.mostrar()
elif pagina == 'Comissão a Receber':
    comissao.mostrar()
else:
    st.error(f'Nenhuma tela encontrada para: {pagina}')
