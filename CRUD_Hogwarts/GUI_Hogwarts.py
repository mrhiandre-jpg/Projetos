import customtkinter as ctk
from tkinter import messagebox
from CRUD_HP import iniciar_banco, Professor, Casas, Ano, Alunos

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')

class GUIHogwarts(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('CRUD Hogwarts')
        self.geometry('600x600')

        print('Conectando ao banco de dados')
        self.conn , self.cursor = iniciar_banco()

        self.ge_professor = Professor(self.conn , self.cursor)
        self.ge_casa = Casas(self.conn , self.cursor)
        self.ge_ano = Ano(self.conn , self.cursor)
        self.ge_aluno = Alunos(self.conn , self.cursor)

        self.abas = ctk.CTkTabview(self, width=400, height=400)
        self.abas.pack(pady=20)

        self.abas.add('Professores')
        self.abas.add('Casas')
        self.abas.add('Ano')
        self.abas.add('Alunos')

        self.aba_professor()

    def aba_professor(self):
        aba_prof = self.abas.tab('Professores')

        lbl_titulo = ctk.CTkLabel(aba_prof,
                                       text='Contratar Novo Professor',
                                       font=('Arial', 12, 'bold'))
        lbl_titulo.pack(pady=20)

        self.digt_nome_prof = ctk.CTkEntry(aba_prof,
                                          placeholder_text='Digite o nome do Professor',
                                          width=300
                                          )
        self.digt_nome_prof.pack(pady=20)

        self.digt_material_prof = ctk.CTkEntry(aba_prof ,
                                               placeholder_text='Digite o Material do Professor',
                                               width=300
                                               )
        self.digt_material_prof.pack(pady=20)

        self.btn_salvar_prof = ctk.CTkButton(aba_prof,
                                             text="Contratar",
                                             command=self.acao_salvar_professor)
        self.btn_salvar_prof.pack(pady=20)


    def acao_salvar_professor(self):
        nome = self.digt_nome_prof.get()
        materia = self.digt_material_prof.get()
        print(f'tentando salvar professor {nome},materia {materia}')


if __name__ == "__main__":
    app = GUIHogwarts()
    app.mainloop()