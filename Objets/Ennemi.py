import unittest
import pygame
class Ennemi:
    def __init__(self,position,image,name,life):
        self.position=position
        self.image=image
        self.name=name
        self.life=life
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
        screen.blit(self.image,(self.x, self.y))

    def damage(self, amount=1):
        self.life -= amount

        if self.life < 0:
            self.life = 0


class Boss(Ennemi):
    pass