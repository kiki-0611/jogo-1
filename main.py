import pygame
import pgzrun
import random
import math

WIDTH = 800
HEIGHT = 600
TITLE = "Primeiro Game no Pygame Zero - Pikomon Quest"

# --- Redimensionamento Utilitário ---
def redimensionar(ator, altura):
    escala = altura / ator.height
    novo = pygame.transform.smoothscale(
        ator._orig_surf, (int(ator.width * escala), altura)
    )
    ator._orig_surf = ator._surf = novo
    ator._update_pos()

# --- Atores ---
pikomon = Actor("mimikyu pixelated!", (100, 100))
redimensionar(pikomon, 70)

comida = Actor("8233211828682191", (400, 300))
redimensionar(comida, 35)

pokeboll = Actor("3166662230476540", (650, 450))
redimensionar(pokeboll, 70)

# --- Obstáculos (Paredes) ---
paredes = [
    Rect((380, 80), (20, 180)),
    Rect((200, 360), (220, 20)),
    Rect((600, 200), (20, 180))
]

# --- Rota de Patrulha ---
waypoints = [
    (650, 450),
    (650, 120),
    (480, 120),
    (480, 450)
]
waypoint_atual = 0

# --- Estados e Variáveis ---
PONTOS_VITORIA = 10
VELOCIDADE_HEROI = 3
VELOCIDADE_BASE_INIMIGO = 1.2
PASSO_RAIO = 10
RAIO_VISAO_INIMIGO = 220

pontos = 0
vidas = 3
estado_jogo = "JOGANDO"

def tem_linha_de_visao(origem, destino, obstaculos=[], alcance_maximo=None):
    dx = destino.x - origem.x
    dy = destino.y - origem.y
    distancia = math.hypot(dx, dy)
    
    if alcance_maximo is not None and distancia > alcance_maximo:
        return False

    if distancia == 0:
        return True
        
    dir_x = dx / distancia
    dir_y = dy / distancia
    passos = int(distancia / PASSO_RAIO)
    
    for d in range(1, passos):
        ponto_x = origem.x + dir_x * (d * PASSO_RAIO)
        ponto_y = origem.y + dir_y * (d * PASSO_RAIO)
        for obs in obstaculos:
            if obs.collidepoint((ponto_x, ponto_y)):
                return False
                
    return True

def reiniciar_jogo():
    global pontos, vidas, estado_jogo, waypoint_atual
    pontos = 0
    vidas = 3
    pikomon.pos = (100, 100)
    comida.pos = (400, 300)
    pokeboll.pos = (650, 450)
    waypoint_atual = 0
    estado_jogo = "JOGANDO"

def mover_pokeboll():
    global waypoint_atual
    vel = VELOCIDADE_BASE_INIMIGO + (pontos // 5) * 0.3
    
    vendo_pikomon = tem_linha_de_visao(pokeboll, pikomon, paredes, RAIO_VISAO_INIMIGO)
    
    if vendo_pikomon:
        alvo_x, alvo_y = pikomon.x, pikomon.y
    else:
        alvo_x, alvo_y = waypoints[waypoint_atual]
        dist_waypoint = math.hypot(alvo_x - pokeboll.x, alvo_y - pokeboll.y)
        if dist_waypoint < 10:
            waypoint_atual = (waypoint_atual + 1) % len(waypoints)
            alvo_x, alvo_y = waypoints[waypoint_atual]

    dx = alvo_x - pokeboll.x
    dy = alvo_y - pokeboll.y
    dist = math.hypot(dx, dy)
    
    if dist > 0:
        pokeboll.x += (dx / dist) * vel
        pokeboll.y += (dy / dist) * vel

def sortear_posicao_valida():
    for _ in range(20):
        px = random.randint(60, WIDTH - 60)
        py = random.randint(60, HEIGHT - 60)
        temp_rect = Rect((px - 15, py - 15), (30, 30))
        if not any(temp_rect.colliderect(p) for p in paredes):
            return px, py
    return 100, 500

def update():
    global pontos, vidas, estado_jogo
    
    if estado_jogo in ["VITORIA", "GAMEOVER"]:
        if keyboard.r:
            reiniciar_jogo()
        return

    pos_ant_x, pos_ant_y = pikomon.x, pikomon.y

    if keyboard.d and pikomon.right < WIDTH:
        pikomon.x += VELOCIDADE_HEROI
    if keyboard.a and pikomon.left > 0:
        pikomon.x -= VELOCIDADE_HEROI
    if keyboard.w and pikomon.top > 0:
        pikomon.y -= VELOCIDADE_HEROI
    if keyboard.s and pikomon.bottom < HEIGHT:
        pikomon.y += VELOCIDADE_HEROI

        

    for p in paredes:
        if pikomon.colliderect(p):
            if pikomon.left < p.right and pikomon.x > p.x:
                pikomon.left = p.right
            if pikomon.right < p.left and pikomon.x < p.x:
                pikomon.right = p.left 
            if pikomon.bottom < p.top and pikomon.y < p.y:
                pikomon.bottom = p.top     
            if pikomon.top < p.bottom and pikomon.y > p.y:
                pikomon.top = p.bottom

    mover_pokeboll()

    if pikomon.colliderect(comida):
        pontos += 1
        px, py = sortear_posicao_valida()
        comida.pos = (px, py)
        if pontos >= PONTOS_VITORIA:
            estado_jogo = "VITORIA"

    if pikomon.colliderect(pokeboll):
        vidas -= 1
        if vidas <= 0:
            estado_jogo = "GAMEOVER"
        else:
            pokeboll.x = random.choice([60, WIDTH - 60])
            pokeboll.y = random.choice([60, HEIGHT - 60])

def draw():
    screen.fill((25, 30, 45))

    if estado_jogo == "JOGANDO":
        for parede in paredes:
            screen.draw.filled_rect(parede, (90, 100, 120))
            screen.draw.rect(parede, "cyan")

        for i, wp in enumerate(waypoints):
            screen.draw.filled_circle(wp, 3, "gold")
            prox_wp = waypoints[(i + 1) % len(waypoints)]
            screen.draw.line(wp, prox_wp, (50, 60, 80))

        screen.draw.circle(pokeboll.pos, RAIO_VISAO_INIMIGO, (255, 0, 0))
        
        if tem_linha_de_visao(pokeboll, pikomon, paredes, RAIO_VISAO_INIMIGO):
            screen.draw.line(pokeboll.pos, pikomon.pos, "red")

        pikomon.draw()
        comida.draw()
        pokeboll.draw()

        screen.draw.text(f"Pontos: {pontos}/{PONTOS_VITORIA}", topleft=(20, 20), fontsize=30, color="gold")
        cor_vida = "lime" if vidas > 1 else "red"
        screen.draw.text(f"Vidas: {'♥ ' * vidas}", topright=(WIDTH - 20, 20), fontsize=26, color=cor_vida)

    elif estado_jogo == "VITORIA":
        screen.draw.text("VOCÊ VENCEU!", center=(WIDTH // 2, 220), fontsize=50, color="lightgreen")
        screen.draw.text("Pressione [R] para jogar novamente", center=(WIDTH // 2, 350), fontsize=24, color="yellow")

    elif estado_jogo == "GAMEOVER":
        screen.draw.text("GAME OVER", center=(WIDTH // 2, 220), fontsize=60, color="crimson")
        screen.draw.text("Pressione [R] para tentar novamente", center=(WIDTH // 2, 350), fontsize=24, color="yellow")

pgzrun.go()
