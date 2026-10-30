import pygame
import os
import Objets.Images
import Objets.Player
import Objets.Ennemi as emi
import Objets.plateforme as pform

pygame.init()
pygame.display.init()
ground=pygame.image.load(os.path.join('Assets', 'Background_test+base.png'))
flags=pygame.SCALED|pygame.RESIZABLE
screen = pygame.display.set_mode((1600, 900),flags,depth=0, display=0, vsync=1)
clock = pygame.time.Clock()
running = True

surface = pygame.display.set_mode((0,0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(ground, (0, 0))
    #print(Objets.Images.player_im)

    #AFFICHER LE JOUEUR SUR ECRAN
    Im_player = Objets.Images.player_im
    Im_player_resize = pygame.transform.scale(Im_player, (100, 100))
    Objets.Player.player = Objets.Player.Player(Objets.Player.position_player,Im_player_resize, "Jean", 3, 0)
    screen.blit(Im_player_resize,(50,744))

    #AFFICHER blocks avec la boucle FOR
    block = Objets.Images.block
    block_resize = pygame.transform.scale(block, (100, 100))
    block = pform.Plateforme(pform.position, block_resize, "block", )
    #8 blocks
    for i in range(1,9):
        screen.blit(block_resize, (300+i*100,600))
        i=i+1
    #3 blocks
    for i in range(1,4):
        screen.blit(block_resize, (700+i*100,400))
        i=i+1

    ennemi1_resize=pygame.transform.scale(Objets.Images.ennnemi1, (100, 100))
    ennemi1=emi.Ennemi(emi.position,ennemi1_resize,"ennemi_n°1",1)
    screen.blit(ennemi1.image,(1400,744))
    ennemi2_resize = pygame.transform.scale(Objets.Images.ennnemi2, (100, 100))
    ennemi2 = emi.Ennemi(emi.position, ennemi2_resize, "ennemi_n°2", 1)
    screen.blit(ennemi2.image, (1400, 200))
    ennemi3_resize = pygame.transform.scale(Objets.Images.ennnemi3, (100, 100))
    ennemi3 = emi.Ennemi(emi.position, ennemi3_resize, "ennemi_n°3", 1)
    screen.blit(ennemi3.image, (1400, 472))


    #AFFICHER UN RECTANGLE
    clc = pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(0, 0, 100, 100))
    pygame.display.flip()

    clock.tick(60)

pygame.display.update()
driver=pygame.display.get_driver()
print(driver)
pygame.quit()

