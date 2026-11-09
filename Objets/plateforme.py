import pygame
import unittest
class Plateforme(pygame.sprite.Sprite):
    def __init__(self,position,image,name):
        pygame.sprite.Sprite.__init__(self)
        self.position=position
        self.image=image
        self.name=name



position=[(300,200)]
