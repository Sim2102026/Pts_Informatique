"""Tests des fonctions de outils.py."""
import pygame

from outils import decouper_planche, agrandir, charger_image


def test_decouper_planche_donne_le_bon_nombre_d_images():
    # On fabrique une fausse planche de 4 images de 32x32 (donc 128x32).
    planche = pygame.Surface((128, 32))
    images = decouper_planche(planche, 32, 32)
    assert len(images) == 4


def test_chaque_image_decoupee_a_la_bonne_taille():
    planche = pygame.Surface((96, 32))
    for image in decouper_planche(planche, 32, 32):
        assert image.get_size() == (32, 32)


def test_agrandir_multiplie_la_taille():
    image = pygame.Surface((32, 32))
    assert agrandir(image, 2).get_size() == (64, 64)


def test_charger_image_de_l_asset():
    # Vérifie que le dossier assets est bien en place.
    image = charger_image("Main Characters", "Ninja Frog", "Run (32x32).png")
    assert image.get_size() == (384, 32)   # 12 images de 32x32
