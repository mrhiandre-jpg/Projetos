import sqlite3

def iniciar_banco():
    sql_tabelas = [
        """
        CREATE TABLE IF NOT EXISTS materia(
            id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_materia TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            e_obrigatori BOOLEAN DEFAULT 1
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS professores (
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_professor TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            materia_de_ensino TEXT 
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS casas (
            id_casa INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_casa TEXT NOT NULL,
            id_coordenador INTEGER NOT NULL UNIQUE REFERENCES professores(nome_professor)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS anos_escolares (
            id_ano INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,       -- Ex: 'Primeiro Ano', 'Quinto Ano'
            ano_numero INTEGER NOT NULL,
            tem_exame_final BOOLEAN,       -- Ex: TRUE para o 5º e 7º ano
            pode_ir_hogsmeade BOOLEAN,     -- Ex: FALSE para 1º e 2º ano
            material_obrigatorio TEXT      -- Ex: 'Livro Padrão de Feitiços Grau 1'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS alunos(
            id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_aluno TEXT NOT NULL,
            data_de_nascimento TEXT NOT NULL,
            data_matricula TEXT DEFAULT CURRENT_DATE,
            id_casa INTEGER NOT NULL,
            id_ano_atual INTEGER,
            aluno_status TEXT CHECK(aluno_status IN ('Ativo', 'Inativo')) DEFAULT 'Ativo',
            FOREIGN KEY (id_casa) REFERENCES casas(id_casa),
            FOREIGN KEY (id_ano_atual) REFERENCES anos_escolares(id_ano)
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
    conn = sqlite3.connect('hogwarts.db')
    cursor = conn.cursor()


    for sql in sql_tabelas:
        cursor.execute(sql)
    conn.commit() # Salva a estrutura
    print("--- Tabelas verificadas/criadas com sucesso ---")

    return conn, cursor

class Materia:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco

    def criar_materia(self, nome, descricao='', obrigatorio=False):
        sql = 'INSERT INTO materia(nome_materia, descricao, e_obrigatori) VALUES (?, ?, ?)'
        try:
            self.cursor.execute(sql, (nome, descricao, obrigatorio))
            self.conn.commit()
            print(f'Materia {nome} criada com sucesso!')
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
    def listar_materia(self):
        sql = 'SELECT nome_materia, descricao, e_obrigatori FROM materia'
        self.cursor.execute(sql,)
        return self.cursor.fetchall()

    def deletar_materia(self, nome_materia):
        try:
            sql_verificar = 'SELECT e_obrigatoria FROM materia WHERE nome_materia = ?'
            self.cursor.execute(sql_verificar, (nome_materia,))
            resultado = self.cursor.fetchone()
            if not resultado:
                return False,  f'Materia {nome_materia} não encontrada'
            eh_obrigatoria = resultado[0]
            if eh_obrigatoria == 1:
                return False, f'Bloqueado: Materia {nome_materia} obriagatorio'

            sql_delete = 'DELETE FROM materia WHERE nome_materia = ?'
            self.cursor.execute(sql_delete  , (nome_materia,))
            self.conn.commit()

            return True, f'Materia {nome_materia} deletada com sucesso!'
        except sqlite3.IntegrityError:
                return False, f'Erro: Materia {nome_materia} não pode ser apagada pois eh obrigatoria'
        except Exception as e:
            return False, f'Erro: {e}'


class Professor:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco

    def contratar(self, nome, data_de_nascimento, materia_de_ensino):
        sql = 'INSERT INTO professores (nome_professor, data_nascimento,materia_de_ensino) VALUES (?, ?,?)'
        try:
            self.cursor.execute(sql, (nome, data_de_nascimento, materia_de_ensino))
            self.conn.commit()
            print(f'Professor {nome} contratado com sucesso!')
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f'Erro ao cadastrar {e}')
            return None
    def busca(self, nome):
        sql = "SELECT id_professor, nome_professor,data_nascimento, materia_de_ensino FROM professores WHERE nome_professor = ?"
        self.cursor.execute(sql, (nome,))
        resultado = self.cursor.fetchone()

        return resultado

    def atualizar(self, id_prof, novo_nome, nova_data_nascimento, nova_materia):
        sql = """
            UPDATE professores 
            SET nome_professor = ?,
            data_nascimento = ?,
            materia_de_ensino  = ? 
            WHERE id_professor = ?
        """
        try:
            novo = (novo_nome, nova_data_nascimento, nova_materia, id_prof)

            self.cursor.execute(sql, novo)
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Atualização com sucesso!')
            else:
                print('Professor não encontrado!')
        except sqlite3.IntegrityError as e:
            print(f'Erro ao atualizar: {e}')
            return False
    def demitir_professor(self, nome_professor):
        sql = "DELETE FROM professores WHERE nome_professor = ?"

        try:
            self.cursor.execute(sql, (nome_professor,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Professor {nome_professor} foi desligado.')
                return True
            else:
                print("Professor não encontrado.")
                return False

        except sqlite3.IntegrityError:

            print(f'ERRO: Não é possível demitir o ID {nome_professor} pois ele é Coordenador de uma Casa!')
            print("Dica: Troque o coordenador da casa primeiro antes de demitir este.")
        except sqlite3.Error as e:
            print(f'Erro ao deletar: {e}')
            return False

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
    def trocar_coord(self, id_casa, novo_id_coordenador):
        sql = 'UPDATE casas SET id_coordenador = ? WHERE id_casa = ?'
        try:
            self.cursor.execute(sql, (novo_id_coordenador, id_casa))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'O coordenador da casa foi atualizado para {novo_id_coordenador} com sucesso!')
            else:
                print(f'O ID {id_casa} não foi encontrado')
        except sqlite3.IntegrityError:
            print(f'Verifica se o ID do {novo_id_coordenador} existe e se ele ja e coordenador de outra casa')

        except sqlite3.Error as e:
            print(f'Erro: {e}')
class Ano:
    def __init__(self, cursor_banco, conexao_banco):
        self.cursor = cursor_banco
        self.conn = conexao_banco
    def criar_ano_letivo(self, numero, titulo, tem_exame_final=False, vai_pra_hogsmeade=False):
        sql = 'INSERT INTO anos_escolares (ano_numero, titulo, tem_exame_final, pode_ir_hogsmeade) VALUES (?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (numero, titulo, tem_exame_final, vai_pra_hogsmeade))
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
    def matricular_aluno(self, nome, id_ano_atual, id_casa, data_de_nascimento):
        sql = 'INSERT INTO alunos (nome_aluno, id_ano_atual, id_casa, data_de_nascimento) VALUES (?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (nome, id_ano_atual, id_casa, data_de_nascimento))
            self.conn.commit()
            print(f'Aluno {nome} foi selecionado para a casa {id_casa}!')
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f'Erro na matrícula {nome}')
            return None


    def atualizar_ano_aluno(self, id_aluno, novo_id_ano):
        sql = 'UPDATE alunos SET id_ano_atual = ? WHERE id_aluno = ?'
        try:
            self.cursor.execute(sql, (novo_id_ano, id_aluno))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Sucesso {id_aluno} atualizado com sucesso!')
            else:
                print(f'Erro: Aluno {id_aluno} não encontrado!')
        except sqlite3.IntegrityError:
            print(f'Erro ao atualizar o aluno {id_aluno}')
    def deletar_aluno(self, id_aluno):
        sql = 'DELETE FROM alunos WHERE id_aluno = ?'
        try:
            self.cursor.execute(sql, (id_aluno,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Aluno {id_aluno} deletado com sucesso!')
            else:
                print('Erro: ID não encontrado!')
        except sqlite3.IntegrityError as e:
            print(f'Erro ao deletar aluno {id_aluno}, {e}')

class Menu:
    def __init__(self, cursor, conn):
        self.ge_materia = Materia(cursor, conn)
        self.ge_prof = Professor(cursor, conn)
        self.ge_casa = Casas(cursor, conn)
        self.ge_ano = Ano(cursor, conn)
        self.ge_aluno = Alunos(cursor, conn)
    @staticmethod
    def ler_numero(mensagem):
        while True:
            entrada = input(mensagem)
            if entrada.isdigit():
                return int(entrada)
            else:
                print("Entrada inválida! Por favor, digite apenas números.")

    def menu_professores(self):
        while True:
            print('\n --- Professores --- ')
            print('1 - Contratar')
            print('2 - Mudar Matéria')
            print('3 - Demitir')
            print('4 - Voltar')
            op = self.ler_numero('Escolha uma opção: ')
            if op == 1:
                print('\n --- Contratando ---')
                nome = input('Nome: ')
                materia = input('Matéria: ')
                self.ge_prof.contratar(nome, materia)
                pass
            elif op == 2:
                print('\n --- Troca de Matéria ---')
                id_professor = self.ler_numero('ID professores: ')
                nova_materia = input('Nova matéria: ')
                self.ge_prof.atualizar_materia(id_professor, nova_materia)
                pass
            elif op == 3:
                print('\n --- Desligamento ---')
                id_delete_professor = self.ler_numero('ID do professor para demitir: ')
                self.ge_prof.demitir_professor(id_delete_professor)
                pass
            elif op == 4:
                break

    # -- Sub-MENUS----
    def menu_casas(self):
        while True:
            print('\n --- Fundar Casas --- ')
            print('1 - Fundar Casas')
            print('2 - Trocar Coordenador')
            print('3 - Voltar   ')
            op = self.ler_numero('Escolha uma opção: ')
            if op == 1:
                print('\n Fundando Casa')
                nome = input('Nome da casa: ')
                id_coordenador = self.ler_numero('Digite o ID do Professor: ')
                self.ge_casa.criar_casa(nome, id_coordenador)
                pass
            elif op == 2:
                print('\n Trocar Coordenador')
                id_casa = self.ler_numero(' Digite o ID da Casa: ')
                novo_id_coordenador = self.ler_numero(' Digite o ID do Professor: ')
                self.ge_casa.trocar_coord(id_casa, novo_id_coordenador)
                pass
            elif op == 3:
                print('\n Voltar')
                break
            else:
                print('Opção Inválida')
    def menu_anos(self):
        while True:
            print('\n Ano Letivo')
            print('1 - Criar Ano Letivo')
            print('2 - Voltar')
            op = self.ler_numero('Escolha uma opção: ')
            if op == 1:
                print('\n Criar Ano Letivo')
                num = self.ler_numero(' Digite o Ano: ')
                titulo = input('Titulo do Ano Letivo: ')
                exame = input('Tem exames finais (S/N): ').upper() == 'S'
                hogsmeade = input('Pode ir a hogsmeade (S/N): ').upper() == 'S'

                self.ge_ano.criar_ano_letivo(num, titulo, exame, hogsmeade)
                pass
            elif op == 2:
                break
    def menu_alunos(self):
        while True:
            print('\n --- Alunos --- ')
            print('1 - Matrícula')
            print('2 - Atualizar aluno')
            print('3 - Deletar aluno')
            print('4 - Voltar')

            op = self.ler_numero('\n Escolha uma opção')

            if op == 1:
                print('\n ---- Matrícula de Aluno ----')
                nome = input('Nome do aluno: ')
                data_nascimento = input('Data de nascimento (AAAA/DD/MM): ')
                id_ano = self.ler_numero(' Digite o ID do Ano: ')
                id_casa = self.ler_numero(' Digite o ID da Casa: ')
                self.ge_aluno.matricular_aluno(nome, id_ano, id_casa, data_nascimento)
                pass
            elif op == 2:
                print('\n ---- Alteração Aluno ----')
                id_aluno = self.ler_numero(' Digite o ID do Aluno que deseja alterar: ')
                id_ano_novo = self.ler_numero(' Digite o ID do novo ano: ')
                self.ge_aluno.atualizar_ano_aluno(id_aluno, id_ano_novo)
                pass
            elif op == 3:
                print('\n --- Desligamento do Aluno ----')
                id_aluno = self.ler_numero(' Digite o ID do Aluno que deseja apagar: ')
                self.ge_aluno.deletar_aluno(id_aluno)
            elif op == 4:
                break
    def iniciar(self):
        while True:
            print('\n' + '='*30)
            print('Bem-vindo ao menu de gestão de Hogwarts')
            print('='*30)
            print('1. Gerenciar Professores')
            print('2. Gerenciar Casas')
            print('3. Gerenciar Ano Letivo')
            print('4. Gerenciar Alunos')
            print('5. Sair')

            op = self.ler_numero('Escolha uma opção: ')
            if op == 1:
                self.menu_professores()
            elif op == 2:
                self.menu_casas()
            elif op == 3:
                self.menu_anos()
            elif op == 4:
                self.menu_alunos()
            elif op == 5:
                print('Nox')
                break
            else:
                print('Opção inválida! Tente novamente!')

if __name__ == '__main__':
    conn, curso = iniciar_banco()
    sistema_hogwarts = Menu(curso, conn)
    sistema_hogwarts.iniciar()
    conn.close()
