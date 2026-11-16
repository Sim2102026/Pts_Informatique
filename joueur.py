"""La classe FILLE Joueur : une Entite contrôlée au clavier."""
import pygame

import config
from entite import Entite
from outils import charger_image, decouper_planche, agrandir


def charger_animations_personnage(nom):
    """Charge les animations d'un personnage de l'asset (ex: "Ninja Frog").

    Renvoie un dictionnaire {"idle": [...], "run": [...], "jump": [...], ...}
    """
    fichiers = {
        "idle": "Idle (32x32).png",
        "run": "Run (32x32).png",
        "jump": "Jump (32x32).png",
        "fall": "Fall (32x32).png",
        "hit": "Hit (32x32).png",
    }
    animations = {}
    for nom_animation, fichier in fichiers.items():
        planche = charger_image("Main Characters", nom, fichier)
        images = decouper_planche(planche, config.TAILLE_PERSO, config.TAILLE_PERSO)
        animations[nom_animation] = [agrandir(img, config.ECHELLE) for img in images]
    return animations


class Joueur(Entite):   # <-- (Entite) entre parenthèses = "Joueur hérite d'Entite"

    def __init__(self, x, y, animations=None):
        if animations is None:
            animations = charger_animations_personnage("Ninja Frog")
        # On laisse la classe mère faire tout le travail commun :
        super().__init__(x, y, animations)
        self.largeur_monde = config.LARGEUR
        self.vies = config.VIES_DEPART
        self.score = 0
        self.invincible = 0     # compte à rebours (en frames) après un coup

    def lire_clavier(self, touches):
        """Règle la vitesse horizontale selon les flèches enfoncées.

        touches = résultat de pygame.key.get_pressed()
        (on peut l'interroger comme ça : touches[pygame.K_RIGHT] -> True/False)
        """
        self.vitesse_x = 0
        if touches[pygame.K_RIGHT]:
            self.vitesse_x = config.VITESSE_JOUEUR
        if touches[pygame.K_LEFT]:
            self.vitesse_x = -config.VITESSE_JOUEUR

    def sauter(self):
        """On ne peut sauter que si on a les pieds sur le sol."""
        if self.au_sol:
            self.vitesse_y = -config.FORCE_SAUT   # négatif = vers le haut
            self.au_sol = False

    def ramasser(self, piece):
        self.score += piece.valeur

    def ecraser(self, ennemi):
        """Le joueur saute sur un ennemi : l'ennemi disparaît et on rebondit."""
        ennemi.kill()           # kill() retire le sprite de tous ses groupes
        self.score += config.POINTS_ENNEMI
        self.vitesse_y = -config.REBOND

    def prendre_un_coup(self):
        """Perd une vie, sauf si on est encore invincible."""
        if self.invincible > 0:
            return
        self.vies -= 1
        self.invincible = config.DUREE_INVINCIBLE
        self.vitesse_y = -config.REBOND / 2     # petit sursaut

    def reapparaitre(self, x, y):
        """Après une chute dans un trou : on perd une vie et on revient au départ."""
        self.vies -= 1
        self.rect.topleft = (x, y)
        self.vitesse_x = 0
        self.vitesse_y = 0

    def soigner(self):
        if self.vies <= 0 or self.vies >= config.VIES_DEPART:
            return False
        self.vies += 1
        return True

    def est_mort(self):
        return self.vies <= 0

    def choisir_animation(self):
        """REDÉFINITION de la méthode de la classe mère :
        le joueur a plus d'animations qu'une entité de base."""
        # Juste après un coup (les 21 premières frames = 7 images x 3)
        if self.invincible > config.DUREE_INVINCIBLE - 21:
            return "hit"
        if self.vitesse_y < 0:
            return "jump"
        if self.vitesse_y > 1:
            return "fall"
        if self.vitesse_x != 0:
            return "run"
        return "idle"

    def update(self, plateformes):
        # On garde la recette de la mère (gravité, déplacement, animation)...
        super().update(plateformes)
        if self.invincible > 0:
            self.invincible -= 1
        # ...et on ajoute une règle propre au joueur : ne pas sortir de la carte.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.largeur_monde:
            self.rect.right = self.largeur_monde
