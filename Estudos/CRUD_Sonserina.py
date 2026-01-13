import sqlite3

conn = sqlite3.connect('escola.db')
cursor = conn.cursor()

sql_tabelas = [
    """
    CREATE TABLE IF NOT EXISTS professores (
        id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_professor TEXT NOT NULL,
        cpf TEXT UNIQUE,
        materia_de_ensino TEXT, 
        professor_status TEXT CHECK(professor_status IN ('Ativo', 'Inativo')) DEFAULT 'Ativo'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS turma(
        id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_turma TEXT,
        ano_letivo INTEGER,
        id_professor_responsavel INTEGER,
        FOREIGN KEY (id_professor_responsavel) REFERENCES professores(id_professor)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS alunos(
        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT NOT NULL UNIQUE,
        nome_completo TEXT NOT NULL,
        data_de_nacimento TEXT NOT NULL,
        cpf TEXT UNIQUE,
        data_matricula TEXT DEFAULT CURRENT_DATE,
        aluno_status TEXT CHECK(aluno_status IN ('Ativo', 'Inativo')) DEFAULT 'Ativo', 
        id_turma INTEGER,
        FOREIGN KEY (id_turma) REFERENCES turma (id_turma)
    );
    """
]

for sql in sql_tabelas:
    cursor.execute(sql)
conn.commit() # Salva a estrutura
print("--- Tabelas verificadas/criadas com sucesso ---")


def cadastrar_professor(nome, cpf, materia):
    sql = 'INSERT INTO professores (nome_professor, cpf, materia_de_ensino) VALUES (?, ?, ?)'
    try:
        cursor.execute(sql, (nome, cpf, materia))
        conn.commit()
        print(f'Professor {nome} criado com sucesso!')
        return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        if 'UNIQUE' in str(e):
            print(f'Aviso: O Professor {nome} já existe. Recuperando ID...')
            # --- O PULO DO GATO ---
            # Se já existe, vamos buscar o ID dele no banco
            cursor.execute("SELECT id_professor FROM professores WHERE cpf = ?", (cpf,))
            resultado = cursor.fetchone()  # Pega o primeiro resultado (tupla)
            return resultado[0] if resultado else None
        else:
            print(f'Erro de integridade: {e}')
            return None


def criar_turma(nome_turma, ano, id_prof):
    if not id_prof:
        return None

    sql = 'INSERT INTO turma (nome_turma, ano_letivo, id_professor_responsavel) VALUES (?, ?, ?)'
    try:
        cursor.execute(sql, (nome_turma, ano, id_prof))
        conn.commit()
        print(f'Turma {nome_turma} criada com sucesso!')
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        # Se der erro (ex: nome da turma for unique ou algo assim,
        # mas aqui vamos simplificar assumindo que queremos buscar se falhar)
        print(f'Aviso: Turma {nome_turma} provavelmente já existe. Buscando ID...')

        # Vamos buscar pelo nome e ano para garantir
        cursor.execute("SELECT id_turma FROM turma WHERE nome_turma = ? AND ano_letivo = ?", (nome_turma, ano))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None


def matricular_aluno(matricula, nome, data_nasc, cpf, id_turma):
    if not id_turma:
        print("Erro: Tentativa de matricular sem ID de turma válido.")
        return None

    # Note que não passamos 'data_matricula' nem 'aluno_status'
    # (O banco usa o DEFAULT)
    sql = """
          INSERT INTO alunos (matricula, nome_completo, data_de_nacimento, cpf, id_turma)
          VALUES (?, ?, ?, ?, ?) \
          """

    try:
        cursor.execute(sql, (matricula, nome, data_nasc, cpf, id_turma))
        conn.commit()
        print(f"Aluno {nome} matriculado com sucesso!")
        return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        if 'UNIQUE' in str(e):
            print(f"Erro: Aluno {nome} (CPF ou Matrícula) já existe no sistema.")
        else:
            print(f"Erro ao matricular: {e}")
        return None


def gerar_relatorio_geral():
    sql = """
          SELECT alunos.nome_completo, \
                 turma.nome_turma, \
                 professores.nome_professor
          FROM alunos WHERE professores.nome_professor = 'Severus Snape'
                   JOIN turma ON alunos.id_turma = turma.id_turma
                   JOIN professores ON turma.id_professor_responsavel = professores.id_professor \
          """

    try:
        cursor.execute(sql)
        dados = cursor.fetchall()  # Pega todas as linhas do resultado

        print("\n--- RELATÓRIO GERAL DA ESCOLA ---")
        print(f"{'ALUNO':<20} | {'TURMA':<20} | {'PROFESSOR':<20}")
        print("-" * 65)

        for linha in dados:
            # linha é uma tupla: (nome_aluno, nome_turma, nome_prof)
            print(f"{linha[0]:<20} | {linha[1]:<20} | {linha[2]:<20}")

    except sqlite3.Error as e:
        print(f"Erro ao gerar relatório: {e}")


if __name__ == '__main__':
    # 1. Garante o Professor (Cria ou Busca)
    id_snape = cadastrar_professor("Severus Snape", "12345678900", "Poções")

    # 2. Garante a Turma (Cria ou Busca) usando o ID do passo 1
    if id_snape:
        id_turma_sonserina = criar_turma('1° Ano - Sonserina', 2024, id_snape)

        # 3. Matricula o Aluno usando o ID do passo 2
        if id_turma_sonserina:
            # Vamos criar o Draco Malfoy
            matricular_aluno(
                "2024-SONS-01",  # Matrícula
                "Draco Malfoy",  # Nome
                "1980-06-05",  # Data Nasc
                "11122233344",  # CPF
                id_turma_sonserina  # ID da Turma
            )

            # Vamos criar o Crabbe
            matricular_aluno(
                "2024-SONS-02",
                "Vincent Crabbe",
                "1980-09-01",
                "55566677788",
                id_turma_sonserina
            )
    gerar_relatorio_geral()