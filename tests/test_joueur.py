"""Tests de la classe fille Joueur."""
import pygame

import config
from entite import Entite
from joueur import Joueur, charger_animations_personnage
from aides import fausses_animations, sol, FauxClavier


def creer_joueur(x=100, y=0):
    return Joueur(x, y, fausses_animations())


def test_joueur_est_une_entite():
    # C'est LE test de l'héritage : un Joueur EST une Entite.
    assert isinstance(creer_joueur(), Entite)


def test_fleche_droite_fait_aller_a_droite():
    j = creer_joueur()
    j.lire_clavier(FauxClavier({pygame.K_RIGHT: True}))
    assert j.vitesse_x == config.VITESSE_JOUEUR


def test_fleche_gauche_fait_aller_a_gauche():
    j = creer_joueur()
    j.lire_clavier(FauxClavier({pygame.K_LEFT: True}))
    assert j.vitesse_x == -config.VITESSE_JOUEUR


def test_aucune_touche_le_joueur_s_arrete():
    j = creer_joueur()
    j.vitesse_x = 5
    j.lire_clavier(FauxClavier())
    assert j.vitesse_x == 0


def test_sauter_depuis_le_sol():
    j = creer_joueur()
    j.au_sol = True
    j.sauter()
    assert j.vitesse_y == -config.FORCE_SAUT


def test_pas_de_saut_en_l_air():
    j = creer_joueur()
    j.au_sol = False
    j.sauter()
    assert j.vitesse_y == 0


def test_choix_des_animations():
    j = creer_joueur()
    j.vitesse_x, j.vitesse_y = 0, 0
    assert j.choisir_animation() == "idle"
    j.vitesse_x = 5
    assert j.choisir_animation() == "run"
    j.vitesse_y = -10
    assert j.choisir_animation() == "jump"
    j.vitesse_y = 10
    assert j.choisir_animation() == "fall"


def test_le_joueur_ne_sort_pas_de_l_ecran():
    j = creer_joueur(x=0, y=400)
    j.vitesse_x = -10
    j.update(sol())
    assert j.rect.left == 0


def test_charger_les_vraies_animations():
    animations = charger_animations_personnage("Ninja Frog")
    assert len(animations["run"]) == 12          # 384 / 32
    assert animations["idle"][0].get_size() == (64, 64)   # 32 x ECHELLE


# ---------- Étape 3 : vies, score, ennemis ----------
from piece import Piece
from ennemi import Ennemi


def test_le_joueur_commence_avec_3_vies_et_0_point():
    j = creer_joueur()
    assert j.vies == config.VIES_DEPART
    assert j.score == 0


def test_ramasser_un_fruit_donne_des_points():
    j = creer_joueur()
    j.ramasser(Piece(0, 0, fausses_animations(noms=("idle",))))
    assert j.score == config.POINTS_FRUIT


def test_prendre_un_coup_enleve_une_vie():
    j = creer_joueur()
    j.prendre_un_coup()
    assert j.vies == config.VIES_DEPART - 1


def test_invincible_juste_apres_un_coup():
    j = creer_joueur()
    j.prendre_un_coup()
    j.prendre_un_coup()             # tout de suite après : ne compte pas
    assert j.vies == config.VIES_DEPART - 1


def test_l_invincibilite_finit_par_s_arreter():
    j = creer_joueur(y=400)
    j.prendre_un_coup()
    for _ in range(config.DUREE_INVINCIBLE):
        j.update(sol())
    assert j.invincible == 0


def test_ecraser_un_ennemi():
    j = creer_joueur()
    ennemi = Ennemi(0, 0, fausses_animations())
    groupe = pygame.sprite.Group(ennemi)
    j.ecraser(ennemi)
    assert len(groupe) == 0                         # l'ennemi a disparu
    assert j.score == config.POINTS_ENNEMI
    assert j.vitesse_y < 0                          # le joueur rebondit


def test_mort_quand_plus_de_vies():
    j = creer_joueur()
    j.vies = 0
    assert j.est_mort() is True


# ---------- Étape 4 ----------
def test_reapparaitre_apres_une_chute():
    j = creer_joueur(x=500, y=900)
    j.vitesse_y = 15
    j.reapparaitre(48, 100)
    assert j.rect.topleft == (48, 100)
    assert j.vies == config.VIES_DEPART - 1
    assert j.vitesse_y == 0
