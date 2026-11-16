"""Affiche les vies de Joueur sans modifier la logique du jeu."""
from pathlib import Path
import math
import pygame


class AffichageSante:
    def __init__(self, maximum=3, taille=64):
        # Images Kenney, à côté de ce fichier dans Assets/HUD.
        dossier = Path(__file__).resolve().parent / "Assets" / "HUD"
        self.coeur = pygame.transform.smoothscale(
            pygame.image.load(str(dossier / "hud_heart.png")), (taille, taille))
        self.coeur_vide = pygame.transform.smoothscale(
            pygame.image.load(str(dossier / "hud_heart_empty.png")), (taille, taille))
        self.maximum = maximum
        self.taille = taille
        self.duree_animation = 600  # millisecondes
        self.joueur_precedent = None
        self.vies_precedentes = maximum
        self.animations = {}  # indice du coeur : début de son animation

    def dessiner(self, ecran, joueur, x=None, y=0):
        """À appeler chaque frame, après le décor et avant display.flip()."""
        vies = max(0, min(self.maximum, joueur.vies))
        maintenant = pygame.time.get_ticks()

        # Rejouer crée un nouveau Joueur : on oublie les anciennes animations.
        if joueur is not self.joueur_precedent:
            self.joueur_precedent = joueur
            self.vies_precedentes = vies
            self.animations.clear()

        if vies < self.vies_precedentes:
            for i in range(vies, self.vies_precedentes):
                self.animations[i] = maintenant
        elif vies > self.vies_precedentes:
            # Un coeur récupéré doit redevenir rouge immédiatement.
            self.animations = {i: t for i, t in self.animations.items() if i >= vies}
        self.vies_precedentes = vies

        self.animations = {i: t for i, t in self.animations.items()
                           if maintenant - t < self.duree_animation}
        pas = round(self.taille * 0.8)
        if x is None:
            x = ecran.get_width() - ((self.maximum - 1) * pas + self.taille) - 15

        for i in range(self.maximum):
            image = self.coeur if i < vies else self.coeur_vide
            decalage = 0
            if i in self.animations:
                temps = maintenant - self.animations[i]
                image = self.coeur if (temps // 75) % 2 == 0 else self.coeur_vide
                # Secousse de plus en plus faible.
                decalage = round(5 * math.sin(temps * 0.08) *
                                 (1 - temps / self.duree_animation))
            ecran.blit(image, (x + i * pas + decalage, y))
