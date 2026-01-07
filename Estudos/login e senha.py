def validar_login(login):
    """
    Verifica se o login é válido.
    """
    if len(login) == 0 or " " in login:
        print('Login inválido')
        return False
    return True

def validar_senha(senha):
    """
    Verifica se a senha atende aos critérios de segurança.
    """
    if len(senha) < 8:
        print("Senha fraca: necessário ter 8 caracteres.")
        return False

    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_simbolo = any(c in "!@#$%" for c in senha)

    if not tem_maiuscula:
        print("Senha fraca: Falta letras maiúsculas.")
    if not tem_minuscula:
        print("Senha fraca: Falta letras minúsculas.")
    if not tem_numero:
        print("Senha fraca: Falta números.")
    if not tem_simbolo:
        print("Senha fraca: Falta símbolos.")

    return tem_maiuscula and tem_minuscula and tem_numero and tem_simbolo


# <------------------ cadastro ---------->
def cadastro_usuario():
    print("--- Cadastro ---")
    while True:
        novo_login = input("Crie o nome de usuário:\n")
        if not validar_login(novo_login):
            continue

        nova_senha = input("Crie a sua senha:\n")
        if not validar_senha(nova_senha):
            continue

        confirme_senha = input("Digite novamente a senha:\n")
        if nova_senha == confirme_senha:
            print("Senha criada com sucesso!")
            return novo_login, nova_senha
        else:
            print("As senhas não coincidem.")
#--------------login-----------

def login_usuario(login_cadastrado, senha_cadastrada):
    print("\n--- Login ---")
    import time
    import sys
    max_tentativa = 3
    tentativa = max_tentativa
    tempo = 60
    while True:
        if tentativa > 0:
            login_digitado = input("Digite o seu login:\n")
            senha_digitada = input("Digite a sua senha:\n")

            if login_digitado == login_cadastrado and senha_digitada == senha_cadastrada:
                print("Login bem-sucedido!")
                break
            else:
                tentativa -= 1
                if tentativa > 0:
                    print(f"Login ou a senha estão incorretos. Você tem mais {tentativa}")
                else:
                    print('Espera 60 segundos para tentar novamente')
                    for segundos_restantes in range(tempo,0,-1):
                        sys.stdout.write(f'\rTempo restante: {segundos_restantes}')
                        sys.stdout.flush()
                        time.sleep(1)
                    print('Tempo acabou porfavor digite novamente')
                    tentativa = max_tentativa
        else:
            tentativa = max_tentativa




login_do_usuario, senha_do_usuario = cadastro_usuario()
login_usuario(login_do_usuario, senha_do_usuario)