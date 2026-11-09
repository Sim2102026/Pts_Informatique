import os
import pygame
import time
import unittest
player_im=pygame.image.load(os.path.join('Assets', 'Player.png'))
#Mettre unittest
position_player=[50, 744]
x =position_player[0]
y=position_player[1]
class Player:
    def __init__(self,position,image,name,life,compteur_piece):
        self.position=position
        self.image=image
        self.name=name
        self.life=life
        self.compteur_piece=compteur_piece
        x = position_player[0]
        y = position_player[1]
    #ICI il faudra réorganiser le code, Les attributs de la classe Player doivent contenir un attribut x et y
    def move_right(self):
        print("right arrow")
        dx = 10
        pass

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
