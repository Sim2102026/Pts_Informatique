"""Decor et carte et collisions des plateformes"""

from pathlib import Path
import pygame

LARGEUR, HAUTEUR = 1024, 640
TAILLE_BLOC = 64
DOSSIER_ASSETS = Path(__file__).resolve().parent / "Assets" / "Kenney"

# Un caractere = une case de 64 pixels. Modifier cette liste pour changer le decor
# . : vide     # : terre     = : plateforme suspendue
CARTE = [
    "................",
    "................",
    "................",
    "...........===..",
    ".......===......",
    "................",
    "...===.......==.",
    "................",
    "########..######",
    "########..######",
]


def charger_image(nom, taille):
    image = pygame.image.load(str(DOSSIER_ASSETS / nom)).convert_alpha()
    return pygame.transform.smoothscale(image, taille)


class Environnement:
    def __init__(self):
        self.fond = charger_image("background_color_hills.png", (LARGEUR, HAUTEUR))
        self.fond.set_colorkey("white")  # Remplacer le blanc du fond par le ciel bleu.
        self.blocs = []          # Images et positions pour le dessin.
        self.plateformes = []    # Rectangles solides pour les collisions.
        textures = {}
        for nom in ["block_top", "block_top_left", "block_top_right", "block_center",
                    "horizontal_left", "horizontal_middle", "horizontal_right"]:
            textures[nom] = charger_image("terrain_grass_" + nom + ".png", (64, 64))

        for ligne, texte in enumerate(CARTE):
            for colonne, symbole in enumerate(texte):
                if symbole not in "#=":
                    continue
                gauche = colonne > 0 and texte[colonne - 1] == symbole
                droite = colonne < len(texte) - 1 and texte[colonne + 1] == symbole
                if symbole == "=":
                    nom = "horizontal_middle"
                    if not gauche:
                        nom = "horizontal_left"
                    elif not droite:
                        nom = "horizontal_right"
                elif ligne > 0 and CARTE[ligne - 1][colonne] == "#":
                    nom = "block_center"
                else:
                    nom = "block_top"
                    if not gauche:
                        nom = "block_top_left"
                    elif not droite:
                        nom = "block_top_right"
                rect = pygame.Rect(colonne * TAILLE_BLOC, ligne * TAILLE_BLOC, 64, 64)
                self.blocs.append((textures[nom], rect))
                self.plateformes.append(rect)

        self.decorations = []   # Decorations sans collision.
        for nom, position in [("bush.png", (384, 448)), ("sign_right.png", (128, 448)),
                              ("bush.png", (704, 448)), ("flag_green_a.png", (960, 448))]:
            self.decorations.append((charger_image(nom, (64, 64)), position))

    def est_au_sol(self, rect):
        # Le petit decalage permet de tester le contact avec le sol
        return rect.move(0, 1).collidelist(self.plateformes) != -1

    def deplacer(self, rect, dx, dy):
        """Modifie rect : d'abord X, puis Y. Renvoie (au_sol, choc_vertical)"""
        rect.x += round(dx)
        for plateforme in self.plateformes:
            if rect.colliderect(plateforme):
                if dx > 0:
                    rect.right = plateforme.left
                elif dx < 0:
                    rect.left = plateforme.right
        rect.x = max(0, min(rect.x, LARGEUR - rect.width))

        choc_vertical = False
        rect.y += round(dy)
        for plateforme in self.plateformes:
            if rect.colliderect(plateforme):
                if dy > 0:
                    rect.bottom = plateforme.top
                    choc_vertical = True
                elif dy < 0:
                    rect.top = plateforme.bottom
                    choc_vertical = True
        return self.est_au_sol(rect), choc_vertical

    def dessiner(self, ecran):
        ecran.fill((195, 227, 255))
        ecran.blit(self.fond, (0, 0))
        for image, position in self.decorations:
            ecran.blit(image, position)
        for image, rect in self.blocs:
            ecran.blit(image, rect)
