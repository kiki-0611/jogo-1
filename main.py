import pygame
import pgzrun
import random

WIDTH = 800
HEIGHT = 600
TITLE = "Primeiro GAAAMEEEE no Pygame Zero"
estado_jogo = "JOGANDO"
waypoint_atual = 0 

waypoints =[
    (650, 450),
    (650,120),
    (480,120),
    (480,450)
]

def redimenssionar(ator,altura):
    escala = altura / ator.height
    novo= pygame.transform.smoothscale(
        ator._orig_surf, (int(ator.width*escala),altura))
    ator._orig_surf = ator._surf = novo
    ator._update_pos()

pikomon = Actor("mimikyu pixelated!")
pikomon = Actor("mimikyu pixelated!",(100,100))
redimenssionar(pikomon,100)

comida = Actor ("8233211828682191")
comida = Actor ("8233211828682191", (400, 300))
redimenssionar(comida,50)

pokeboll = Actor ("3166662230476540",(700,500))
redimenssionar(pokeboll,100)

pontos = 0  

def perseguicao_pokeboll():
    if estado_inimigo =="perseguicao"
        if pikomon.x > pokeboll.x:
            pokeboll.x = pokeboll.x + 0.8
        if pikomon.x < pokeboll.x:
            pokeboll.x = pokeboll.x - 0.8
        if pikomon.y > pokeboll.y:
            pokeboll.y = pokeboll.y + 0.8
        if pikomon.y < pokeboll.y:
            pokeboll.y = pokeboll.y - 0.8
    elif estado_inimigo == "patrulha":
        alvo_x,alvo_y = waypoints [waypoints_atual]
        dist_waypoint+ math.hyplot (alvo_x - inimigo.x, alvo_y - iimigo.y)
    if dist_waypoint < 10:
        waypoint_atual = (waypoint_atual + 1) %len (waypoints)
        alvo_x,alvo_y = waypoints [waypoint_atual]




def update():
    global pontos, estado_jogo
    if keyboard.d:
        pikomon.x += 2
    if keyboard.a:
        pikomon.x -= 2
    if keyboard.w:
        pikomon.y -= 2
    if keyboard.s:
        pikomon.y +=  2

    perseguicao_pokeboll ()
    
    if pikomon.colliderect(comida):
        comida.x = random.randint (50, WIDTH - 50)
        comida.y = random.randint (50, HEIGHT - 50)
        pontos = pontos + 1

    if pikomon.colliderect(pokeboll):
        pokeboll.x = random.randint (50, WIDTH - 50)
        pokeboll.y = random.randint (50, HEIGHT - 50)
        pontos = pontos - 1

    if pontos >= 10:
        estado_jogo = "VITORIA"

    if estado_jogo == "VITORIA":
        if keyboard.r:
            pontos = 0 
            pikomon.pos = (100,100)
            comida.pos = (400,300)
            pokeboll.pos = (700,500)
            estado_jogo = "JOGANDO"
def draw():
    screen.fill ((0,0,255))

    if estado_jogo == "JOGANDO":
        pikomon.draw()
        comida.draw()
        pokeboll.draw()
        screen.draw.text (f"Pontos: {pontos}",(20,20),fontsize=36, color="yellow")

        
    
    elif estado_jogo == "VITORIA":
        screen.draw.text (f"VOCE VENCEU!!!!!!!!",center=(WIDTH/2,220),fontsize=36, color="yellow")
        screen.draw.text (f"Aperte R para reiniciar", midbottom=(WIDTH/2,500),fontsize=36, color="yellow")


pgzrun.go()