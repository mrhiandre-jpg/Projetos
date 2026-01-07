import pyttsx3
import time
from winotify import Notification
import sys

# 1. Essa parte e para criar uma notificação
def enviar_notificacao(titulo, mensagem):
    notificacao = Notification(
        app_id='Meu Alarme',
        title=titulo,
        msg=mensagem,
        duration='short'
    )
    notificacao.show()
#2. Essa partecria o relogio de contagem regresiva
def contagem_regresiva(segundos, mensagem):
    while segundos > 0:
        mins, secs = divmod(segundos, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f'Status: {mensagem} [{timer}]', end='\r')
        #2_1. utilizei a biblioteca sys para criar o contador
        sys.stdout.flush()
        time.sleep(1)
        segundos -= 1
    print('\n')

#3. Aqui começa o verdadeiro codigo
def alarme_ciclo():
    #3_1. Essa e a parte de configuração
    print('Cada ciclo e igual a 20 minutos.', '\n')
    ciclo_agua = int(input('Digite quantos ciclos de Agua: '))
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)

    print('Ciclo iniciado! Vou te avisar a cada ciclo.')
    #3_2. Criei uma função dentro para otimizar o codigo
    def tomar_agua():
        total_minutos = ciclo_agua * 20
        print('Ta na hora de beber àgua.')
        engine.say(f'Se passaram {total_minutos}, vamos beber àgua')
        engine.runAndWait()
        print('Tempo iniciado para beber àgua')

    #3_2. Agora sera executado o alarme de 20 mim e 20 segundo
    i = 0
    while True:
        contagem_regresiva(20 * 60, 'Foco Total')

        enviar_notificacao('Descanso', 'Esta na hora de descnasar')
        print('Esta na hora de descnasar')
        engine.say('Se passaram 20 minutos esta na hora dedesnsar os olhos.')
        engine.runAndWait()

        contagem_regresiva(20, 'Descansar 20 segundos')
        print('Voltando a Trabalhar')
        engine.say('Se passaram 20 segundos esta na hora de voltar a focar')
        engine.runAndWait()

        i += 1
        if i == ciclo_agua:
            enviar_notificacao('Agua', 'Esta na hora de beber agua')
            tomar_agua()
            i = 0

alarme_ciclo()