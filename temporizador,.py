import pyttsx3
import time
from winotify import Notification

def notificacao(titulo, mensagem):
    e_notificacao = Notification(
        app_id="Meu Alarme",
        title=titulo,
        msg=mensagem,
        duration='short',
    )
    e_notificacao.show()

def contagem_regressiva(segundos, mensagem):
    while segundos > 0:
        # Divmod divide os segundos em minutos e segundos restantes
        mins, secs = divmod(segundos, 60)
        timer = f'{mins:02d}:{secs:02d}'
        # O \r faz o texto sobrescrever a linha anterior no terminal
        print(f"Status: {mensagem} [{timer}]", end="\r")
        time.sleep(1)
        segundos -= 1
    print("\n") # Pula linha quando acaba

def alarme_ciclo():
    tempo_agua_minutos = int(input("Enquantos ciclos de 20 minutos vc deseja beber agua?(1 ciclo = 20 minutos):  "))
    engine = pyttsx3.init()

    # Ajustando a velocidade da voz (opcional)
    engine.setProperty('rate', 180)

    print("Ciclo iniciado! Vou te avisar a cada 20 minutos.")

    def tomar_agua():
        total_minutos = tempo_agua_minutos * 20
        print(f'Ta na hora de beber Água. (Total: {total_minutos} minutos)')
        engine.say(f'Se passaram {total_minutos} minutos. Vamos beber Água.')
        engine.runAndWait()
        print('Tempo iniciado para beber Água!')


    i = 0
    while True:
        # 1. Espera 20 minutos (20 minutos * 60 segundos)
        contagem_regressiva(10*60, "foco Total")

        # 2. Desperta avisando que deu o tempo
        notificacao("DESCANSO", 'Esta na hora de descansar')
        print("HORA DE DESCANSAR!")
        engine.say("Vinte minutos se passaram. Hora de descansar vinte segundos.")
        engine.runAndWait()

        # 3. Espera 20 segundos de intervalo
        print("Aguardando 20 segundos...")
        contagem_regressiva(20, 'Aguardando 20 segundos')


        # 4. Avisa para voltar ao trabalho
        print("VOLTANDO AO TRABALHO!")
        engine.say("Intervalo de vinte segundos encerrado. Voltando ao ciclo de vinte minutos.")
        engine.runAndWait()
        i += 1
        if i == tempo_agua_minutos:
            notificacao("HIDRATAÇÃO", "Hora de beber aquele copo d'água!")
            tomar_agua()
            i = 0
    # Inicia o programa

alarme_ciclo()
