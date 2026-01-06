import pandas as pd
import numpy as np

# Criando 15 alunos com notas aleatórias entre 4 e 10
np.random.seed(42) # Para as notas serem sempre as mesmas ao rodar
nomes = ['Ana', 'Bruno', 'Carla', 'Diego', 'Erik', 'Fernanda', 'Gabriel',
         'Helena', 'Igor', 'Julia', 'Kevin', 'Larissa', 'Mario', 'Nina', 'Otto']
notas = [8.2, 7.5, 9.4, 8.8, 9.8, 6.5, 8.0, 9.1, 5.4, 8.9, 7.2, 9.5, 4.5, 8.1, 9.2]

df = pd.DataFrame({
    'Nome': nomes,
    'Nota_Original': notas
})

# Salvando em um arquivo Excel (caso você queira abrir no computador)
df.to_csv('notas_alunos.csv', index=False)

print("Arquivo 'notas_alunos.csv' criado com sucesso!")
print(df)