import pygame
import os
import unittest


import Objets.Images
import Objets.Player
import Objets.Ennemi as emi
import Objets.plateforme as pform
import Objets.Camera as cam
import Objets.Collision as col
import time
pygame.init()
pygame.display.init()
ground=pygame.image.load(os.path.join('Assets', 'Background_test+base.png'))
WIDTH = 1280
HEIGHT = 720
flags=pygame.RESIZABLE
pygame.display.set_caption("Isep_plateforme")
screen = pygame.display.set_mode((WIDTH, HEIGHT),flags,depth=0, display=0, vsync=1)
clock = pygame.time.Clock()
running = True
player = Objets.Player.create_player("Jean",50,570,3,0)
camera = cam.Camera(WIDTH, HEIGHT)
SIZE = (50, 50)

surface = pygame.display.set_mode((0,0))
block_image = pygame.transform.scale(Objets.Images.block,SIZE)

ennemi1_image = pygame.transform.scale(Objets.Images.ennnemi1,SIZE)

ennemi2_image = pygame.transform.scale(Objets.Images.ennnemi2,SIZE)

ennemi3_image = pygame.transform.scale(Objets.Images.ennnemi3,SIZE)

ennemi1 = emi.Ennemi([1180, 570],ennemi1_image,"ennemi_n°1",1)

ennemi2 = emi.Ennemi([1180, 180],ennemi2_image,"ennemi_n°2",1)

ennemi3 = emi.Ennemi([1180, 430],ennemi3_image,"ennemi_n°3",1)

platforms = []
for i in range(-1, 40):
    platforms.append(pform.Plateforme([i * 50, 620],block_image,"block") )

for i in range(1, 9):
    platforms.append(pform.Plateforme([200 + i * 50, 480],block_image,"block"))

for i in range(1, 4):
    platforms.append(pform.Plateforme([600 + i * 100, 280],block_image,"block"))

collision = col.Collision()
while running:


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_f:
                collision.toggle_hitbox()

            if event.key == pygame.K_SPACE:
                player.jump()
    keys=pygame.key.get_pressed()
    # déplace joueur à droite
    if keys[pygame.K_RIGHT]:
        player.move_right()
        fps = clock.get_fps()
        print(f"FPS: {fps:.2f}")
    # déplace joueur à gauche
    elif keys[pygame.K_LEFT]:
        print("right arrow")
        player.move_left()
        fps = clock.get_fps()
        print(f"FPS: {fps:.2f}")

    else:
        player.stop_horizontal()
    player.physics()

    collision.move_player(player,platforms)

    camera.update(player)

    screen.fill((0, 0, 0))

    screen.blit(pygame.transform.scale(ground, (WIDTH, HEIGHT)),(-int(camera.offset_x), -int(camera.offset_y)))

    for platform in platforms:
        screen.blit(platform.image,camera.apply(platform.rect))

    for ennemi in [ennemi1, ennemi2, ennemi3]:
        screen.blit(ennemi.image,camera.apply(ennemi.rect))

    screen.blit(player.image,camera.apply(player.rect))

    if collision.show_hitbox:

        for obj in [player, ennemi1, ennemi2, ennemi3] + platforms:
            pygame.draw.rect(screen,(255, 0, 0),camera.apply(obj.rect),2)

    pygame.display.flip()
    pygame.display.update()

    clock.tick(30)
driver=pygame.display.get_driver()
print(driver)
pygame.quit()

