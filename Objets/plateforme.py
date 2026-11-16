import pygame
import unittest
position = [0, 0]
class Plateforme(pygame.sprite.Sprite):
    def __init__(self,position,image,name):
        pygame.sprite.Sprite.__init__(self)
        self.position=position
        self.image=image
        self.name=name
        self.x = position[0]
        self.y = position[1]

        self.width = image.get_width()
        self.height = image.get_height()

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        def update(self):
            self.position[0] = self.x
            self.position[1] = self.y

            self.rect.x = self.x
            self.rect.y = self.y

        def draw(self, screen):
            screen.blit(self.image,self.rect)


