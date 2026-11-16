"""Tests du défilement et de la séparation monde/écran (pytest)."""
import pygame
import config
from camera import Camera
from niveau import Niveau
from jeu import Jeu


def test_camera_seuil_centre_et_bords():
    cible = type("Cible", (), {"rect": pygame.Rect(0, 0, 64, 64)})()
    camera = Camera(960, 7680)
    cible.rect.centerx = 480
    camera.update(cible)
    assert camera.offset_x == 0
    cible.rect.centerx = 1200
    camera.update(cible)
    assert camera.offset_x == 720
    assert camera.appliquer(cible.rect).centerx == 480
    cible.rect.centerx = 7680
    camera.update(cible)
    assert camera.offset_x == 6720
    cible.rect.centerx = 200
    camera.update(cible)
    assert camera.offset_x == 0


def test_camera_ne_modifie_pas_les_collisions():
    camera = Camera(960, 7680)
    camera.offset_x = 1500
    rect = pygame.Rect(1800, 300, 50, 50)
    avant = rect.copy()
    assert camera.appliquer(rect).x == 300
    assert rect == avant


def test_carte_plus_courte_que_ecran():
    camera = Camera(960, 400)
    cible = type("Cible", (), {"rect": pygame.Rect(350, 0, 50, 50)})()
    camera.update(cible)
    assert camera.offset_x == 0


def test_joueur_et_ennemis_peuvent_depasser_le_premier_ecran():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    jeu.joueur.rect.x = 2000
    jeu.joueur.update(jeu.niveau.plateformes)
    assert jeu.joueur.rect.x == 2000
    ennemi = next(iter(jeu.niveau.ennemis))
    ennemi.rect.x = 2000
    ennemi.vitesse_x = 2
    ennemi.update(pygame.sprite.Group())
    assert ennemi.vitesse_x == 2


def test_largeur_arrivee_et_reset_camera():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    assert jeu.niveau.largeur == 7680
    assert len(jeu.niveau.arrivee) == 1
    jeu.joueur.rect.x = 4000
    jeu.camera.update(jeu.joueur)
    assert jeu.camera.offset_x > 0
    jeu.executer_action("Rejouer")
    assert jeu.camera.offset_x == 0


def test_chute_revient_au_depart_avec_camera():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    jeu.joueur.rect.topleft = (4000, config.HAUTEUR + 50)
    jeu.camera.update(jeu.joueur)
    jeu.mettre_a_jour()
    assert jeu.joueur.vies == 2
    assert jeu.joueur.rect.topleft == jeu.niveau.position_depart
    assert jeu.camera.offset_x == 0


def test_victoire_hors_du_premier_ecran():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    fin = next(iter(jeu.niveau.arrivee))
    jeu.joueur.rect.center = fin.rect.center
    jeu.mettre_a_jour()
    assert jeu.etat == "fin" and jeu.menu.gagne


def test_dessin_apres_defilement_garde_les_rects():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    jeu.joueur.rect.x = 3500
    jeu.camera.update(jeu.joueur)
    rects = [s.rect.copy() for s in jeu.niveau.plateformes]
    jeu.dessiner()
    assert rects == [s.rect for s in jeu.niveau.plateformes]


def test_soin_hors_premier_ecran_et_plein_de_vies():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    soin = next(iter(jeu.niveau.soins))
    assert soin.rect.x > config.LARGEUR
    jeu.joueur.rect.center = soin.rect.center
    jeu.camera.update(jeu.joueur)
    jeu.verifier_collisions()
    assert soin.alive() and jeu.joueur.vies == 3
    jeu.joueur.vies = 2
    jeu.verifier_collisions()
    assert jeu.joueur.vies == 3 and not soin.alive()
    jeu.verifier_collisions()
    assert jeu.joueur.vies == 3


def test_soin_ne_ressuscite_pas_et_reapparait_au_rejeu():
    jeu = Jeu()
    jeu.executer_action("Jouer")
    assert len(jeu.niveau.soins) == 5
    soin = next(iter(jeu.niveau.soins))
    jeu.joueur.vies = 0
    assert not soin.ramasser(jeu.joueur) and soin.alive()
    jeu.joueur.vies = 1
    assert soin.ramasser(jeu.joueur) and jeu.joueur.vies == 2
    jeu.executer_action("Rejouer")
    assert len(jeu.niveau.soins) == 5 and jeu.joueur.vies == 3


def test_soin_flottant_et_collision_reste_dans_le_monde():
    jeu = Jeu()
    soin = next(iter(jeu.niveau.soins))
    avant = soin.rect.copy()
    soin.update(0.4)
    assert soin.rect.centery != avant.centery
    assert soin.rect.centerx == avant.centerx
    jeu.camera.offset_x = 1000
    jeu.niveau.dessiner(jeu.ecran, jeu.camera)
    assert soin.rect.centerx == avant.centerx


def test_parcours_complet_sans_ennemis_avec_physique_reelle():
    # Vérifie les distances de saut ; les ennemis sont couverts séparément.
    jeu = Jeu()
    joueur = jeu.joueur
    for _ in range(2200):
        if joueur.au_sol:
            obstacle = pygame.Rect(joueur.rect.right + 1, joueur.rect.top,
                                   20, joueur.rect.height - 2)
            sol_devant = pygame.Rect(joueur.rect.right + 20, joueur.rect.bottom, 1, 4)
            mur = any(obstacle.colliderect(b.rect) for b in jeu.niveau.plateformes)
            trou = not any(sol_devant.colliderect(b.rect) for b in jeu.niveau.plateformes)
            if mur or trou:
                joueur.sauter()
        joueur.vitesse_x = config.VITESSE_JOUEUR
        joueur.update(jeu.niveau.plateformes)
        assert joueur.rect.top <= config.HAUTEUR
        if joueur.rect.x > 7500:
            return
    raise AssertionError("Le parcours automatique n'a pas atteint l'arrivee")
