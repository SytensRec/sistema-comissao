import hashlib
import os
from getpass import getpass

ITERACOES = 600_000

senha = getpass('Digite a nova senha: ')
salt = os.urandom(16)
hash_senha = hashlib.pbkdf2_hmac('sha256', senha.encode(), salt, ITERACOES)

print('Cole no secrets.toml: ')
print(f'salt = "{salt.hex()}"')
print(f'senha_hash = "{hash_senha.hex()}"')
print(f'iteracoes = {ITERACOES}')