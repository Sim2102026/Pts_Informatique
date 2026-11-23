"""Arène fixe : zone sûre à gauche, déclencheur, puis combat."""
import pygame
import config
from niveau import Niveau
from porte import Porte
from boss import Boss
from arrivee import Arrivee


def carte_salle():
    lignes = [list("X" + "." * 18 + "X") for _ in range(13)]
    lignes[0] = list("X" * 20)
    lignes[12] = list("X" * 20)
    lignes[11][2] = "P"
    for x in (4, 5, 14, 15):
        lignes[9][x] = "X"
    return ["".join(ligne) for ligne in lignes]


class SalleBoss(Niveau):
    def __init__(self):
        super().__init__(carte_salle())
        # Bloc de pierre déjà présent dans le terrain Pixel Adventure.
        from outils import charger_image
        terrain = charger_image("Terrain", "Terrain (16x16).png")
        pierre = terrain.subsurface(pygame.Rect(0, 0, 48, 48))
        for bloc in self.plateformes:
            bloc.image = pierre
        self.sol_y = config.HAUTEUR - config.TAILLE_TUILE
        self.porte = Porte(120, self.sol_y)
        self.boss = Boss(650, self.sol_y, 48, config.LARGEUR - 48)
        self.declenche = False
        self.recompense = False

    def mettre_a_jour_boss(self, dt, joueur, ancien_rect):
        if not self.declenche and joueur.rect.centerx >= 320:
            self.declenche = True
            self.boss.activer()
        self.boss.update(dt, joueur)
        coup = self.boss.toucher_joueur(joueur, ancien_rect)
        if self.boss.etat == "vaincu":
            self.reveler_trophee()
        return coup

    def reveler_trophee(self):
        if not self.recompense:
            self.recompense = True
            self.arrivee.add(Arrivee(810, self.sol_y - 64))

    def dessiner(self, ecran, camera=None):
        ecran.fill((25, 27, 44))
        for x in range(48, config.LARGEUR - 48, 48):
            for y in range(64, self.sol_y, 48):
                pygame.draw.rect(ecran, (35, 38, 56), (x + 2, y + 2, 44, 44), 1)
        ecran.blit(self.porte.image, self.porte.rect)
        super().dessiner(ecran, camera)
        if self.boss.etat != "vaincu":
            ecran.blit(self.boss.image, self.boss.rect)

    def dessiner_infos(self, ecran, police):
        boss = self.boss
        if not self.declenche:
            texte = "Avance pour reveiller le Roi Slime"
        elif boss.etat == "vaincu":
            texte = "Boss vaincu ! Ramasse le trophee."
        else:
            texte = {"patrouille": "Attention au slime !",
                     "charge": "Il charge... Prepare ton saut !",
                     "attaque": "Saute pour eviter la charge !",
                     "fatigue": "Fatigue ! Saute sur sa tete !",
                     "blesse": "Bien joue !", "mort": "Victoire !"}[boss.etat]
            fond = pygame.Rect(280, 68, 400, 18)
            pygame.draw.rect(ecran, (65, 45, 70), fond, border_radius=6)
            if boss.vies:
                barre = fond.copy()
                barre.width = round(400 * boss.vies / boss.VIES_MAX)
                pygame.draw.rect(ecran, (184, 101, 233), barre, border_radius=6)
        couleur = (164, 246, 177) if boss.vulnerable else (240, 228, 205)
        image = police.render(texte, True, couleur)
        ecran.blit(image, image.get_rect(center=(config.LARGEUR // 2, 110)))
