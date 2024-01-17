import pygame
from sys import exit
import random

pygame.init()

l = 1200
h = 700
dislay = pygame.display.set_mode((l, h))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
font1 = pygame.font.Font("./art/font/font1.ttf", 50)
font2 = pygame.font.Font("./art/font/font1.ttf", 100)

# Variabili di controllo
max_healt = 5 # Numero Cuori
gravity_speed = 1
snail_speed = 7 # Velocità chiocciola
potion_speed = 3 # Velocità pozione
score_seconds = 2 # Ogni quanti secondi il gioco ti da un punto

score = 0
healt = max_healt
game_state = 0
ctrl = False
timeSlicePotion = 0
timeSliceSnail = 0
firstTimeCollisionPotion = True
firstTimeCollisionSnail = True
newTick = score_seconds*1000

healt_surface = pygame.image.load("art/graphics/healt.png")
healt_surface = pygame.transform.rotozoom(healt_surface, 0, 2)

bg_surface = pygame.image.load("art/graphics/terrain/bg.png").convert_alpha()
bg_surface = pygame.transform.rotozoom(bg_surface, 0, 4)

ground_surface = pygame.image.load("art/graphics/terrain/ground.png").convert_alpha()
ground_surface = pygame.transform.rotozoom(ground_surface, 0, 2)

#Potion
potion = pygame.image.load("./art/graphics/potion.png")
potion_rect = potion.get_rect(midbottom=(500, 578))

# Snail
snail = pygame.image.load("./art/graphics/enemy/snail.png").convert_alpha()
snail = pygame.transform.scale(snail, (90, 50))
snail_rect = snail.get_rect(midbottom=(1150, 578))

mob_rect_list  = []

# PG
player = pygame.image.load("./art/graphics/player/walk.png").convert_alpha()
player = pygame.transform.rotozoom(player, 0, 2)
player_rect = player.get_rect(midbottom=(100, 578))
player_gravity = 0

go_surface = font2.render("GAME OVER!", False, "White")
go_img = pygame.image.load("./art/graphics/skull.png")
restart_surface = font1.render("Premi R per riavviare il gioco", False, "White")

entity_timer = pygame.USEREVENT + 1
pygame.time.set_timer(entity_timer, 900)

while True:
    if game_state == 0 :
        # Gioco principale

        r = random.randint(0,10)

        record = int(open("record.txt", "r").readline())
        if (score > record):
            open("record.txt", "w").write(str(score))

        score_surface = font1.render(f"Punteggio: {score}", False, "White")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Salto
                    if player_rect.bottom >= 578:
                        player_gravity = -22
                if event.key == pygame.K_k : # Tasto del suicidio
                        healt = 0

            if event.type == entity_timer:
                if r==0 :
                    dislay.blit(potion, potion_rect)
                    print("A")

        #potion_rect.x -= potion_speed
        #if (potion_rect.right < 0):
        #    potion_rect.left = 1200

        snail_rect.x -= snail_speed #Movimento lumaca asse X

        # Render IMG
        dislay.blit(bg_surface, (0, 0))
        dislay.blit(ground_surface, (0, 0))
        dislay.blit(snail, snail_rect)

        # Player
        player_gravity += gravity_speed
        player_rect.y += player_gravity
        if player_rect.bottom >= 578: player_rect.bottom = 578
        dislay.blit(player, player_rect)

        # Render Font
        dislay.blit(score_surface, (25, 5))
        # (25, 50)

        # Mostra cuori
        for i in range(healt):
            dislay.blit(healt_surface, ((l - 80) - i * 50, 0))

        # Effetto Pac Man lumaca
        #if (snail_rect.right < 0):
        #    snail_rect.left = 1200

        # Aggiunta punti ogni TOT secondi
        if (pygame.time.get_ticks() > newTick) :
            score+=1
            newTick += score_seconds*1000

        # Giocatore raccoglie pozione
        if (player_rect.colliderect(potion_rect)) :
            if firstTimeCollisionPotion == True :
                healt+=1
                firstTimeCollisionPotion = False
            else :
                if (ctrl == False):
                    timeSlicePotion = pygame.time.get_ticks()

                if (pygame.time.get_ticks() >= timeSlicePotion + 3000):
                    ctrl = False
                    healt+=1
                else:
                    ctrl = True

        # Lumaca colpisce il giocatore
        if (player_rect.colliderect(snail_rect)):
            if firstTimeCollisionSnail == True :
                healt-=1
                firstTimeCollisionSnail = False
            else :
                if (ctrl == False):
                    timeSliceSnail = pygame.time.get_ticks()

                if (pygame.time.get_ticks() >= timeSliceSnail + 3000):
                    ctrl = False
                    healt-=1
                else:
                    ctrl = True

        # Controllo Game Over
        if (healt<=0) :
            game_state = 1

    elif game_state == 1 :
        # Menù di morte

        record_surface = font1.render(f"Record: {record}", False, "Gold")
        dislay.fill((33, 33, 33))
        dislay.blit(go_surface, (l*0.5-200, h*0.5-175))
        dislay.blit(go_img, (l*0.5-50, h*0.5-50))
        dislay.blit(restart_surface, (l * 0.5 - 310, h * 0.5 + 100))
        dislay.blit(score_surface, (l * 0.5 - 120, h * 0.5 + 200))
        dislay.blit(record_surface, (l * 0.5 - 107, h * 0.5 + 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r :
                    game_state = 0
                    score = 0
                    snail_rect.left = 1200
                    healt = max_healt

    pygame.display.update()
    clock.tick(60)  # esegui il ciclo un massimo di 60 volte al secondo