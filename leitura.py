import pandas as pd

# Criando um exemplo rápido
dados = {'Produto': ['Teclado', 'Mouse', 'Monitor'], 'Preco': [150, 80, 900]}
df = pd.DataFrame(dados)

# Filtrando: Quero apenas produtos acima de 100 reais
caros = df[df['Preco'] > 100]
print(caros)