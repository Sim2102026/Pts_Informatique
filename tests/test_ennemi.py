"""Tests de la classe fille Ennemi."""
import pygame

import config
from entite import Entite
from ennemi import Ennemi
from plateforme import Plateforme
from aides import fausses_animations, sol


def creer_ennemi(x=100, y=0):
    return Ennemi(x, y, fausses_animations())


def test_ennemi_est_une_entite():
    assert isinstance(creer_ennemi(), Entite)


def test_l_ennemi_avance_tout_seul():
    e = creer_ennemi(x=100, y=436)        # posé sur le sol (436 + 64 = 500)
    e.update(sol(y=500))
    assert e.rect.x > 100


def test_toucher_un_mur_fait_demi_tour():
    e = creer_ennemi()
    e.toucher_mur()
    assert e.vitesse_x == -config.VITESSE_ENNEMI


def test_l_ennemi_fait_demi_tour_contre_un_bloc():
    e = creer_ennemi(x=0, y=0)
    mur = pygame.sprite.Group(Plateforme(65, 0, pygame.Surface((48, 48))))
    e.deplacer(mur)                       # avance de 2 : son bord droit passe de 64 à 66, il rentre dans le mur (x=65)
    assert e.vitesse_x < 0


def test_l_ennemi_ne_tombe_pas_dans_le_vide():
    # Une petite plateforme de 0 à 100 : l'ennemi doit rester dessus.
    plateformes = pygame.sprite.Group(Plateforme(0, 500, pygame.Surface((100, 48))))
    e = creer_ennemi(x=10, y=436)
    for _ in range(300):
        e.update(plateformes)
    assert e.rect.bottom == 500           # toujours sur la plateforme
    assert e.au_sol is True


def test_l_ennemi_ne_sort_pas_de_l_ecran():
    e = creer_ennemi(x=config.LARGEUR - 64, y=436)
    for _ in range(10):
        e.update(sol(y=500, largeur=config.LARGEUR + 200))
    assert e.vitesse_x < 0


def test_l_ennemi_joue_l_animation_run():
    assert creer_ennemi().choisir_animation() == "run"
