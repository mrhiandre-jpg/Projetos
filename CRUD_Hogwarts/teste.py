import customtkinter as ctk
from tkinter import filedialog  # 1. Importamos a ferramenta que abre pastas!


# 2. Criamos a função (O Motor)
def escolher_arquivo():
    # Abre a janela do Windows/Mac e guarda o endereço do arquivo escolhido
    caminho_do_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo",
        # Podemos até filtrar para o usuário só ver certos tipos de arquivo!
        filetypes=[("Arquivos PDF", "*.pdf"), ("Imagens", "*.png *.jpg"), ("Todos", "*.*")]
    )

    # Verificação de segurança: E se o usuário abriu a janela e clicou em "Cancelar"?
    if caminho_do_arquivo:
        # Se ele escolheu, mudamos o texto da tela para mostrar o caminho
        label_arquivo.configure(text=f"Arquivo escolhido:\n{caminho_do_arquivo}", text_color="white")
    else:
        # Se ele cancelou
        label_arquivo.configure(text="Seleção cancelada.", text_color="red")


# ---------------------------------------------------------
# 3. Criando a Interface Visual (A Carroceria)
# ---------------------------------------------------------
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("500x300")
root.title("Meu Abridor de Arquivos")

# Texto na tela que vai mudar quando escolhermos o arquivo
label_arquivo = ctk.CTkLabel(root, text="Nenhum arquivo selecionado.", text_color="gray")
label_arquivo.pack(pady=50)

# O Botão! 
# Atenção: no 'command', colocamos o nome da função SEM os parênteses ().
# Se colocar (), ele vai rodar a função sozinho assim que o programa abrir.
botao_abrir = ctk.CTkButton(root, text="Abrir Arquivo...", command=escolher_arquivo)
botao_abrir.pack(pady=10)

root.mainloop()