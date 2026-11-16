"""Tests de la classe AffichageSante (les coeurs de vie)."""
import pygame

import config
from affichage_sante import AffichageSante
from joueur import Joueur
from aides import fausses_animations


def creer_joueur():
    return Joueur(0, 0, fausses_animations())


def test_charge_les_images_des_coeurs():
    pygame.init()
    affichage = AffichageSante(maximum=3, taille=48)
    assert affichage.coeur.get_size() == (48, 48)
    assert affichage.coeur_vide.get_size() == (48, 48)


def test_dessiner_ne_plante_pas():
    pygame.init()
    ecran = pygame.Surface((config.LARGEUR, config.HAUTEUR))
    AffichageSante().dessiner(ecran, creer_joueur())


def test_perdre_une_vie_lance_l_animation_du_coeur():
    pygame.init()
    ecran = pygame.Surface((config.LARGEUR, config.HAUTEUR))
    affichage = AffichageSante(maximum=3)
    joueur = creer_joueur()
    affichage.dessiner(ecran, joueur)   # 3 vies : aucune animation
    joueur.vies = 2
    affichage.dessiner(ecran, joueur)   # 1 vie perdue : le 3e coeur clignote
    assert 2 in affichage.animations


def test_un_nouveau_joueur_efface_les_animations():
    pygame.init()
    ecran = pygame.Surface((config.LARGEUR, config.HAUTEUR))
    affichage = AffichageSante(maximum=3)
    joueur = creer_joueur()
    affichage.dessiner(ecran, joueur)
    joueur.vies = 1
    affichage.dessiner(ecran, joueur)
    affichage.dessiner(ecran, creer_joueur())   # "Rejouer" = nouveau Joueur
    assert affichage.animations == {}
