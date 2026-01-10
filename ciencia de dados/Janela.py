import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd

def carregar_arquivo():
    root = tk.Tk()
    root.withdraw()

    caminho = filedialog.askopenfilename(
        title='Carregar arquivo',
        filetypes= (('Arquivo csv','*.csv'), )
    )
    if not caminho:
        root.deiconify()
        return None,None
    try:
        df = pd.read_csv(caminho)
        return df, root
    except Exception as e:
        print(f'Erro ao carregar arquivo: {e}')
        root.destroy()
        return None,None


def mostrar_na_janela(root, df):
    root.deiconify()
    root.title("Visualização de Notas")
    root.geometry("800x400")

    tree = ttk.Treeview(root, columns=list(df.columns), show='headings')

    # --- 1. CONFIGURANDO AS CORES (Tags) ---
    # Usamos cores em Hexadecimal (pasteis) para o texto continuar legível
    tree.tag_configure('aprovado_tag', background='#C6EFCE')  # Verde claro (Excel)
    tree.tag_configure('reprovado_tag', background='#FFC7CE')  # Vermelho claro (Excel)
    tree.tag_configure('recuperacao_tag', background='#FFEB9C')  # Amarelo claro (Excel)

    # Configurando cabeçalhos
    for coluna in df.columns:
        tree.heading(coluna, text=coluna)
        tree.column(coluna, width=100,)  # Centralizado

    # --- 2. DESCOBRINDO ONDE ESTÁ A COLUNA STATUS ---
    # Precisamos saber o índice (0, 1, 2...) da coluna 'status' para checar o valor
    try:
        index_status = list(df.columns).index('status')
    except ValueError:
        print("Aviso: Coluna 'status' não encontrada. As cores não funcionarão.")
        index_status = -1

    # --- 3. INSERINDO DADOS COM LÓGICA DE COR ---
    for linha in df.to_numpy().tolist():

        # Define a tag padrão (sem cor)
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

        # Inserimos a linha passando a tag escolhida
        tree.insert("", "end", values=linha, tags=minha_tag)

    # Barra de Rolagem
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    root.mainloop()


notas, janela_root = carregar_arquivo()

if notas is not None:
    print('---- Processando dados... ----')
    try:
        # --- SUA LÓGICA (Com notação de ponto!) ---
        notas['Notas_Finais'] = notas.Nota_Original
        notas['status'] = 'Reprovado'

        notas.loc[(notas.Nota_Original >= 8.0) & (notas.Nota_Original <= 9.0), 'Notas_Finais'] += 1
        notas.loc[notas.Nota_Original >= 9.0, 'Notas_Finais'] = 10

        notas['Bonus'] = notas.Notas_Finais - notas.Nota_Original

        notas.loc[notas.Nota_Original >= 7.0, 'status'] = 'Aprovado'
        notas.loc[(notas.Nota_Original >= 5.0) & (notas.Nota_Original < 7.0), 'status'] = 'Recuperado'

        # --- AQUI VEM A MÁGICA ---
        # Em vez de print(tabulate...), chamamos nossa função visual:
        notas = notas.round(1)
        mostrar_na_janela(janela_root, notas)

    except AttributeError:
        print("Erro: Verifique os nomes das colunas (lembre-se: sem espaços para usar ponto!)")
    except Exception as e:
        print(f"Erro: {e}")
else:
    print("Nenhum arquivo carregado.")
