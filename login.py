import streamlit as st
import hashlib
import hmac

def senha_confere(senha_digitada):
    salt = bytes.fromhex(st.secrets['salt'])
    hash_certo = bytes.fromhex(st.secrets['senha_hash'])
    iteracoes = int(st.secrets['iteracoes'])

    hash_digitado = hashlib.pbkdf2_hmac(
        'sha256', senha_digitada.encode(), salt, iteracoes
    )
    return hmac.compare_digest(hash_digitado, hash_certo)

def fazer_login():
    usuario_ok = st.session_state.get('usuario_input') == st.secrets['usuario']
    senha_ok = senha_confere(st.session_state.get('senha_input', ''))

    if usuario_ok and senha_ok:
        st.session_state['autenticando'] = True
    else:
        st.error('Usuário ou senha incorretos!')
def tela_login():
    if 'autenticando' not in st.session_state:
        st.session_state['autenticando'] = False

    if not st.session_state['autenticando']:
        st.title('🔐 Login - Sistema de Comissão')
        st.text_input('Usuário', key='usuario_input')
        st.text_input('Senha', type='password', key='senha_input')
        st.button('Login', on_click=fazer_login)
        st.stop()