import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variável global para guardar os dados
df_atual = None


# --- FUNÇÕES DE NAVEGAÇÃO (O Segredo!) ---
def mostrar_pagina_tabela():
    # Esconde o frame do gráfico
    frame_grafico.pack_forget()
    # Mostra o frame da tabela (ocupa a tela toda)
    frame_tabela.pack(fill=tk.BOTH, expand=True)


def mostrar_pagina_grafico():
    # Verifica se tem dados antes de trocar
    if df_atual is None:
        messagebox.showwarning("Aviso", "Carregue um arquivo primeiro!")
        return

    # Esconde a tabela
    frame_tabela.pack_forget()

    # Gera o gráfico novo
    gerar_grafico_no_frame()

    # Mostra o frame do gráfico
    frame_grafico.pack(fill=tk.BOTH, expand=True)


# --- FUNÇÃO DE CARREGAR ARQUIVO ---
def carregar_arquivo():
    global df_atual
    caminho = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if not caminho: return

    try:
        df = pd.read_csv(caminho)

        # Sua Lógica de Negócio
        if 'Nota_Original' in df.columns:
            df['status'] = 'Reprovado'
            df.loc[df.Nota_Original >= 7.0, 'status'] = 'Aprovado'
            df.loc[(df.Nota_Original >= 5.0) & (df.Nota_Original < 7.0), 'status'] = 'Recuperação'

            df_atual = df
            atualizar_tabela_visual(df)

            # Habilita o botão de ir para o gráfico
            btn_ir_grafico['state'] = 'normal'
        else:
            messagebox.showerror("Erro", "Faltou a coluna 'Nota_Original'")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")


# --- ATUALIZAR A TABELA (Visual) ---
def atualizar_tabela_visual(df):
    # Limpa dados antigos
    tree.delete(*tree.get_children())

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Configura Cores
    tree.tag_configure('aprovado_tag', background='#C6EFCE')
    tree.tag_configure('reprovado_tag', background='#FFC7CE')
    tree.tag_configure('recuperacao_tag', background='#FFEB9C')

    # Descobre coluna status
    try:
        idx = list(df.columns).index('status')
    except:
        idx = -1

    for linha in df.to_numpy().tolist():
        tag = ()
        if idx != -1:
            val = linha[idx]
            if val == 'Aprovado':
                tag = ('aprovado_tag',)
            elif val == 'Reprovado':
                tag = ('reprovado_tag',)
            elif val == 'Recuperação':
                tag = ('recuperacao_tag',)

        tree.insert("", "end", values=linha, tags=tag)


# --- GERAR GRÁFICO (Visual) ---
def gerar_grafico_no_frame():
    # Limpa o gráfico anterior do frame
    for widget in area_desenho.winfo_children():
        widget.destroy()

    # Cria Figura
    fig = plt.Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)

    sns.countplot(data=df_atual, x='status', hue='status', palette='viridis', legend=False, ax=ax)
    ax.set_title("Status da Turma")

    for c in ax.containers: ax.bar_label(c)

    canvas = FigureCanvasTkAgg(fig, master=area_desenho)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# ==========================================
#      INTERFACE PRINCIPAL (SETUP)
# ==========================================
root = tk.Tk()
root.title("Sistema Escolar - Navegação")
root.geometry("800x600")

# --- BARRA SUPERIOR (Fixa) ---
# Essa barra nunca some, fica sempre no topo
header = tk.Frame(root, bg="#eee", height=50)
header.pack(fill=tk.X, side=tk.TOP)

btn_load = tk.Button(header, text="📂 Carregar CSV", command=carregar_arquivo)
btn_load.pack(side=tk.LEFT, padx=10, pady=10)

# --- PÁGINA 1: TABELA (Frame Container) ---
frame_tabela = tk.Frame(root, bg="white")

# Botão para ir para o gráfico
btn_ir_grafico = tk.Button(frame_tabela, text="Ver Gráfico da Turma ➔",
                           command=mostrar_pagina_grafico,  # CHAMA A TROCA DE PÁGINA
                           bg="#4CAF50", fg="white", font=("Arial", 12), state='disabled')
btn_ir_grafico.pack(pady=10)

# Tabela Treeview
tree = ttk.Treeview(frame_tabela)
scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill=tk.BOTH, expand=True)

# --- PÁGINA 2: GRÁFICO (Frame Container) ---
frame_grafico = tk.Frame(root, bg="white")

# Botão VOLTAR
btn_voltar = tk.Button(frame_grafico, text="⬅ Voltar para Tabela",
                       command=mostrar_pagina_tabela,  # CHAMA A VOLTA
                       bg="#FF9800", fg="white", font=("Arial", 12))
btn_voltar.pack(anchor="w", padx=20, pady=10)  # anchor='w' cola na esquerda

# Área onde o desenho do gráfico vai entrar
area_desenho = tk.Frame(frame_grafico)
area_desenho.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# --- INICIALIZAÇÃO ---
# Começamos mostrando a tabela e escondendo o gráfico
mostrar_pagina_tabela()

root.mainloop()