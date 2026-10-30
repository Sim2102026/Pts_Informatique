import Pts_Informatique.Objets.Images
from Pts_Informatique.Objets.Images import player_im
import os

class Player:
    def __init__(self,position,image,name,life,compteur_piece):
        self.position=position
        self.image=image
        self.name=name
        self.life=life
        self.compteur_piece=compteur_piece

position=[()]
player=Player(position,player_im,"Jean",3,0)
