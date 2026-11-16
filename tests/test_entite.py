"""Tests de la classe mère Entite."""
import pygame

import config
from entite import Entite
from plateforme import Plateforme
from aides import fausses_animations, sol


def test_position_de_depart():
    e = Entite(100, 50, fausses_animations())
    assert e.rect.topleft == (100, 50)


def test_la_gravite_fait_accelerer_vers_le_bas():
    e = Entite(0, 0, fausses_animations())
    e.appliquer_gravite()
    e.appliquer_gravite()
    assert e.vitesse_y == 2 * config.GRAVITE


def test_la_vitesse_de_chute_est_limitee():
    e = Entite(0, 0, fausses_animations())
    for _ in range(1000):
        e.appliquer_gravite()
    assert e.vitesse_y == config.VITESSE_CHUTE_MAX


def test_l_entite_atterrit_sur_le_sol():
    e = Entite(0, 400, fausses_animations())
    plateformes = sol(y=500)
    for _ in range(100):           # on laisse tomber pendant 100 frames
        e.update(plateformes)
    assert e.rect.bottom == 500    # les pieds pile sur le sol
    assert e.au_sol is True


def test_l_entite_ne_traverse_pas_un_mur():
    e = Entite(0, 0, fausses_animations())      # rect de 0 à 64 en x
    murs = pygame.sprite.Group(Plateforme(70, 0, pygame.Surface((48, 48))))
    e.vitesse_x = 10
    e.deplacer(murs)
    assert e.rect.right == 70      # bloquée contre le mur


def test_l_entite_se_retourne_quand_elle_va_a_gauche():
    e = Entite(200, 0, fausses_animations())
    e.vitesse_x = -3
    e.update(sol())
    assert e.regarde_a_droite is False


def test_l_animation_tourne_en_boucle():
    e = Entite(0, 0, fausses_animations(nb_images=4))
    for _ in range(4 * 3):         # 4 images x 3 frames chacune
        e.animer()
    assert e.index_image == 0      # on est revenu au début
