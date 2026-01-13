import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas.core import frame

df_atual = None

#essa parte faz com q abra arquivo CSV
def carregar_arquivo():
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title='carregar arquivo',
        filetype=(('Arquivo csv', '*.csv'),)
    )
    if not caminho:
        root.deiconify()
        return None,None
    try:
        df = pd.read_csv(caminho)
        return None,None
    except Exception as e:
        print(f'Erro ao carregar arquivo: {e}')
        root.destroy()
        return None,None

def gerar_grafico():
    for widget in frame.winfo_children():
        widget.destroy()
    if df_atual is None:
        return

    figura = plt.figure(figsize = (10,10), dpi = 100)