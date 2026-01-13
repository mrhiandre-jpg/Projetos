import sqlite3

conn = sqlite3.connect('hogwarts.db')
cursor = conn.cursor()

sql_tabelas = [
    """
    CREATE TABLE IF NOT EXISTS professores (
        id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_professor TEXT NOT NULL,
        materia_de_ensino TEXT 
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS casas (
    id_casa INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_casa TEXT NOT NULL,
    id_coordenador INTEGER NOT NULL UNIQUE REFERENCES professores(id_professor)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS anos_escolares (
        id_ano INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,       -- Ex: 'Primeiro Ano', 'Quinto Ano'
        ano_numero INTEGER NOT NULL
        tem_exame_final BOOLEAN,       -- Ex: TRUE para o 5º e 7º ano
        pode_ir_hogsmeade BOOLEAN,     -- Ex: FALSE para 1º e 2º ano
        material_obrigatorio TEXT      -- Ex: 'Livro Padrão de Feitiços Grau 1'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS alunos(
        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_aluno TEXT NOT NULL,
        data_de_nacimento TEXT NOT NULL,
        data_matricula TEXT DEFAULT CURRENT_DATE,
        id_casa INTEGER NOT NULL,
        FOREIGN KEY (id_casa) REFERENCES casas(id_casa),
        FOREIGN KEY (id_ano_atual) REFERENCES anos_escolares(id_ano),
        aluno_status TEXT CHECK(aluno_status IN ('Ativo', 'Inativo')) DEFAULT 'Ativo'
    );
    """,
    """
    CREATE TRIGGER IF NOT EXISTS bloqueia_troca_casa
    BEFORE UPDATE ON alunos
    FOR EACH ROW
    WHEN OLD.id_casa <> NEW.id_casa  -- Se a Casa Velha for diferente da Nova
    BEGIN
        -- O comando RAISE(ABORT) cancela tudo e manda uma mensagem de erro
        SELECT RAISE(ABORT, 'Erro: A decisão do Chapéu Seletor é final! Não é permitido mudar de casa.');
    END;
    """
]

for sql in sql_tabelas:
    cursor.execute(sql)
conn.commit() # Salva a estrutura
print("--- Tabelas verificadas/criadas com sucesso ---")

class Professor:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco

    def criar_professor(self, nome, materia_de_ensino):
        sql = 'INSERT INTO professores (nome_professor, materia_de_ensino) VALUES (?, ?)'
        try:
            self.cursor.execute(sql, (nome, materia_de_ensino))
            self.conn.commit()
            print(f'Professor {nome} contratado com sucesso!')
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f'Erro ao cadastrar {e}')
            return None

    def atualizar_materia(self, id_professor, nova_materia):
        sql = 'UPDATE professores SET materia_de_ensino = ? WHERE id_professor = ?'
        try:
            self.cursor.execute(sql, (nova_materia, id_professor))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Materia do Professor {id_professor} atualizada para {nova_materia} com sucesso!')
            else:
                print('Professor não encontrado!')
        except sqlite3.IntegrityError as e:
            print(f'Erro ao atualizar: {e}')
    def demitir_professor(self, id_professor):
        sql = "DELETE FROM professores WHERE id_professor = ?"

        try:
            self.cursor.execute(sql, (id_professor,))
            self.conn.commit()
            if cursor.rowcount > 0:
                print(f"Professor ID {id_professor} demitido.")
            else:
                print("Professor não encontrado.")

        except sqlite3.IntegrityError:
            # É aqui que cai se ele for Coordenador de uma casa
            print(f"ERRO: Não é possível demitir o ID {id_professor} pois ele é Coordenador de uma Casa!")
            print("Dica: Troque o coordenador da casa primeiro antes de demitir este.")
        except sqlite3.Error as e:
            print(f"Erro ao deletar: {e}")

class Casas:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco
    def criar_casa(self,nome_casa, id_coordenador):
        sql = 'INSERT INTO casas (nome_casa, id_coordenador) VALUES (?, ?)'
        try:
            self.cursor.execute(sql, (nome_casa, id_coordenador))
            self.conn.commit()
            print(f'Casa {nome_casa} criada com sucesso!')
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f'Erro: O Professor ID {id_coordenador} já coordena outra casa! Escolha outro professor!')
            return None
class Ano:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco
    def criar_ano_letivo(self, numero, titulo, tem_exames=False, vai_pra_hogsmeade=False):
        sql = 'INSERT INTO anos_escolares (ano_numero, titulo, tem_exames, pode_ir_hogsmeade) VALUES (?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (numero, titulo, tem_exames, vai_pra_hogsmeade))
            self.conn.commit()
            print(f'Ano escolar {titulo} criado com sucesso!')
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f'Erro ao cadastrar ano {numero}')
            return None
class Alunos:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco
    def matricular_aluno(self, nome, ano, id_casa, data_de_nacimento):
        sql = 'INSERT INTO alunos (nome_aluno, ano_escolar, id_casa, data_de_nacimento) VALUES (?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (nome, ano, id_casa, data_de_nacimento))
            self.conn.commit()
            print(f'Aluno {nome} foi selecionado para a casa {id_casa}!')
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f'Erro na matricula {nome}')
            return None


    def atualizar_ano_aluno(self, id_aluno, novo_id_ano):
        sql = 'UPDATE alunos SET ano_escolar = ? WHERE id_aluno = ?'
        try:
            self.cursor.execute(sql, (novo_id_ano, id_aluno))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Sucesso {id_aluno} atualizado com sucesso!')
            else:
                print(f'Erro: Aluno {id_aluno} não encontrado!')
        except sqlite3.IntegrityError as e:
            print(f'Erro ao atualizar o aluno {id_aluno}')
    def deletar_aluno(self, id_aluno):
        sql = 'DELETE FROM alunos WHERE id_aluno = ?'
        try:
            self.cursor.execute(sql, (id_aluno,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Aluno {id_aluno} deletado com sucesso!')
            else:
                print('Erro: Id não encontrado!')
        except sqlite3.IntegrityError as e:
            print(f'Erro ao deletar aluno {id_aluno}, {e}')

class Menu:
    def __init__(self, cursor, conn):
        self.ge_prof = Professor(cursor, conn)
        self.ge_casa = Casas(cursor, conn)
        self.ge_ano = Ano(cursor, conn)
        self.ge_aluno = Alunos(cursor, conn)

    def ler_numero(self, mensagem):
        while True:
            entrada = input(mensagem)
            if entrada.isdigit():
                return int(entrada)
            else:
                print("Entrada inválida! Por favor, digite apenas números.")

    def iniciar(self):
        while True:
            print('\n' + '='*30)
            print('Bem vindo ao menu de gestão de Hogwarts')
            print('='*30)
            print('1. Gerenciar Professores')
            print('2. Gerenciar Casas')
            print('3. Gerenciar Ano Letivo')
            print('4. Gerenciar Alunos')
            print('5. Sair')

            op = self.ler_numero('Escolha uma opção: ')