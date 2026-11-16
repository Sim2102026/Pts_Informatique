"""Tests de la classe Jeu."""
import pygame
import pytest

import config
from jeu import Jeu
from joueur import Joueur
from niveau import Niveau
from menu import MenuAccueil, MenuFin


@pytest.fixture
def jeu():
    j = Jeu()
    yield j
    pygame.quit()


@pytest.fixture
def partie(jeu):
    """Un jeu où on a déjà appuyé sur "Jouer"."""
    jeu.executer_action("Jouer")
    return jeu


def appuyer(touche):
    """Simule l'appui sur une touche du clavier."""
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=touche))


# ---------- Fenêtre et événements ----------
def test_la_fenetre_a_la_bonne_taille(jeu):
    assert jeu.ecran.get_size() == (config.LARGEUR, config.HAUTEUR)


def test_cliquer_sur_la_croix_arrete_le_jeu(jeu):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    jeu.gerer_evenements()
    assert jeu.en_cours is False


def test_echap_arrete_le_jeu(jeu):
    appuyer(pygame.K_ESCAPE)
    jeu.gerer_evenements()
    assert jeu.en_cours is False


# ---------- Menus ----------
def test_le_jeu_commence_sur_le_menu_d_accueil(jeu):
    assert jeu.etat == "accueil"
    assert isinstance(jeu.menu, MenuAccueil)


def test_entree_sur_jouer_lance_la_partie(jeu):
    appuyer(pygame.K_RETURN)
    jeu.gerer_evenements()
    assert jeu.etat == "jeu"


def test_choisir_quitter_ferme_le_jeu(jeu):
    appuyer(pygame.K_DOWN)
    appuyer(pygame.K_RETURN)
    jeu.gerer_evenements()
    assert jeu.en_cours is False


def test_dans_le_menu_le_jeu_est_en_pause(jeu):
    avant = jeu.joueur.rect.topleft
    for _ in range(30):
        jeu.mettre_a_jour()
    assert jeu.joueur.rect.topleft == avant


def test_dessiner_ne_plante_pas_dans_chaque_etat(jeu):
    jeu.dessiner()                     # accueil
    jeu.executer_action("Jouer")
    jeu.dessiner()                     # jeu
    jeu.finir_partie(gagne=True)
    jeu.dessiner()                     # fin


# ---------- Partie ----------
def test_le_jeu_contient_un_niveau_et_un_joueur(partie):
    assert isinstance(partie.niveau, Niveau)
    assert isinstance(partie.joueur, Joueur)


def test_le_joueur_commence_a_la_case_depart(partie):
    assert partie.joueur.rect.topleft == partie.niveau.position_depart


def test_le_joueur_finit_par_tomber_sur_le_sol(partie):
    for _ in range(60):
        partie.mettre_a_jour()
    assert partie.joueur.au_sol is True


def test_espace_fait_sauter_le_joueur(partie):
    for _ in range(60):
        partie.mettre_a_jour()
    appuyer(pygame.K_SPACE)
    partie.gerer_evenements()
    assert partie.joueur.vitesse_y < 0


def test_toucher_un_fruit_le_ramasse(partie):
    piece = next(iter(partie.niveau.pieces))
    nb_avant = len(partie.niveau.pieces)
    partie.joueur.rect.center = piece.rect.center
    partie.verifier_collisions()
    assert len(partie.niveau.pieces) == nb_avant - 1
    assert partie.joueur.score == config.POINTS_FRUIT


def test_toucher_un_ennemi_de_cote_fait_perdre_une_vie(partie):
    ennemi = next(iter(partie.niveau.ennemis))
    partie.joueur.vitesse_y = 0
    partie.joueur.rect.center = ennemi.rect.center
    partie.verifier_collisions()
    assert partie.joueur.vies == config.VIES_DEPART - 1


def test_tomber_sur_un_ennemi_l_ecrase(partie):
    ennemi = next(iter(partie.niveau.ennemis))
    nb_avant = len(partie.niveau.ennemis)
    partie.joueur.vitesse_y = 5
    partie.joueur.rect.midbottom = (ennemi.rect.centerx, ennemi.rect.top + 10)
    partie.verifier_collisions()
    assert len(partie.niveau.ennemis) == nb_avant - 1


def test_tomber_dans_un_trou_fait_perdre_une_vie(partie):
    partie.joueur.rect.top = config.HAUTEUR + 10
    partie.mettre_a_jour()
    assert partie.joueur.vies == config.VIES_DEPART - 1
    assert partie.joueur.rect.topleft == partie.niveau.position_depart


# ---------- Fin de partie ----------
def test_toucher_le_trophee_fait_gagner(partie):
    trophee = next(iter(partie.niveau.arrivee))
    partie.joueur.rect.center = trophee.rect.center
    partie.mettre_a_jour()
    assert partie.etat == "fin"
    assert isinstance(partie.menu, MenuFin)
    assert partie.menu.gagne is True


def test_plus_de_vies_fait_perdre(partie):
    partie.joueur.vies = 0
    partie.mettre_a_jour()
    assert partie.etat == "fin"
    assert partie.menu.gagne is False


def test_rejouer_remet_tout_a_zero(partie):
    partie.joueur.score = 999
    partie.finir_partie(gagne=False)
    partie.executer_action("Rejouer")
    assert partie.etat == "jeu"
    assert partie.joueur.score == 0
    assert partie.joueur.vies == config.VIES_DEPART
