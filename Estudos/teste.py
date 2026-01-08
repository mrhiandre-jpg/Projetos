import os
import tkinter as tk
import pandas as pd

from tkinter import filedialog
from tabulate import tabulate
from tkinter import ttk

def carregar_arquivo():
    root = tk.Tk()
    root.withdraw()

    print('Abrindo arquivo')
    abrir_arquivo = filedialog.askopenfilename(
        title='Carregar Arquivo',
        filetypes=(('Arquivo', '*.csv'),)
    )
    if not abrir_arquivo:
        root.destroy()
        return None, None
        print(f'Arquivo selecionado: {abrir_arquivo}')
    try:

        df = pd.read_csv(abrir_arquivo)
        return df, root
    except Exception as e:
        print(f'Erro ao carregar arquivo: {e}')
        return None

def janela(root, df):
    root.deiconify()
    root.title('Janela')
    root.geometry('500x500')

    tree = ttk.Treeview(root, columns=list(df.columns), show='headings')

    tree.tag_configure('aprovado_tag', background='#C6EFCE')  # Verde claro (Excel)
    tree.tag_configure('reprovado_tag', background='#FFC7CE')  # Vermelho claro (Excel)
    tree.tag_configure('recuperacao_tag', background='#FFEB9C')  # Amarelo claro (Excel)

    try:
        index_status = list(df.columns).index('status')
    except ValueError:
        print("Aviso: Coluna 'status' não encontrada. As cores não funcionarão.")
        index_status = -1

    for coluna in df.columns:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, width=100)

    for linha in df.to_numpy().tolist():

        minha_tag = ()

        # Se achamos a coluna status, verificamos o valor dela nessa linha
        if index_status != -1:
            valor_status = linha[index_status]

            if valor_status == 'Aprovado':
                minha_tag = ('aprovado_tag',)
            elif valor_status == 'Reprovado':
                minha_tag = ('reprovado_tag',)
            elif valor_status == 'Recuperado':  # Ou 'Recuperação', dependendo do seu código
                minha_tag = ('recuperacao_tag',)
        tree.insert('', 'end', values=linha, tags=minha_tag)

    scroll = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side='right', fill='y')
    tree.pack(expand=True, fill='both')
    root.mainloop()

#chamar a função para pegar os dados

notas, janela_root = carregar_arquivo()
if notas is not None:
    print('\n---- processando arquivo ----')
    try:
        notas['Notas_Finais'] = notas['Nota_Original']
        notas['status'] = 'Reprovado'

        notas.loc[(notas['Nota_Original'] >= 8.0) & (notas['Nota_Original'] <= 9.0), 'Notas_Finais'] +=1
        notas.loc[notas['Nota_Original'] >= 9.0, 'Notas_Finais'] = 10

        notas['Bonus'] = notas['Notas_Finais'] - notas['Nota_Original']

        notas.loc[notas['Nota_Original'] >= 7.0, 'status'] = 'Aprovado'
        notas.loc[(notas['Nota_Original'] >= 5.0) & (notas['Nota_Original'] < 7.0), 'status'] = 'Recuperado'

        """ 
        Modo mais proficional
        regra_bonus = (notas.Nota_Original >= 7.0) & (notas.Nota_Original <= 9.0)
        regra_dez = (notas.Nota_Original >= 9.0)
        
        nota.loc[ regra_bonus, 'Notas_Finais'] += 1
        nota.loc[ regra_dezz    , 'Notas_Finais'] = 10
        """
        notas = notas.round(1)

        janela(janela_root, notas)
        print(tabulate(notas, headers='keys', tablefmt='psql', showindex=False, stralign='left', numalign='left'))

    except AttributeError:
        print("Erro: Verifique os nomes das colunas (lembre-se: sem espaços para usar ponto!)")
    except KeyError as e:
        print(f'Erro ao carregar arquivo: {e}')
else:
    print('Nenhum arquivo encontrado')