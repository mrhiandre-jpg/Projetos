import customtkinter as ctk
from tkinter import messagebox
from CRUD_HP import iniciar_banco, Professor, Casas, Ano, Alunos

ctk.set_appearance_mode('Dark')
ctk.set_default_color_theme('blue')

class View_Professor:
    def __init__(self, mestre, cursor, conn):
        self.mestre = mestre
        self.conn = conn
        self.cursor = cursor

        self.logica_professor = Professor(self.cursor, self.conn)

        self.container = ctk.CTkFrame(self.mestre, fg_color='transparent')
        self.container.pack(fill='both', expand=True)

        self.menu_lateral = ctk.CTkFrame(self.container, width=140, corner_radius=0)
        self.menu_lateral.pack(side='left', fill='y')

        self.area_conteudo = ctk.CTkFrame(self.container, corner_radius=0, fg_color='transparent')
        self.area_conteudo.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        self.btn_contratar = ctk.CTkButton(self.menu_lateral, text='contratar',
                                           command=self.aba_contratar)
        self.btn_contratar.pack(pady=20, padx=20)

        self.btn_modi = ctk.CTkButton(self.menu_lateral, text='modificar')
        self.btn_modi.pack(pady=20, padx=20)

        self.btn_demitir = ctk.CTkButton(self.menu_lateral, text='Demitir',
                                                  command=self.aba_demitir)
        self.btn_demitir.pack(pady=20, padx=20)

        self.aba_contratar()
    def limpar(self):
        for tela in self.area_conteudo.winfo_children():
            tela.destroy()

    def aba_contratar(self):

        self.limpar()

        ctk.CTkLabel(self.area_conteudo,
            text="Contratar do Professor",
            font=('Arial', 20, 'bold')
            ).pack(pady=10)
        digt_nome_prof = ctk.CTkEntry(self.area_conteudo,
                                           placeholder_text='Digite o nome do Professor',
                                           width=300
                                           )
        digt_nome_prof.pack(pady=20)

        digt_material_prof = ctk.CTkEntry(self.area_conteudo,
                                               placeholder_text='Digite o Material do Professor',
                                               width=300
                                               )
        digt_material_prof.pack(pady=20)

        def acao_salvar_professor():
            nome = digt_nome_prof.get()
            materia = digt_material_prof.get()

            if nome.strip() == '' or materia.strip() == '':
                messagebox.showwarning('Atenção! Preencha os campos')
                return

            successo = self.logica_professor.contratar(nome, materia)
            if successo:
                messagebox.showinfo('Sucesso', f'{nome} contratado para a Materia {materia}!')
                digt_nome_prof.delete(0, 'end')
                digt_material_prof.delete(0, 'end')
            else:
                messagebox.showerror('Erro: Não foi possível realizar a contratação')


        btn_salvar_prof = ctk.CTkButton(self.area_conteudo,
                                             text="Contratar",
                                             command=acao_salvar_professor)
        btn_salvar_prof.pack(pady=20)

    def aba_demitir(self):
        self.limpar()
        ctk.CTkLabel(self.area_conteudo,
                     text='Demitir Professor',
                     font=('Arial', 20, 'bold')
                     ).pack(pady=10)
        digt_nome_prof = ctk.CTkEntry(self.area_conteudo,
                                      placeholder_text='Digite o nome do(a) Professor(a)',
                                      width=300
                                      )
        digt_nome_prof.pack(pady=20)

        def acao_demitir_professor():
            nome_prof = digt_nome_prof.get().strip().title()

            if nome_prof.strip() == '':
                messagebox.showwarning('Atenção! Preencha os campos')
                return

            successo = self.logica_professor.demitir_professor(nome_prof)
            if successo:
                messagebox.showinfo(f'Sucesso, o professor {nome_prof} foi desligado')
                digt_nome_prof.delete(0, 'end')
            else:
                messagebox.showerror(f'Erro: Não foi possivel demitir o o professor {nome_prof}')

        btn_demitir= ctk.CTkButton(self.area_conteudo,
                                        text='Demitir',
                                        command=acao_demitir_professor)
        btn_demitir.pack(pady=20)

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

         View_Professor(self.abas.tab('Professores'), self.cursor, self.conn)


if __name__ == '__main__':
    app = GUIHogwarts()
    app.mainloop()