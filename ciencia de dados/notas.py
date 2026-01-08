import pandas as pd
from tabulate import tabulate

notas = pd.read_csv('notas_alunos.csv')
notas = notas.round(1)
notas.info()
notas.describe()
notas['Notas_Finais'] = notas['Nota_Original']
notas['status'] = 'Reprovado'

notas.loc[(notas['Nota_Original'] >= 8.0) & (notas['Nota_Original'] < 9.0), 'Notas_Finais'] += 1
notas.loc[(notas['Nota_Original'] >= 9.0),   'Notas_Finais'] = 10

notas['Bonus'] = notas['Notas_Finais'] - notas['Nota_Original']

notas.loc[notas['Nota_Original'] >= 7.0, 'status'] = 'aprovados'
notas.loc[(notas['Nota_Original'] >= 5.0) & (notas['Nota_Original'] < 7.0), 'status'] = 'Recuperação'


#tabulete

print(tabulate(notas, headers='keys', tablefmt='psql', showindex=False, stralign='left', numalign='left'))
# [FILTRO DE LINHAS , NOME DA COLUNA]
