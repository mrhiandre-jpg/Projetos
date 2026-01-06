import pyttsx3
import datetime
import time


def despertar(hora_alarme, frase):
    engine = pyttsx3.init()
    print(f"Alarme configurado para às {hora_alarme}. Aguardando...")

    while True:
        # Pega a hora atual no formato HH:MM
        agora = datetime.datetime.now().strftime("%H:%M")

        if agora == hora_alarme:
            print("HORA DE ACORDAR!")
            # Faz o computador falar a frase 3 vezes
            for i in range(3):
                engine.say(frase)
                engine.runAndWait()
            break  # Para o programa após despertar

        time.sleep(10)  # Verifica a cada 10 segundos para não sobrecarregar o PC


# Configuração do usuário
horario = input("Digite a hora do alarme (ex: 07:30): ")
mensagem = input("O que o despertador deve dizer? ")

despertar(horario, mensagem)