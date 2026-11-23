"""Porte Kenney : approcher puis appuyer sur Haut pour entrer."""
from pathlib import Path
import pygame

DOSSIER_BOSS = Path(__file__).resolve().parent / "Assets" / "Boss"


def charger_asset(nom):
    return pygame.image.load(str(DOSSIER_BOSS / nom)).convert_alpha()


class Porte(pygame.sprite.Sprite):
    def __init__(self, centre_x, sol_y):
        super().__init__()
        self.images = {}
        for etat in ("closed", "open"):
            image = pygame.Surface((64, 128), pygame.SRCALPHA)
            for suffixe, y in (("_top", 0), ("", 64)):
                tuile = charger_asset(f"door_{etat}{suffixe}.png")
                image.blit(pygame.transform.scale(tuile, (64, 64)), (0, y))
            self.images[etat] = image
        self.image = self.images["closed"]
        self.rect = self.image.get_rect(midbottom=(centre_x, sol_y))

    def proche(self, joueur):
        return (joueur.au_sol and joueur.vies > 0
                and abs(joueur.rect.centerx - self.rect.centerx) <= 52
                and abs(joueur.rect.bottom - self.rect.bottom) <= 8)

    def ouvrir(self):
        self.image = self.images["open"]
