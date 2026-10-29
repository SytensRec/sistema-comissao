# Sistema de Comissão

Sistema web para cadastrar produtos e vendas e calcular a comissão a receber, feito com Python, Streamlit e SQLite.

## Funcionalidades

- Login com senha protegida por hash (PBKDF2 com salt), com os segredos fora do código
- Cadastro de produtos, com comissão em valor fixo por unidade
- Cadastro de vendas, com cálculo automático da comissão
- Tabela de vendas com filtros por produto, período e quantidade mínima, e exclusão com confirmação
- Tabela de produtos com edição e exclusão (produtos com vendas não podem ser excluídos)
- Comissão a receber por período, com o total por produto
- Página inicial com resumo do mês, últimas vendas e gráfico de comissão por dia

## Tecnologias

Python, Streamlit, pandas, Altair e SQLite.

## Como rodar

1. Instale as dependências: `pip install -r requirements.txt`
2. Gere o hash da senha: `python gerar_hash.py`
3. Crie o arquivo `.streamlit/secrets.toml` com o resultado:

```toml
usuario = "seu_usuario"
salt = "gerado pelo gerar_hash.py"
senha_hash = "gerado pelo gerar_hash.py"
iteracoes = 600000
```

4. Rode o app: `streamlit run codigov2.py`

O banco de dados (`comissao.db`) é criado automaticamente na primeira execução.

## Estrutura do projeto

```
codigov2.py        # menu e navegação
banco.py           # conexão e criação das tabelas
login.py           # tela de login e verificação da senha
gerar_hash.py      # gera salt e hash da senha
paginas/           # uma tela por arquivo
```

## O que aprendi
Aprendi nessas ultimas semanas alguns sitemas. Como o uso de HASH e como utilizar ele de forma correta, e como funciona, aprendi sobre a biblicoteca SQL, melhorei muitos pontos no sistema do streamlit.
    Entendo que tenho muitas coisas para melhorar, porem como meu primeiro projeto, me sinto feliz e satisfeito

## URL

https://repositorio-demonstracao.streamlit.app/git add .

# AVISO 
Banco de dados temporario, apenas para uso de demonstração.