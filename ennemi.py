"""La classe FILLE Ennemi : une Entite qui fait des allers-retours toute seule."""
import pygame

import config
from entite import Entite
from joueur import charger_animations_personnage


class Ennemi(Entite):

    def __init__(self, x, y, animations=None):
        if animations is None:
            # L'asset n'a pas de vrais ennemis : on prend un autre personnage.
            animations = charger_animations_personnage("Mask Dude")
        super().__init__(x, y, animations)
        self.vitesse_x = config.VITESSE_ENNEMI   # il part vers la droite

    def faire_demi_tour(self):
        self.vitesse_x = -self.vitesse_x         # on inverse le signe

    def toucher_mur(self):
        """REDÉFINITION : dans Entite, cette méthode ne fait rien.
        Pour un ennemi, toucher un mur = faire demi-tour."""
        self.faire_demi_tour()

    def choisir_animation(self):
        return "run"

    def vide_devant(self, plateformes):
        """Y a-t-il un trou juste devant ses pieds ?"""
        if self.vitesse_x > 0:
            x = self.rect.right + 1   # juste à droite
        else:
            x = self.rect.left - 1    # juste à gauche
        y = self.rect.bottom + 1      # juste sous les pieds
        for bloc in plateformes:
            if bloc.rect.collidepoint(x, y):
                return False          # il y a un bloc : pas de vide
        return True

    def update(self, plateformes):
        super().update(plateformes)   # gravité, déplacement, animation (la mère)
        # Règles en plus, propres à l'ennemi :
        if self.au_sol and self.vide_devant(plateformes):
            self.faire_demi_tour()    # ne pas tomber de sa plateforme
        if self.rect.left < 0 or self.rect.right > config.LARGEUR:
            self.faire_demi_tour()    # ne pas sortir de l'écran
