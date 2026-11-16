"""Tests de la classe Plateforme."""
import pygame

from plateforme import Plateforme


def test_plateforme_a_la_bonne_position():
    p = Plateforme(96, 48, pygame.Surface((48, 48)))
    assert p.rect.topleft == (96, 48)


def test_plateforme_a_la_taille_de_son_image():
    p = Plateforme(0, 0, pygame.Surface((48, 48)))
    assert p.rect.size == (48, 48)
