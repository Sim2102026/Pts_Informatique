"""Tests de la classe fille Piece."""
import config
from entite import Entite
from piece import Piece, charger_animation_fruit
from aides import fausses_animations


def creer_piece():
    return Piece(100, 100, fausses_animations(noms=("idle",)))


def test_piece_est_une_entite():
    assert isinstance(creer_piece(), Entite)


def test_la_piece_ne_tombe_pas():
    # update() est redéfinie : pas de gravité
    p = creer_piece()
    for _ in range(60):
        p.update()
    assert p.rect.topleft == (100, 100)


def test_la_piece_est_animee():
    p = creer_piece()
    p.update()
    assert p.index_image == 1


def test_la_piece_a_une_valeur():
    assert creer_piece().valeur == config.POINTS_FRUIT


def test_charger_le_vrai_fruit():
    animations = charger_animation_fruit("Apple")
    assert len(animations["idle"]) == 17      # 544 / 32
