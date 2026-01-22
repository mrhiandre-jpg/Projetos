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
        self.btn_contratar.pack(pady=5, padx=5)

        self.btn_modi = ctk.CTkButton(self.menu_lateral, text='modificar',
                                      command=self.aba_modicar)
        self.btn_modi.pack(pady=5, padx=5)

        self.btn_demitir = ctk.CTkButton(self.menu_lateral, text='Demitir',
                                                  command=self.aba_demitir)
        self.btn_demitir.pack(pady=5, padx=5)

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

        container_nome = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        container_nome.pack(pady=(0,10))

        ctk.CTkLabel(container_nome, text="Nome do Professor:", font=('Arial', 12, 'bold')).pack(anchor="w")
        digt_nome_prof = ctk.CTkEntry(container_nome,
                                           placeholder_text='Digite o nome do Professor',
                                           width=300
                                           )
        digt_nome_prof.pack(pady=5)


        container_dtn = ctk.CTkFrame(self.area_conteudo, fg_color='transparent')
        container_dtn.pack(pady=(0,10))

        ctk.CTkLabel(container_dtn, text='Data do Professor:', font=('Arial', 12, 'bold')).pack(anchor="w")
        digt_dtn_prof = ctk.CTkEntry(container_dtn,
                                               placeholder_text='DD/MM/AAAA',
                                               width=300
                                               )
        digt_dtn_prof.pack(pady=5)

        container_materia = ctk.CTkFrame(self.area_conteudo, fg_color='transparent')
        container_materia.pack(pady=(0,10))

        ctk.CTkLabel(container_materia, text='Materia do Professor:', font=('Arial', 12, 'bold')).pack(anchor="w")
        digt_material_prof = ctk.CTkEntry(container_materia,
                                               placeholder_text='Digite o Material do Professor',
                                               width=300
                                               )
        digt_material_prof.pack(pady=5)

        def acao_salvar_professor():
            nome = digt_nome_prof.get()
            data = digt_dtn_prof.get()
            materia = digt_material_prof.get()

            if nome.strip() == ''  or data.strip() == '' or materia.strip() == '':
                messagebox.showwarning('Atenção! Preencha os campos')
                return

            successo = self.logica_professor.contratar(nome, data, materia)
            if successo:
                messagebox.showinfo('Sucesso', f'{nome} contratado para a Materia {materia}!')
                digt_nome_prof.delete(0, 'end')
                digt_dtn_prof.delete(0, 'end')
                digt_material_prof.delete(0, 'end')
            else:
                messagebox.showerror('Erro: Não foi possível realizar a contratação')


        btn_salvar_prof = ctk.CTkButton(self.area_conteudo,
                                             text="Contratar",
                                             command=acao_salvar_professor)
        btn_salvar_prof.pack(pady=20)
    def aba_modicar(self):
        self.limpar()
        ctk.CTkLabel(self.area_conteudo,
                     text='Buscar Professor',
                     font=('Arial', 20, 'bold')
                     ).pack(pady=10)
        container_nome = ctk.CTkFrame(self.area_conteudo, fg_color="transparent")
        container_nome.pack(pady=(0,10))

        ctk.CTkLabel(container_nome, text="Nome do Professor:", font=('Arial', 12, 'bold')).pack(anchor="w")

        prof_busca = ctk.CTkEntry(container_nome,
                                      placeholder_text='Digite o nome do Professor',
                                      width=300
                                      )
        prof_busca.pack(pady=5)

        self.caixa_edicao = ctk.CTkFrame(self.area_conteudo, fg_color='transparent')

        def verificar_professor():
            nome = prof_busca.get().strip()
            dados = self.logica_professor.busca(nome)

            if dados:
                for tela in self.caixa_edicao.winfo_children():
                    tela.destroy()
                self.caixa_edicao.pack(pady=20, fill='both', expand=True)

                id_prof, nome_atual, dtn_atual, materia_atual = dados

                ctk.CTkLabel(self.caixa_edicao, text=f'Editando: {nome_atual} (ID:{id_prof})').pack()

                ctk.CTkLabel(self.caixa_edicao, text='Nome do Professor: ').pack(anchor='w', pady=5)
                ent_novo_nome = ctk.CTkEntry(self.caixa_edicao, width=300)
                ent_novo_nome.insert(0, nome_atual)
                ent_novo_nome.pack(pady=5)

                ctk.CTkLabel(self.caixa_edicao, text='Data de Nascimento: ').pack(anchor='w', pady=5)
                ent_novo_dtn =ctk.CTkEntry(self.caixa_edicao, width=300)
                ent_novo_dtn.insert(0, dtn_atual)
                ent_novo_dtn.pack(pady=5)

                ctk.CTkLabel(self.caixa_edicao, text='Materia:').pack(anchor='w', pady=5)
                ent_nova_materia = ctk.CTkEntry(self.caixa_edicao, width=300)
                ent_nova_materia.insert(0, materia_atual)
                ent_nova_materia.pack(pady=5)

                def salvar_alteração():
                    nome_final = ent_novo_nome.get().strip()
                    dtn_final = ent_novo_dtn.get().strip()
                    materia_final = ent_nova_materia.get().strip()

                    if nome_final and materia_final:
                        sucesso = self.logica_professor.atualizar(id_prof, nome_final, dtn_final, materia_final)
                        if sucesso:
                            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                            self.caixa_edicao.pack_forget()  # Esconde após salvar
                            prof_busca.delete(0, 'end')
                        else:
                            messagebox.showerror("Erro", "Não foi possível atualizar.")
                    else:
                        messagebox.showwarning("Atenção", "Preencha todos os campos!")

                ctk.CTkButton(self.caixa_edicao, text="Salvar Alterações", fg_color="green",
                              command=salvar_alteração).pack(pady=5)
            else:
                messagebox.showerror("Erro", "Professor não encontrado!")
                self.caixa_edicao.pack_forget()

        ctk.CTkButton(self.area_conteudo, text="Buscar e Editar", command=verificar_professor).pack()

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
        self.entry_busca = ctk.CTkFrame(self.area_conteudo, fg_color='transparent')

        def verificar_professor():
            nome = digt_nome_prof.get().strip()
            dados = self.logica_professor.busca(nome)

            if dados:
                for tela in self.entry_busca.winfo_children():
                    tela.destroy()
                self.entry_busca.pack(pady=20, fill='both', expand=True)

                id_prof, nome_atual, dtn_atual, materia_atual = dados

                ctk.CTkLabel(self.entry_busca, text=f'Buscando: {nome_atual} (ID:{id_prof})').pack()

                ctk.CTkLabel(self.entry_busca, text=f'Nome do Professor: {nome_atual} ').pack(anchor='w', pady=5)

                ctk.CTkLabel(self.entry_busca, text=f'Data de Nascimento:{dtn_atual} ').pack(anchor='w', pady=5)

                ctk.CTkLabel(self.entry_busca, text=f'Materia:{materia_atual}').pack(anchor='w', pady=5)

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

            ctk.CTkButton(self.entry_busca, text="Salvar Alterações", fg_color="green",
                            command=acao_demitir_professor).pack(pady=5)

        btn_demitir= ctk.CTkButton(self.area_conteudo,
                                            text='Demitir',
                                            command=verificar_professor)
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