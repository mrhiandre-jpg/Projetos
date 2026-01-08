import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

def janela():
    root = tk.Tk()
    root.title('Ciência de dados')
    root.geometry('500x500')
    root.withdraw()

    print('Abrindo arquivo')
    abrir_arquivo = filedialog.askopenfilename(
        title='Escolha uma arquivo',
        filetypes=[('Arquivos csv', '*.csv'), ('todos arquivos', '*.*')]
    )

    if abrir_arquivo:
        print(f'Arquivo selecionado: {abrir_arquivo}')

        try:
            df = pd.read_csv(abrir_arquivo)
            return df
        except Exception as e:
            print(f'Erro ao abrir arquivo {e}')
            return None
    else:
        print('Nenhum arquivo selecionado')
        return None
dados = janela()

if dados is not None:
    print('\n---- Primeiras 5 linhas ----')
    print(dados.head())
    print(f'\n0 Arquivo selecionado tem {dados.shape[0]} linhas e {dados.shape[1]} colunas')