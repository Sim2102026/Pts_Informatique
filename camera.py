"""Caméra horizontale : coordonnées du monde -> coordonnées de l'écran."""
import pygame


class Camera:
    def __init__(self, largeur_ecran, largeur_monde):
        self.largeur_ecran = largeur_ecran
        self.largeur_monde = largeur_monde
        self.offset_x = 0

    def update(self, cible):
        # Au début : caméra fixe. Au milieu : le joueur reste centré.
        # À la fin : la caméra s'arrête au bord droit de la carte.
        souhaite = cible.rect.centerx - self.largeur_ecran // 2
        maximum = max(0, self.largeur_monde - self.largeur_ecran)
        self.offset_x = max(0, min(souhaite, maximum))

    def appliquer(self, rect):
        # move renvoie une COPIE : ne jamais déplacer les rects de collision.
        return rect.move(-self.offset_x, 0)

    def dessiner_groupe(self, ecran, groupe):
        zone = ecran.get_rect()
        for sprite in groupe:
            destination = self.appliquer(sprite.rect)
            if zone.colliderect(destination):
                ecran.blit(sprite.image, destination)
