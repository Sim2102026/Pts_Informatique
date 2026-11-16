"""Petites fonctions partagées par plusieurs fichiers de test."""
import pygame

from plateforme import Plateforme


def fausses_animations(noms=("idle", "run", "jump", "fall", "hit"), nb_images=4):
    """Des animations "bidon" (carrés de 64x64) : pas besoin de l'asset
    pour tester la logique."""
    return {nom: [pygame.Surface((64, 64)) for _ in range(nb_images)] for nom in noms}


def sol(y=500, largeur=1000):
    """Un groupe contenant une grande plateforme horizontale."""
    groupe = pygame.sprite.Group()
    groupe.add(Plateforme(0, y, pygame.Surface((largeur, 48))))
    return groupe


class FauxClavier(dict):
    """Imite pygame.key.get_pressed() : une touche absente vaut False."""
    def __missing__(self, touche):
        return False
