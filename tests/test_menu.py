"""Tests des classes Menu, MenuAccueil et MenuFin."""
import pygame

from menu import Menu, MenuAccueil, MenuFin


def test_la_premiere_option_est_selectionnee_au_depart():
    assert Menu("Titre", ["A", "B"]).selection == 0


def test_fleche_bas_passe_a_l_option_suivante():
    m = Menu("Titre", ["A", "B", "C"])
    m.gerer_touche(pygame.K_DOWN)
    assert m.selection == 1


def test_apres_la_derniere_option_on_revient_au_debut():
    m = Menu("Titre", ["A", "B"])
    m.gerer_touche(pygame.K_DOWN)
    m.gerer_touche(pygame.K_DOWN)
    assert m.selection == 0


def test_fleche_haut_depuis_le_debut_va_a_la_fin():
    m = Menu("Titre", ["A", "B", "C"])
    m.gerer_touche(pygame.K_UP)
    assert m.selection == 2


def test_entree_renvoie_l_option_choisie():
    m = Menu("Titre", ["A", "B"])
    m.gerer_touche(pygame.K_DOWN)
    assert m.gerer_touche(pygame.K_RETURN) == "B"


def test_une_autre_touche_ne_choisit_rien():
    assert Menu("Titre", ["A"]).gerer_touche(pygame.K_a) is None


def test_menu_accueil_est_un_menu():
    m = MenuAccueil()
    assert isinstance(m, Menu)
    assert m.options == ["Jouer", "Quitter"]
    assert len(m.lignes_infos()) > 0      # redéfinie : affiche les commandes


def test_menu_fin_victoire():
    m = MenuFin(gagne=True, score=120)
    assert isinstance(m, Menu)
    assert "gagné" in m.titre
    assert m.lignes_infos() == ["Score : 120"]


def test_menu_fin_defaite():
    assert MenuFin(gagne=False, score=0).titre == "Perdu..."


def test_dessiner_ne_plante_pas():
    pygame.init()
    ecran = pygame.Surface((960, 640))
    MenuFin(True, 50).dessiner(ecran)     # si ça plante, le test échoue
