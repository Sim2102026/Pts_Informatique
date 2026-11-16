"""La classe MÈRE Entite.

Tout ce qui bouge dans le jeu et qui est soumis à la gravité (le joueur,
les ennemis) a les mêmes besoins : une position, une vitesse, des
animations, des collisions avec les plateformes.
Au lieu de recopier ce code dans chaque classe, on l'écrit UNE fois ici,
et les classes filles en héritent.
"""
import pygame

import config


class Entite(pygame.sprite.Sprite):
    # Entite hérite elle-même de pygame.sprite.Sprite : ça lui donne
    # gratuitement self.image, self.rect et la possibilité d'être rangée
    # dans un "groupe" de sprites.

    def __init__(self, x, y, animations):
        super().__init__()   # appelle le __init__ de Sprite (le parent)

        # animations = dictionnaire  {"idle": [img1, img2...], "run": [...]}
        self.animations = animations
        self.animation_courante = "idle"
        self.index_image = 0          # quelle image de l'animation on montre
        self.regarde_a_droite = True  # pour retourner l'image vers la gauche

        self.image = self.animations["idle"][0]
        # rect = le rectangle qui sert à la position ET aux collisions
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vitesse_x = 0
        self.vitesse_y = 0
        self.au_sol = False

    # ------------------------------------------------------------------
    # Physique
    # ------------------------------------------------------------------
    def appliquer_gravite(self):
        """La gravité augmente la vitesse vers le bas, frame après frame."""
        self.vitesse_y += config.GRAVITE
        if self.vitesse_y > config.VITESSE_CHUTE_MAX:
            self.vitesse_y = config.VITESSE_CHUTE_MAX

    def deplacer(self, plateformes):
        """Déplace l'entité et l'empêche de traverser les plateformes.

        On bouge en DEUX temps (d'abord x, puis y) : comme ça, quand on
        touche un bloc, on sait si on l'a touché par le côté ou par le dessus.
        """
        # 1) Horizontal
        self.rect.x += self.vitesse_x
        for bloc in pygame.sprite.spritecollide(self, plateformes, False):
            if self.vitesse_x > 0:          # on allait à droite
                self.rect.right = bloc.rect.left
            elif self.vitesse_x < 0:        # on allait à gauche
                self.rect.left = bloc.rect.right
            self.toucher_mur()

        # 2) Vertical
        # round() : un rect ne contient que des nombres ENTIERS. Sans round,
        # "y += 0.8" ne bougerait pas du tout (0.8 serait coupé à 0), on ne
        # toucherait jamais le sol et au_sol resterait False.
        self.rect.y += round(self.vitesse_y)
        self.au_sol = False
        for bloc in pygame.sprite.spritecollide(self, plateformes, False):
            if self.vitesse_y > 0:          # on tombait : on atterrit
                self.rect.bottom = bloc.rect.top
                self.au_sol = True
            elif self.vitesse_y < 0:        # on montait : on se cogne la tête
                self.rect.top = bloc.rect.bottom
            self.vitesse_y = 0

    def toucher_mur(self):
        """Appelée quand on cogne un mur. Ne fait rien par défaut :
        une classe fille peut la REDÉFINIR (l'ennemi fera demi-tour)."""
        pass

    # ------------------------------------------------------------------
    # Animation
    # ------------------------------------------------------------------
    def choisir_animation(self):
        """Renvoie le nom de l'animation à jouer. Les filles la redéfinissent."""
        return "idle"

    def animer(self):
        """Passe à l'image suivante de l'animation."""
        nouvelle = self.choisir_animation()
        if nouvelle != self.animation_courante:   # on change d'animation :
            self.animation_courante = nouvelle    # on repart de la 1re image
            self.index_image = 0

        images = self.animations[self.animation_courante]
        self.index_image = (self.index_image + 1) % (len(images) * 3)
        image = images[self.index_image // 3]     # 1 image toutes les 3 frames

        if not self.regarde_a_droite:
            # flip(image, horizontal, vertical) = effet miroir
            image = pygame.transform.flip(image, True, False)
        self.image = image

    # ------------------------------------------------------------------
    def update(self, plateformes):
        """Appelée à chaque frame : la "recette" commune à toutes les entités."""
        self.appliquer_gravite()
        self.deplacer(plateformes)
        if self.vitesse_x > 0:
            self.regarde_a_droite = True
        elif self.vitesse_x < 0:
            self.regarde_a_droite = False
        self.animer()
