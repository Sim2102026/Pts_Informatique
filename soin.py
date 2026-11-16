"""Coeur à ramasser : animation visuelle et collecte conditionnelle."""
from pathlib import Path
import math
import pygame


class Soin(pygame.sprite.Sprite):
    def __init__(self, centre_x, centre_y):
        super().__init__()
        chemin = Path(__file__).resolve().parent / "Assets" / "HUD" / "heart.png"
        image = pygame.image.load(str(chemin))
        # Retirer la marge transparente pour une collision proche du dessin.
        image = image.subsurface(image.get_bounding_rect()).copy()
        self.image = pygame.transform.smoothscale(image, (30, 30))
        self.rect = self.image.get_rect(center=(centre_x, centre_y))
        self.centre_y = centre_y
        self.temps = 0.0

    def update(self, dt=0):
        """dt : secondes de jeu écoulées ; pas d'avancée pendant les menus."""
        self.temps += dt
        self.rect.centery = round(self.centre_y + 4 * math.sin(self.temps * 3))

    def ramasser(self, joueur):
        """Ne disparaît que si le joueur a effectivement récupéré une vie."""
        if joueur.soigner():
            self.kill()
            return True
        return False
