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

# 20 colonnes x 13 lignes = un écran de 960 x 624 pixels
CARTE = [
    "....................",
    "....................",
    "..............F..D..",
    ".............XXXXXX.",
    "....................",
    ".......F.E.F........",
    ".......XXXXX........",
    "....................",
    "....F.F........E.F..",
    "...XXXX......XXXXX..",
    "....................",
    ".P......F....E......",
    "XXXXXXXXX..XXXXXXXXX",
]


class Niveau:
    # Niveau n'hérite de rien : il CONTIENT des groupes de sprites (composition).

    def __init__(self, carte=CARTE):
        terrain = charger_image("Terrain", "Terrain (16x16).png")
        self.image_bloc = terrain.subsurface(pygame.Rect(96, 0, 48, 48))

        self.plateformes = pygame.sprite.Group()
        self.ennemis = pygame.sprite.Group()
        self.pieces = pygame.sprite.Group()
        self.arrivee = pygame.sprite.Group()
        self.position_depart = (0, 0)

        self.construire(carte)

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
                elif case == "D":
                    self.arrivee.add(Arrivee(x, bas_de_case - 64))

    def dessiner(self, ecran):
        """Dessine tout le décor, du fond vers l'avant."""
        self.plateformes.draw(ecran)
        self.arrivee.draw(ecran)
        self.pieces.draw(ecran)
        self.ennemis.draw(ecran)
