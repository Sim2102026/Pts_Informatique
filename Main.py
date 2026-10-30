#Ne pas oublier la commande pip
import pygame
import os
pygame.display.init()
ground=pygame.image.load(os.path.join('Assets', 'Background_test.png'))
flags=pygame.SCALED|pygame.RESIZABLE
screen = pygame.display.set_mode((1600, 900),flags,depth=0, display=0, vsync=1)
clock = pygame.time.Clock()
running = True


#pygame.image.load(os.path.join('/home/Overthemoon117/Documents/Ecole/Isep/I2/Informatique/Pts_info/Pts_Informatique/', 'Background.png'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(ground, (0, 0))
    pygame.display.flip()

    clock.tick(60)
pygame.display.update()
driver=pygame.display.get_driver()
print(driver)
pygame.quit()

