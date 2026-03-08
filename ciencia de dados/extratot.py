import socket
import time

# Configuração do Servidor (Redes)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 5000))
servidor.listen(1)

print("Aguardando conexão da Terra...")
conexao, endereco = servidor.accept()

while True:
    dados = conexao.recv(1024).decode()
    if not dados: break

    print(f"\n[Sonda] Comando '{dados}' chegou!")

    # Lógica de SO: Prioridade de Execução
    if dados == "INICIAR_PERFURACAO":
        print("[Sonda] Ligando motores... Estabilizando tripé...")
        time.sleep(1)  # Simulando tempo de processamento

    # Enviando confirmação de volta (mais 2 segundos de volta)
    time.sleep(2)
    conexao.send(f"Comando {dados} executado com sucesso.".encode())

conexao.close()