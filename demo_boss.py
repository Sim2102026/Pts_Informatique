"""Essai rapide : python demo_boss.py (sans refaire la grande carte)."""
from jeu import Jeu

if __name__ == "__main__":
    jeu = Jeu()
    jeu.entrer_salle_boss()
    jeu.etat = "jeu"
    jeu.lancer()
