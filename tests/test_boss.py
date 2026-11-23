"""Entrée réelle, combat, checkpoint et séparation des scènes."""
import pygame
import pytest
import config
import db
from jeu import Jeu
from salle_boss import SalleBoss


@pytest.fixture
def jeu(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    j = Jeu()
    j.etat = "jeu"
    yield j
    pygame.quit()


def tomber_sur_tete(jeu):
    boss = jeu.niveau.boss
    avant = jeu.joueur.rect.copy()
    avant.midbottom = (boss.rect.centerx, boss.rect.top - 2)
    jeu.joueur.rect.midbottom = (boss.rect.centerx, boss.rect.top + 5)
    jeu.joueur.vitesse_y = 7
    return boss.toucher_joueur(jeu.joueur, avant)


def test_porte_exige_proximite_sol_et_touche_haut(jeu):
    assert not jeu.commencer_entree()
    porte = next(iter(jeu.niveau.portes))
    jeu.joueur.rect.midbottom = porte.rect.midbottom
    jeu.joueur.au_sol = False
    assert not jeu.commencer_entree()
    jeu.joueur.au_sol = True
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    jeu.gerer_evenements()
    assert jeu.transition == 0
    assert jeu.joueur.vitesse_y == 0
    assert porte.image is porte.images["open"]
    for _ in range(50):
        jeu.mettre_a_jour()
    assert isinstance(jeu.niveau, SalleBoss)
    assert jeu.transition is None
    assert jeu.camera.offset_x == 0


def test_entree_conserve_score_et_vies_et_attend_le_joueur(jeu):
    jeu.joueur.score, jeu.joueur.vies = 120, 2
    jeu.entrer_salle_boss()
    assert (jeu.joueur.score, jeu.joueur.vies) == (120, 2)
    for _ in range(100):
        jeu.mettre_a_jour()
    assert jeu.niveau.boss.etat == "attente"
    jeu.joueur.rect.centerx = 330
    jeu.mettre_a_jour()
    assert jeu.niveau.declenche
    assert jeu.niveau.boss.etat == "patrouille"
    assert not jeu.niveau.arrivee


def test_cycle_attaque_borne_et_direction_verrouillee(jeu):
    jeu.entrer_salle_boss()
    boss = jeu.niveau.boss
    boss.activer()
    boss.update(0.91, jeu.joueur)
    assert boss.etat == "charge" and boss.direction == -1
    jeu.joueur.rect.x = 850
    boss.update(0.66, jeu.joueur)
    assert boss.etat == "attaque" and boss.direction == -1
    boss.update(0.71, jeu.joueur)
    assert boss.vulnerable
    assert 48 <= boss.rect.left and boss.rect.right <= 912


def test_corps_blesse_mais_invincibilite_evite_degats_en_chaine(jeu):
    jeu.entrer_salle_boss()
    boss = jeu.niveau.boss
    boss.activer()
    jeu.joueur.invincible = 0
    jeu.joueur.rect.center = boss.rect.center
    jeu.joueur.vitesse_y = 0
    for _ in range(10):
        boss.toucher_joueur(jeu.joueur, jeu.joueur.rect.copy())
    assert jeu.joueur.vies == 2
    assert boss.vies == 3


def test_coup_valide_rebond_et_un_seul_point_de_vie(jeu):
    jeu.entrer_salle_boss()
    boss = jeu.niveau.boss
    boss.changer_etat("fatigue")
    assert tomber_sur_tete(jeu)
    assert boss.vies == 2 and boss.etat == "blesse"
    assert jeu.joueur.vitesse_y < 0
    assert not tomber_sur_tete(jeu)
    assert boss.vies == 2


def test_pas_de_coup_en_remontant_ou_pendant_charge(jeu):
    jeu.entrer_salle_boss()
    boss = jeu.niveau.boss
    boss.changer_etat("charge")
    assert not tomber_sur_tete(jeu)
    boss.changer_etat("fatigue")
    jeu.joueur.vitesse_y = -4
    assert not boss.toucher_joueur(jeu.joueur, jeu.joueur.rect.copy())
    assert boss.vies == 3


def test_un_vrai_saut_permet_de_toucher_la_tete(monkeypatch, jeu):
    jeu.entrer_salle_boss()
    boss = jeu.niveau.boss
    jeu.niveau.declenche = True
    boss.changer_etat("fatigue")
    jeu.joueur.rect.midbottom = (boss.rect.centerx - 130, jeu.niveau.sol_y)
    jeu.joueur.au_sol = True
    jeu.joueur.invincible = 0
    jeu.joueur.sauter()
    for frame in range(60):
        touches = {pygame.K_LEFT: False, pygame.K_RIGHT: frame < 20}
        monkeypatch.setattr(pygame.key, "get_pressed", lambda: touches)
        jeu.mettre_a_jour()
        if boss.vies == 2:
            assert jeu.joueur.vies == 3
            assert jeu.joueur.vitesse_y < 0
            return
    pytest.fail("Le saut réel n'a pas atteint la tête du boss")


def test_trois_coups_trophee_et_victoire(jeu):
    jeu.entrer_salle_boss()
    salle = jeu.niveau
    salle.declenche = True
    for _ in range(3):
        salle.boss.changer_etat("fatigue")
        assert tomber_sur_tete(jeu)
    assert salle.boss.vies == 0
    assert not salle.arrivee
    salle.mettre_a_jour_boss(0.71, jeu.joueur, jeu.joueur.rect.copy())
    assert len(salle.arrivee) == 1
    salle.reveler_trophee()
    assert len(salle.arrivee) == 1
    jeu.joueur.rect.center = next(iter(salle.arrivee)).rect.center
    jeu.mettre_a_jour()
    assert jeu.etat == "fin" and jeu.menu.gagne


def test_rejouer_apres_mort_recommence_dans_la_salle(jeu):
    jeu.joueur.score = 140
    jeu.entrer_salle_boss()
    jeu.joueur.vies = 0
    jeu.mettre_a_jour()
    assert jeu.etat == "fin" and not jeu.menu.gagne
    jeu.executer_action("Rejouer")
    assert jeu.scene == "salle_boss" and jeu.etat == "jeu"
    assert jeu.joueur.vies == 3 and jeu.joueur.score == 140
    assert jeu.niveau.boss.vies == 3
    assert not jeu.niveau.declenche


def test_sauvegarde_room_et_recharge_checkpoint(monkeypatch, jeu):
    jeu.joueur.score = 100
    jeu.entrer_salle_boss()
    jeu.joueur.rect.x = 800
    jeu.joueur.vies = 1
    jeu.sauvegarde_disponible = True
    jeu.slot_actif = 2
    captures = []
    monkeypatch.setattr(db, "sauvegarder", lambda slot, joueur, **kw:
                        captures.append((slot, joueur, kw)))
    assert jeu.sauvegarder_automatiquement()
    slot, joueur, kw = captures[0]
    assert kw["niveau"] == "salle_boss"
    assert joueur.rect.topleft == jeu.niveau.position_depart
    assert joueur.vies == 3
    monkeypatch.setattr(db, "charger_sauvegarde", lambda slot:
                        dict(niveau="salle_boss", score=100, x=800, y=500, vies=1))
    assert jeu.selectionner_sauvegarde(2)
    assert jeu.scene == "salle_boss" and jeu.joueur.vies == 3
    assert jeu.niveau.boss.vies == 3 and not jeu.niveau.declenche


def test_sauvegarde_boss_vaincu_ne_ressuscite_pas(monkeypatch, jeu):
    jeu.sauvegarde_disponible = True
    monkeypatch.setattr(db, "charger_sauvegarde", lambda slot:
                        dict(niveau="boss_vaincu", score=400, x=96, y=528, vies=3))
    assert jeu.selectionner_sauvegarde(1)
    assert jeu.niveau.boss.etat == "vaincu"
    assert len(jeu.niveau.arrivee) == 1
    assert jeu.joueur.score == 400


def test_dessiner_tous_les_etats_du_boss(jeu):
    jeu.entrer_salle_boss()
    jeu.niveau.declenche = True
    for etat in ("attente", "patrouille", "charge", "attaque", "fatigue", "blesse", "mort", "vaincu"):
        jeu.niveau.boss.changer_etat(etat)
        jeu.niveau.boss.animer()
        # attente n'est affichée que dans la zone sûre.
        jeu.niveau.declenche = etat != "attente"
        jeu.dessiner()
