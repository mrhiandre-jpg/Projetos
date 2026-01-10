import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



# 1. Busca os dados no catálogo online
titanic = sns.load_dataset('titanic')

# 2. Configura o visual (opcional, só pra ficar bonito)
sns.set_theme(style="whitegrid")

tabela = pd.crosstab(titanic['class'], titanic['alive'])

mortos_1 = tabela.loc['First', 'no']
vivos_1 = tabela.loc['First', 'yes']
total_1 = mortos_1 + vivos_1

mortos_2 = tabela.loc['Second', 'no']
vivos_2 = tabela.loc['Second', 'yes']
total_2 = mortos_2 + vivos_2

mortos_3 = tabela.loc['Third', 'no']
vivos_3 = tabela.loc['Third', 'yes']
total_3 = mortos_3 + vivos_3

texto_legenda_1 = (f'1° Class\n'
                   f'total: {total_1}\n'
                   f'Mortos: {mortos_1}\n'
                   f'Sobreviveu: {vivos_1}')
texto_legenda_2 = (f'2° Class\n'
                   f'total: {total_2}\n'
                   f'Mortos: {mortos_2}\n'
                   f'Sobreviveu: {vivos_2}')
texto_legenda_3 = (f'3° Class\n'
                   f'total: {total_3}\n'
                   f'Mortos: {mortos_3}\n'
                   f'Sobreviveu: {vivos_3}')



# 3. Cria o gráfico
# x = eixo horizontal (Classes)
# hue = cores diferentes (Sobreviveu ou não)
plt.figure(figsize=(10, 7))
plt.subplots_adjust(bottom=0.35)

ax = sns.countplot(data=titanic, x='class', hue='alive', palette='pastel')

for container in ax.containers:
    ax.bar_label(container)

# 4. Títulos
plt.title('Sobreviventes do Titanic por Classe')
plt.xlabel('Classe Social')
plt.ylabel('Quantidade de Pessoas')

plt.figtext(x=0.1, y=0.5, s=texto_legenda_1, transform=ax.transAxes, fontsize=11, ha='left', bbox=dict(facecolor='#f0f0f0', edgecolor='gray', boxstyle='round,pad=1'))
# 5. Mostra a janela
plt.show()