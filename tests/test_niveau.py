"""Tests de la classe Niveau."""
import config
from niveau import Niveau, CARTE

# Une toute petite carte pour les tests : facile à compter à la main
PETITE_CARTE = [
    "P..F.D",
    "..E...",
    "XXXXXX",
]


def test_compte_les_blocs():
    assert len(Niveau(PETITE_CARTE).plateformes) == 6


def test_compte_les_ennemis_fruits_et_arrivee():
    n = Niveau(PETITE_CARTE)
    assert len(n.ennemis) == 1
    assert len(n.pieces) == 1
    assert len(n.arrivee) == 1


def test_le_niveau_est_colle_en_bas_de_l_ecran():
    n = Niveau(PETITE_CARTE)
    plus_bas = max(bloc.rect.bottom for bloc in n.plateformes)
    assert plus_bas == config.HAUTEUR


def test_position_des_blocs():
    n = Niveau(PETITE_CARTE)
    t = config.TAILLE_TUILE
    xs = sorted(bloc.rect.x for bloc in n.plateformes)
    assert xs == [0, t, 2 * t, 3 * t, 4 * t, 5 * t]


def test_l_ennemi_est_pose_sur_le_sol():
    n = Niveau(PETITE_CARTE)
    ennemi = next(iter(n.ennemis))
    sol = min(bloc.rect.top for bloc in n.plateformes)
    assert ennemi.rect.bottom == sol


def test_position_de_depart_du_joueur():
    n = Niveau(PETITE_CARTE)
    t = config.TAILLE_TUILE
    decalage = config.HAUTEUR - 3 * t
    assert n.position_depart == (0, decalage + t - 64)


def test_la_vraie_carte_est_rectangulaire():
    # Toutes les lignes ont la largeur du monde, independante de la fenetre.
    for ligne in CARTE:
        assert len(ligne) == len(CARTE[0])
    assert len(CARTE[0]) * config.TAILLE_TUILE > config.LARGEUR


def test_la_vraie_carte_a_un_depart_et_une_arrivee():
    texte = "".join(CARTE)
    assert texte.count("P") == 1
    assert texte.count("D") == 1
