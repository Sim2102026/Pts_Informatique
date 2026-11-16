"""Réglages du jeu, rangés au même endroit.

Si on veut changer la taille de la fenêtre ou la vitesse du jeu,
on le fait ici, une seule fois, au lieu de chercher partout dans le code.
"""
import os

# --- Fenêtre ---
LARGEUR = 960          # largeur de la fenêtre en pixels
HAUTEUR = 640          # hauteur de la fenêtre en pixels
TITRE = "Mon Platformer"
FPS = 60               # images par seconde (vitesse de la boucle)

# --- Images ---
TAILLE_PERSO = 32      # les personnages de l'asset font 32x32 pixels
ECHELLE = 2            # on agrandit tout x2, sinon c'est minuscule à l'écran

# Dossier où se trouve l'asset (le dossier "assets" à côté de ce fichier).
# os.path.dirname(__file__) = le dossier qui contient config.py.
DOSSIER_ASSETS = os.path.join(os.path.dirname(__file__), "assets")

# --- Décor ---
TAILLE_TUILE = 48      # un bloc de terrain fait 48x48 pixels

# --- Physique ---
GRAVITE = 0.8          # vitesse ajoutée vers le bas à chaque frame
VITESSE_CHUTE_MAX = 15 # on ne tombe jamais plus vite que ça
VITESSE_JOUEUR = 5     # pixels parcourus par frame quand on court
FORCE_SAUT = 17        # vitesse vers le haut au moment du saut (≈ 3,5 blocs de haut)

# --- Ennemis, fruits, vies (étape 3) ---
VITESSE_ENNEMI = 2     # les ennemis marchent moins vite que le joueur
VIES_DEPART = 3
DUREE_INVINCIBLE = 90  # frames d'invincibilité après un coup (1,5 s)
REBOND = 10            # petit saut quand on écrase un ennemi
POINTS_FRUIT = 10
POINTS_ENNEMI = 50
