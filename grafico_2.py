import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. Busca os dados
titanic = sns.load_dataset('titanic')

# 2. Configura visual e cálculos
sns.set_theme(style="whitegrid")

tabela = pd.crosstab(titanic['class'], titanic['alive'])

# Cálculos (Igual ao seu código)
mortos_1 = tabela.loc['First', 'no']
vivos_1 = tabela.loc['First', 'yes']
total_1 = mortos_1 + vivos_1

mortos_2 = tabela.loc['Second', 'no']
vivos_2 = tabela.loc['Second', 'yes']
total_2 = mortos_2 + vivos_2

mortos_3 = tabela.loc['Third', 'no']
vivos_3 = tabela.loc['Third', 'yes']
total_3 = mortos_3 + vivos_3

# Textos formatados
texto_legenda_1 = (f'1° Class\nTotal: {total_1}\nMortos: {mortos_1}\nSobreviveu: {vivos_1}')
texto_legenda_2 = (f'2° Class\nTotal: {total_2}\nMortos: {mortos_2}\nSobreviveu: {vivos_2}')
texto_legenda_3 = (f'3° Class\nTotal: {total_3}\nMortos: {mortos_3}\nSobreviveu: {vivos_3}')

# 3. Cria o gráfico
plt.figure(figsize=(10, 8)) # Aumentei um pouco a altura
plt.subplots_adjust(bottom=0.35) # Espaço branco embaixo

ax = sns.countplot(data=titanic, x='class', hue='alive', palette='pastel')

# Rótulos nas barras
for container in ax.containers:
    ax.bar_label(container)

plt.title('Sobreviventes do Titanic por Classe')
plt.xlabel('Classe Social')
plt.ylabel('Quantidade de Pessoas')

# --- AQUI ESTÁ A MUDANÇA ---
# Criamos 3 chamadas separadas, mudando apenas o valor de X

# Caixa 1 (Esquerda - x=0.05)
plt.figtext(x=0.2, y=0.2, s=texto_legenda_1,
            fontsize=10, ha='left',
            bbox=dict(facecolor='#f0f0f0', edgecolor='gray', boxstyle='round,pad=1'))

# Caixa 2 (Meio - x=0.38)
plt.figtext(x=0.45, y=0.2, s=texto_legenda_2,
            fontsize=10, ha='left',
            bbox=dict(facecolor='#f0f0f0', edgecolor='gray', boxstyle='round,pad=1'))

# Caixa 3 (Direita - x=0.72)
plt.figtext(x=0.72, y=0.2, s=texto_legenda_3,
            fontsize=10, ha='left',
            bbox=dict(facecolor='#f0f0f0', edgecolor='gray', boxstyle='round,pad=1'))

plt.show()