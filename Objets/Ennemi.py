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


class Boss(Ennemi):
    pass

position=[(450,0)]
#ennemi1=Ennemi(position,Images.ennnemi1,"ennemi_n°1",1)