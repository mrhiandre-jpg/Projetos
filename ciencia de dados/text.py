while True:
    print('\n' + '=' * 30)
    print('Bem vindo ao menu de gestão de Hogwarts')
    print('=' * 30)
    print('1. Gerenciar Professores')
    print('2. Gerenciar Casas')
    print('3. Gerenciar Ano Letivo')
    print('4. Gerenciar Alunos')
    print('5. Sair')

    op = self.ler_numero('Escolha uma opção: ')
    if op == '1':
        self.menu_professores()
    elif op == '2':
        self.menu_casas()
    elif op == '3':
        self.menu_anos()
    elif op == '4':
        self.menu_alunos
    elif op == '5':
        print('Nox')
        break
    else:
        print('Opção invalida! Tente novamente!')