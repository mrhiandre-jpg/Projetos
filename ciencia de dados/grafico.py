import seaborn as sns
import matplotlib.pyplot as plt

# 1. Busca os dados no catálogo online
titanic = sns.load_dataset('titanic')

# 2. Configura o visual (opcional, só pra ficar bonito)
sns.set_theme(style="whitegrid")

# 3. Cria o gráfico
# x = eixo horizontal (Classes)
# hue = cores diferentes (Sobreviveu ou não)
plt.figure(figsize=(8, 6))
sns.countplot(data=titanic, x='class', hue='survived', palette='pastel')

# 4. Títulos
plt.title('Sobreviventes do Titanic por Classe')
plt.xlabel('Classe Social')
plt.ylabel('Quantidade de Pessoas')

# 5. Mostra a janela
plt.show()