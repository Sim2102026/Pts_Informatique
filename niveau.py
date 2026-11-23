"""La classe Niveau : construit le niveau à partir d'une "carte" en texte.

Chaque caractère de la carte est une case de 48x48 pixels :
    X = bloc de terrain      P = départ du joueur
    E = ennemi               F = fruit
    D = trophée d'arrivée    . = vide
"""
import pygame

import config
from outils import charger_image
from plateforme import Plateforme
from ennemi import Ennemi
from piece import Piece
from arrivee import Arrivee
from soin import Soin
from porte import Porte

from carte_longue import CARTE_LONGUE

CARTE = CARTE_LONGUE


class Niveau:
    # Niveau n'hérite de rien : il CONTIENT des groupes de sprites (composition).

    def __init__(self, carte=CARTE):
        if not carte or not carte[0] or len({len(ligne) for ligne in carte}) != 1:
            raise ValueError("La carte doit etre rectangulaire et non vide")
        self.largeur = len(carte[0]) * config.TAILLE_TUILE
        self.hauteur = len(carte) * config.TAILLE_TUILE
        terrain = charger_image("Terrain", "Terrain (16x16).png")
        self.image_bloc = terrain.subsurface(pygame.Rect(96, 0, 48, 48))

        self.plateformes = pygame.sprite.Group()
        self.ennemis = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()
        self.soins = pygame.sprite.Group()
        self.arrivee = pygame.sprite.Group()
        self.portes = pygame.sprite.Group()
        self.position_depart = (0, 0)

        self.construire(carte)
        for ennemi in self.ennemis:
            ennemi.largeur_monde = self.largeur

    def construire(self, carte):
        t = config.TAILLE_TUILE
        # On colle le niveau en bas de l'écran (640 - 13 x 48 = 16 pixels de marge en haut)
        decalage = config.HAUTEUR - len(carte) * t

        # enumerate donne à la fois le numéro (ligne) et le contenu (texte)
        for ligne, texte in enumerate(carte):
            for colonne, case in enumerate(texte):
                x = colonne * t
                y = ligne * t + decalage
                bas_de_case = y + t   # pour poser les grands sprites (64 px) sur le sol

                if case == "X":
                    self.plateformes.add(Plateforme(x, y, self.image_bloc))
                elif case == "P":
                    self.position_depart = (x, bas_de_case - 64)
                elif case == "E":
                    self.ennemis.add(Ennemi(x, bas_de_case - 64))
                elif case == "F":
                    piece = Piece(x, y)
                    piece.rect.center = (x + t // 2, y + t // 2)   # centré dans la case
                    self.pieces.add(piece)
                elif case == "H":
                    self.soins.add(Soin(x + t // 2, y + t // 2))
                elif case == "D":
                    self.arrivee.add(Arrivee(x, bas_de_case - 64))
                elif case == "T":
                    self.portes.add(Porte(x + t // 2, bas_de_case))

    def dessiner(self, ecran, camera=None):
        """Dessine tout le décor, du fond vers l'avant."""
        for groupe in (self.portes, self.plateformes, self.arrivee, self.pieces, self.ennemis, self.soins):
            if camera is None:
                groupe.draw(ecran)
            else:
                camera.dessiner_groupe(ecran, groupe)
