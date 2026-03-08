import socket
import time

# Configuração de Rede (Camada de Transporte)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('localhost', 5000))


def enviar_comando(comando):
    print(f"[Terra] Enviando: {comando}")
    # Simulando a latência de rádio (ex: 2 segundos para ir)
    time.sleep(2)
    cliente.send(comando.encode())

    # Esperando a confirmação (Redes: Handshake/ACK)
    resposta = cliente.recv(1024).decode()
    print(f"[Terra] Resposta recebida: {resposta}")


enviar_comando("INICIAR_PERFURACAO")
time.sleep(1)
enviar_comando("RECOLHER_TRIPE")