import sqlite3


def conectar():
    return sqlite3.connect('comissao.db')


def criar_tabelas():
    with conectar() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                preco REAL NOT NULL,
                comissao_valor REAL NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total REAL NOT NULL,
                comissao REAL NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')