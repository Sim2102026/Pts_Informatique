import pygame
class Plateforme(pygame.sprite.Sprite):
    def __init__(self,position,image,name):
        pygame.sprite.Sprite.__init__(self)
        self.position=position
        self.image=image
        self.name=name
        pygame.sprite.collide_rect(image,image)
        if pygame.sprite.collide_rect(image,image)==True:
            print("ok")

position=[(300,200)]
