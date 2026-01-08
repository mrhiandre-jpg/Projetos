import os
import tkinter as tk
import pandas as pd

from tkinter import filedialog
from tabulate import tabulate

def carregar_arquivo():
    root = tk.Tk()
    root.title('Carregar Arquivo')
    root.geometry('500x500')
    root.withdraw()

    print('Abrindo arquivo')
    abrir_arquivo = filedialog.askopenfilename(
        title='Carregar Arquivo',
        filetypes=(('Arquivo', '*.csv'),)
    )
    if abrir_arquivo:

        print(f'Arquivo selecionado: {abrir_arquivo}')
        try:

            df = pd.read_csv(abrir_arquivo)
            return df
        except Exception as e:
            print(f'Erro ao carregar arquivo: {e}')
            return None
    else:
        print('Nenhum arquivo selecionado')
        return None

#chamar a função para pegar os dados

notas = carregar_arquivo()
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
        print(tabulate(notas, headers='keys', tablefmt='psql', showindex=False, stralign='left', numalign='left'))
    except KeyError as e:
        print(f'Erro ao carregar arquivo: {e}')