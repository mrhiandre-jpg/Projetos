import sqlite3

conn = sqlite3.connect('hogwarts.db')
cursor = conn.cursor()

# Troque 'alunos' pelo nome real da sua tabela
nome_tabela = 'alunos'

try:
    cursor.execute(f"SELECT * FROM casas")

    # Pega os nomes das colunas para o cabeçalho
    nomes_colunas = [description[0] for description in cursor.description]
    print(f"Colunas: {nomes_colunas}")
    print("-" * 40)

    dados = cursor.fetchall()

    for linha in dados:
        print(linha)

except sqlite3.OperationalError:
    print(f"Erro: A tabela 'casas' não existe.")

conn.close()