#Ne pas oublier la commande pip
import pygame
import os
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True


#pygame.image.load(os.path.join('/home/Overthemoon117/Documents/Ecole/Isep/I2/Informatique/Pts_info/Pts_Informatique/', 'Background.png'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
