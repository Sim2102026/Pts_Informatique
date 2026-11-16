import pygame
import unittest

class Collision:
    def __init__(self):
        self.show_hitbox = False

    def toggle_hitbox(self):
        self.show_hitbox = not self.show_hitbox

    def check(self, object1, object2):
        return object1.rect.colliderect(object2.rect)
#Le carré collision du joueur qui suit le déplacement du joueur
    def move_player(self, player, platforms):
        player.rect.x = player.x

        for platform in platforms:

            if player.rect.colliderect(platform.rect):

                if player.vitesse_x > 0:
                    player.rect.right = platform.rect.left

                elif player.vitesse_x < 0:
                    player.rect.left = platform.rect.right

                player.x = player.rect.x

        player.rect.y = player.y

        player.is_falling = True

        for platform in platforms:

            if player.rect.colliderect(platform.rect):

                if player.vitesse_y > 0:
                    player.rect.bottom = platform.rect.top
                    player.y = player.rect.y
                    player.vitesse_y = 0
                    player.is_jumping = False
                    player.is_falling = False

                elif player.vitesse_y < 0:
                    player.rect.top = platform.rect.bottom
                    player.y = player.rect.y
                    player.vitesse_y = 0

        player.update()

    def draw_hitbox(self, screen, obj):
        if self.show_hitbox:
            #hitbox rouge
            pygame.draw.rect(screen,(255, 0, 0),obj.rect,2)

    def draw_all_hitboxes(self, screen, objects):
        if self.show_hitbox:

            for obj in objects:
                self.draw_hitbox(screen, obj)

if __name__ == '__main__':
    pass
