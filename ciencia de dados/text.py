import pygame

# 1. Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Jogo de Hogwarts")

# Cores (RGB)
COR_FUNDO = (30, 30, 30)
COR_BRUXO = (100, 50, 150)  # Um roxo místico

# 2. Atributos do Personagem
# x, y, largura, altura
jogador = pygame.Rect(400, 300, 40, 40)
velocidade = 5

clock = pygame.time.Clock()  # Para controlar o FPS
rodando = True

# 3. Game Loop
while rodando:
    # --- Entradas (Eventos)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # --- Lógica de Movimento (Teclado)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= velocidade
    if teclas[pygame.K_RIGHT] and jogador.x < LARGURA - jogador.width:
        jogador.x += velocidade
    if teclas[pygame.K_UP] and jogador.y > 0:
        jogador.y -= velocidade
    if teclas[pygame.K_DOWN] and jogador.y < ALTURA - jogador.height:
        jogador.y += velocidade

    # --- Desenho (Render)
    tela.fill(COR_FUNDO)  # Limpa a tela

    # Desenha o bruxo
    pygame.draw.rect(tela, COR_BRUXO, jogador)

    pygame.display.flip()  # Atualiza a tela
    clock.tick(60)  # Crava o jogo em 60 frames por segundo

pygame.quit()