"""Petites fonctions utiles pour charger et découper les images de l'asset."""
import os
import pygame

from config import DOSSIER_ASSETS


def charger_image(*chemin):
    """Charge une image du dossier assets.

    Exemple : charger_image("Background", "Blue.png")
    L'étoile (*chemin) permet de donner autant de morceaux de chemin qu'on veut.
    """
    chemin_complet = os.path.join(DOSSIER_ASSETS, *chemin)
    image = pygame.image.load(chemin_complet)
    # convert_alpha() rend l'affichage plus rapide et garde la transparence.
    # Elle ne marche que si une fenêtre est déjà ouverte, d'où le "if".
    if pygame.display.get_surface() is not None:
        image = image.convert_alpha()
    return image


def decouper_planche(planche, largeur, hauteur):
    """Découpe une "planche" (sprite sheet) en une liste de petites images.

    Dans l'asset, une animation est une seule longue image :
    par exemple "Run (32x32).png" fait 384x32 pixels = 12 images de 32x32
    collées les unes à côté des autres. Cette fonction les sépare.
    """
    images = []
    nb_images = planche.get_width() // largeur   # // = division entière
    for i in range(nb_images):
        # Rect(x, y, largeur, hauteur) = le rectangle à "photocopier"
        zone = pygame.Rect(i * largeur, 0, largeur, hauteur)
        images.append(planche.subsurface(zone))
    return images


def agrandir(image, echelle):
    """Agrandit une image (pixel art => on multiplie la taille par un entier)."""
    nouvelle_taille = (image.get_width() * echelle, image.get_height() * echelle)
    return pygame.transform.scale(image, nouvelle_taille)
