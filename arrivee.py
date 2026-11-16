"""L'arrivée (le trophée de l'asset) : la toucher fait gagner la partie."""
import pygame

from outils import charger_image


class Arrivee(pygame.sprite.Sprite):
    # Comme Plateforme, l'arrivée ne bouge pas et ne tombe pas :
    # ce n'est PAS une Entite, juste un Sprite.
    def __init__(self, x, y, image=None):
        super().__init__()
        if image is None:
            image = charger_image("Items", "Checkpoints", "End", "End (Idle).png")
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
