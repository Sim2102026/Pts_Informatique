"""Tests de la classe Arrivee."""
import pygame

from arrivee import Arrivee


def test_arrivee_a_la_bonne_position():
    a = Arrivee(100, 200, pygame.Surface((64, 64)))
    assert a.rect.topleft == (100, 200)


def test_arrivee_charge_le_drapeau_de_l_asset():
    a = Arrivee(0, 0)
    assert a.image.get_size() == (64, 64)
