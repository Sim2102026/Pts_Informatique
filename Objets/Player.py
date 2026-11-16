import os
import pygame
import time
import unittest
player_im=pygame.image.load(os.path.join('Assets', 'Player.png'))
#Mettre unittest
position_player=[50, 620]

class Player:
    def __init__(self,position,image,name,life,compteur_piece):
        self.position=position
        self.image=image
        self.name=name
        self.life=life
        self.compteur_piece=compteur_piece
        self.x = position[0]
        self.y = position[1]
        self.speed = 50
        self.jump_force = 70
        self.gravity = 10
        self.vitesse_x = 0
        self.vitesse_y = 0
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.is_jumping = False
        self.is_falling = False
        self.is_alive = True
    #Réorganiser méthodes
    def move_right(self):
        print("right arrow")
        dx = 10
        x=Player.position[0]
        x=dx+x
        print(x)
        return x

    def move_up(self):
        print("bruh")
        time.sleep(2)
        d=-100


    def move_left(self):
        pass

    def collect_piece(self):
        pass

    def damage(self):
        pass
    def physics(self):
        pass
play_tets=Player(position_player, player_im, "Jean", 3, 0)
