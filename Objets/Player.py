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
    def update(self):
        self.rect.topleft = (self.x, self.y)
        self.position[0] = self.x
        self.position[1] = self.y
    def move_right(self):
        print("right arrow")
        dx = 10
        self.x += self.speed
        self.update()
        print(self.x)


    def move_up(self):
        if not self.is_jumping and not self.is_falling:
            self.vitesse_y = -self.jump_force
            self.is_jumping = True

    def move_left(self):
        self.x -= self.speed
        self.update()

    def stop_horizontal(self):
        self.vitesse_x = 0

    def jump(self):
        self.move_up()

# dessiner player dans la classe au lieu de main
    def draw(self, screen):
        screen.blit(self.image,self.rect)

    def collect_piece(self):
        pass

    def damage(self):
        pass
    def physics(self):
        self.vitesse_y += self.gravity
        self.y += self.vitesse_y

        if self.vitesse_y > 0:
            self.is_falling = True

        self.update()

    def reset(self):
        self.x = 50
        self.y = 620

        self.vitesse_x = 0
        self.vitesse_y = 0

        self.is_jumping = False
        self.is_falling = False

        self.life = 3
        self.compteur_piece = 0
        self.is_alive = True

        self.update()

def create_player(name="Jean",x=50,y=620,life=3,compteur_piece=0):
    image = pygame.transform.scale(player_im,(50, 50))

    return Player([x, y],image,name,life,compteur_piece)
player = create_player()