import pygame
import os
import Objets.Images
import Objets.Player
import Objets.Ennemi as emi
import Objets.plateforme as pform
import time
pygame.init()
pygame.display.init()
ground=pygame.image.load(os.path.join('Assets', 'Background_test+base.png'))
flags=pygame.SCALED|pygame.RESIZABLE
screen = pygame.display.set_mode((1600, 900),flags,depth=0, display=0, vsync=1)
clock = pygame.time.Clock()
running = True

surface = pygame.display.set_mode((0,0))
# print(Objets.Images.player_im)

# AFFICHER LE JOUEUR SUR ECRAN
Im_player = Objets.Images.player_im
Im_player_resize = pygame.transform.scale(Im_player, (100, 100))
Objets.Player.player = Objets.Player.Player(Objets.Player.position_player, Im_player_resize, "Jean", 3, 0)

# AFFICHER blocks avec la boucle FOR
block = Objets.Images.block
block_resize = pygame.transform.scale(block, (100, 100))
block = pform.Plateforme(pform.position, block_resize, "block", )

ennemi1_resize = pygame.transform.scale(Objets.Images.ennnemi1, (100, 100))
ennemi1 = emi.Ennemi(emi.position, ennemi1_resize, "ennemi_n°1", 1)
ennemi2_resize = pygame.transform.scale(Objets.Images.ennnemi2, (100, 100))
ennemi2 = emi.Ennemi(emi.position, ennemi2_resize, "ennemi_n°2", 1)
ennemi3_resize = pygame.transform.scale(Objets.Images.ennnemi3, (100, 100))
ennemi3 = emi.Ennemi(emi.position, ennemi3_resize, "ennemi_n°3", 1)

# AFFICHER UN RECTANGLE
clc = pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(0, 0, 100, 100))
x = Objets.Player.position_player[0]
while running:
    screen.blit(ground, (0, 0))
    #x →la position sur l'axe x du joueur
    player=screen.blit(Im_player_resize, (x, 744))
    # 8 blocks
    for i in range(1, 9):
        screen.blit(block_resize, (300 + i * 100, 600))
        i = i + 1
    # 3 blocks
    for i in range(1, 4):
        screen.blit(block_resize, (700 + i * 100, 400))
        i = i + 1
    screen.blit(ennemi1.image, (1400, 744))
    screen.blit(ennemi2.image, (1400, 200))
    screen.blit(ennemi3.image, (1400, 472))
    keys=pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # déplace joueur à droite
    if keys[pygame.K_RIGHT]:
        print("right arrow")
        dx = (time.clock_gettime(keys[pygame.K_RIGHT]) / 1000)
        print(time.clock_gettime(keys[pygame.K_RIGHT]))
        x = x + dx
        fps = clock.get_fps()
        print(f"FPS: {fps:.2f}")
    # déplace joueur à gauche
    if keys[pygame.K_LEFT]:
        print("right arrow")
        dx = -(time.clock_gettime(keys[pygame.K_LEFT]) / 1000)
        print(time.clock_gettime(keys[pygame.K_LEFT]))
        x = x + dx
        fps = clock.get_fps()
        print(f"FPS: {fps:.2f}")
    pygame.display.flip()
    pygame.display.update()

    clock.tick(30)
driver=pygame.display.get_driver()
print(driver)
pygame.quit()

