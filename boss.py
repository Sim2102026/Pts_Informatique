"""Roi Slime : une petite machine à états, sans modifier Ennemi."""
import pygame
from porte import charger_asset


class Boss(pygame.sprite.Sprite):
    VIES_MAX = 3
    POINTS = 300
    DUREES = {"patrouille": 0.9, "charge": 0.65, "attaque": 0.7,
              "fatigue": 2.2, "blesse": 0.65, "mort": 0.7}

    def __init__(self, centre_x, sol_y, limite_gauche=48, limite_droite=912):
        super().__init__()
        self.images = {}
        for etat in ("rest", "walk_a", "walk_b", "flat"):
            image = charger_asset(f"slime_normal_{etat}.png")
            image = image.subsurface(image.get_bounding_rect())
            self.images[etat] = pygame.transform.smoothscale(image, (128, 76))
        self.image = self.images["rest"]
        self.rect = self.image.get_rect(midbottom=(centre_x, sol_y))
        self.limite_gauche = limite_gauche
        self.limite_droite = limite_droite
        self.x = float(self.rect.x)
        self.vies = self.VIES_MAX
        self.etat = "attente"
        self.temps = 0.0
        self.temps_total = 0.0
        self.direction = -1

    @property
    def vulnerable(self):
        return self.etat == "fatigue" and self.vies > 0

    def changer_etat(self, etat):
        self.etat = etat
        self.temps = 0.0

    def activer(self):
        if self.etat == "attente":
            self.changer_etat("patrouille")

    def update(self, dt, joueur):
        self.temps += dt
        self.temps_total += dt
        if self.etat in ("patrouille", "attaque"):
            vitesse = 95 if self.etat == "patrouille" else 560
            self.x += self.direction * vitesse * dt
            self.x = max(self.limite_gauche,
                         min(self.x, self.limite_droite - self.rect.width))
            self.rect.x = round(self.x)
            if self.rect.left <= self.limite_gauche or self.rect.right >= self.limite_droite:
                if self.etat == "attaque":
                    self.changer_etat("fatigue")
                else:
                    self.direction *= -1

        if self.etat in self.DUREES and self.temps >= self.DUREES[self.etat]:
            suivant = {"patrouille": "charge", "charge": "attaque",
                       "attaque": "fatigue", "fatigue": "patrouille",
                       "blesse": "patrouille", "mort": "vaincu"}[self.etat]
            if suivant == "charge":
                # La direction est annoncée pendant la charge, puis verrouillée.
                self.direction = 1 if joueur.rect.centerx > self.rect.centerx else -1
            self.changer_etat(suivant)
        self.animer()

    def animer(self):
        image = self.images["rest"]
        if self.etat in ("patrouille", "attaque"):
            image = self.images["walk_a" if int(self.temps_total * 8) % 2 == 0 else "walk_b"]
        elif self.etat in ("charge", "mort", "vaincu"):
            image = pygame.transform.smoothscale(self.images["flat"], (128, 38))
        image = image.copy()
        if self.etat == "charge":
            image.fill((255, 120, 80, 255), special_flags=pygame.BLEND_RGBA_MULT)
        elif self.vulnerable:
            image.fill((150, 255, 160, 255), special_flags=pygame.BLEND_RGBA_MULT)
        if self.direction > 0:
            image = pygame.transform.flip(image, True, False)
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        if self.etat != "blesse" or int(self.temps * 14) % 2 == 0:
            surface.blit(image, image.get_rect(midbottom=(self.rect.width // 2, self.rect.height)))
        self.image = surface

    def prendre_un_coup(self):
        if not self.vulnerable:
            return False
        self.vies -= 1
        self.changer_etat("mort" if self.vies == 0 else "blesse")
        return True

    def toucher_joueur(self, joueur, ancien_rect):
        """Le dessus n'est une faiblesse que pendant la fatigue."""
        if self.etat in ("attente", "blesse", "mort", "vaincu"):
            return False
        if not joueur.rect.colliderect(self.rect):
            return False
        tombe_sur_tete = (joueur.vitesse_y > 0
                          and ancien_rect.bottom <= self.rect.top + 12
                          and joueur.rect.bottom >= self.rect.top)
        if tombe_sur_tete and self.prendre_un_coup():
            joueur.rect.bottom = self.rect.top
            joueur.vitesse_y = -13
            joueur.au_sol = False
            # Évite de perdre une vie juste après un coup réussi.
            joueur.invincible = max(joueur.invincible, 30)
            return True
        joueur.prendre_un_coup()
        return False
