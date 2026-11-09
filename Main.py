"""Petit exemple pour tester Environnement avec un joueur provisoire."""

import pygame
from Environnement import DOSSIER_ASSETS, Environnement, LARGEUR, HAUTEUR


class JoueurDemo:
    """A remplacer par la classe Joueur de l'equipe lors de l'integration."""

    def __init__(self, environnement):
        self.images = {}
        for etat in ["idle", "jump", "walk_a", "walk_b"]:
            image = pygame.image.load(str(DOSSIER_ASSETS / ("character_green_" + etat + ".png"))).convert_alpha()
            # Enlever les marges transparentes pour que les pieds touchent le sol.
            image = image.subsurface(image.get_bounding_rect())
            self.images[etat] = pygame.transform.smoothscale(image, (52, 62))
        self.rect = self.images["idle"].get_rect()
        self.reinitialiser(environnement)

    def reinitialiser(self, environnement):
        self.rect.topleft = (64, 450)
        self.vitesse_y = 0
        self.au_sol = environnement.est_au_sol(self.rect)
        self.vers_la_gauche = False
        self.etat = "idle"
        self.compteur_marche = 0

    def mettre_a_jour(self, environnement, direction, saut):
        dx = direction * 5       # 5 pixels par image, a 60 images/seconde.
        if direction != 0:
            self.vers_la_gauche = direction < 0
        if saut and self.au_sol:
            self.vitesse_y = -15
        self.vitesse_y = min(self.vitesse_y + 0.7, 15)  # Gravite et vitesse maximale.
        ancien_x = self.rect.x
        self.au_sol, choc_vertical = environnement.deplacer(self.rect, dx, self.vitesse_y)
        if choc_vertical:
            self.vitesse_y = 0

        # Deux images alternees toutes les 8 mises a jour, seulement si on avance au sol.
        if not self.au_sol:
            self.etat = "jump"
            self.compteur_marche = 0
        elif self.rect.x != ancien_x:
            self.etat = "walk_a" if self.compteur_marche < 8 else "walk_b"
            self.compteur_marche = (self.compteur_marche + 1) % 16
        else:
            self.etat = "idle"
            self.compteur_marche = 0
        if self.rect.top >= HAUTEUR:
            self.reinitialiser(environnement)

    def dessiner(self, ecran):
        image = self.images[self.etat]
        if self.vers_la_gauche:
            image = pygame.transform.flip(image, True, False)
        ecran.blit(image, self.rect)


def main():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Pts Informatique - Environnement Kenney")
    environnement = Environnement()
    joueur = JoueurDemo(environnement)
    horloge = pygame.time.Clock()
    police = pygame.font.Font(None, 24)
    aide = police.render("A D / Gauche Droite : bouger   |   Espace / Haut : sauter   |   R : recommencer   |   Echap : quitter",
                         True, (32, 53, 77))
    actif = True

    while actif:
        saut = False
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                actif = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    actif = False
                elif evenement.key == pygame.K_r:
                    joueur.reinitialiser(environnement)
                elif evenement.key in [pygame.K_SPACE, pygame.K_UP]:
                    saut = True
        if not actif:
            break

        touches = pygame.key.get_pressed()
        gauche = touches[pygame.K_LEFT] or touches[pygame.K_a]
        droite = touches[pygame.K_RIGHT] or touches[pygame.K_d]
        direction = int(droite) - int(gauche)
        joueur.mettre_a_jour(environnement, direction, saut)
        environnement.dessiner(ecran)
        joueur.dessiner(ecran)
        ecran.blit(aide, (22, 20))
        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
