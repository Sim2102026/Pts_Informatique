"""La classe Jeu : elle ouvre la fenêtre, fait tourner la boucle du jeu,
et CONTIENT tous les objets (composition : le jeu "a un" niveau,
"a un" joueur, "a un" menu...).

Le jeu peut être dans 3 états :
    "accueil" -> le menu de départ est affiché
    "jeu"     -> on joue
    "fin"     -> l'écran de victoire ou de défaite est affiché
"""
import pygame
from types import SimpleNamespace

import config
from outils import charger_image
from joueur import Joueur
from niveau import Niveau
from camera import Camera
from menu import MenuAccueil, MenuFin, MenuSauvegardes
from affichage_sante import AffichageSante
from salle_boss import SalleBoss
import db


class Jeu:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((config.LARGEUR, config.HAUTEUR))
        pygame.display.set_caption(config.TITRE)
        self.horloge = pygame.time.Clock()
        self.en_cours = True
        # La sauvegarde est automatique : un checkpoint est écrit de manière périodique.
        self.intervalle_sauvegarde = 5.0
        self.temps_depuis_sauvegarde = 0.0
        self.sauvegarde_disponible = False
        self.slot_actif = None
        try:
            db.initialiser_base()
            self.sauvegarde_disponible = True
        except Exception:
            # Le jeu reste lançable même si PostgreSQL n'est pas configuré.
            self.sauvegarde_disponible = False


        self.tuile_fond = charger_image("Background", "Blue.png")
        self.police = pygame.font.Font(None, 36)
        # Les coeurs en haut à droite (classe écrite par Zitong)
        self.affichage_sante = AffichageSante(maximum=config.VIES_DEPART, taille=48)

        self.nouvelle_partie()       # le niveau est visible derrière le menu
        self.etat = "accueil"
        self.menu = MenuAccueil()

    def nouvelle_partie(self):
        """Crée un niveau tout neuf et un joueur à la case de départ."""
        self.niveau = Niveau()
        x, y = self.niveau.position_depart
        self.joueur = Joueur(x, y)
        self.joueur.largeur_monde = self.niveau.largeur
        self.camera = Camera(config.LARGEUR, self.niveau.largeur)
        self.camera.update(self.joueur)
        self.scene = "niveau_1"
        self.transition = None
        self.score_entree_boss = 0
        self.reessayer_boss = False

    def porte_proche(self):
        return next((p for p in self.niveau.portes if p.proche(self.joueur)), None)

    def commencer_entree(self):
        porte = self.porte_proche()
        if porte is None or self.transition is not None:
            return False
        porte.ouvrir()
        self.transition = 0.0
        return True

    def entrer_salle_boss(self, restaurer_vies=False):
        """Change de carte, conserve le score et les vies à l'entrée normale."""
        self.score_entree_boss = self.joueur.score
        self.niveau = SalleBoss()
        self.scene = "salle_boss"
        self.joueur.rect.topleft = self.niveau.position_depart
        self.joueur.largeur_monde = self.niveau.largeur
        self.joueur.vitesse_x = self.joueur.vitesse_y = 0
        self.joueur.au_sol = False
        self.joueur.invincible = 60
        if restaurer_vies:
            self.joueur.vies = config.VIES_DEPART
        self.camera = Camera(config.LARGEUR, self.niveau.largeur)
        self.camera.update(self.joueur)
        self.temps_depuis_sauvegarde = 0.0

    def finir_partie(self, gagne):
        self.reessayer_boss = self.scene == "salle_boss" and not gagne
        self.etat = "fin"
        self.menu = MenuFin(gagne, self.joueur.score)

    def executer_action(self, action):
        """Traite une action du menu principal ou de sélection des slots."""
        if action in ("Jouer", "Sauvegardes"):
            self.ouvrir_menu_sauvegardes()
        elif action == "Retour":
            self.etat = "accueil"
            self.menu = MenuAccueil()
        elif isinstance(action, str) and action.startswith("Slot "):
            try:
                slot = int(action.split("|", 1)[0].replace("Slot", "").strip())
            except (ValueError, IndexError):
                return
            self.selectionner_sauvegarde(slot)
        elif action == "Rejouer":
            if self.reessayer_boss:
                self.joueur.score = self.score_entree_boss
                self.entrer_salle_boss(restaurer_vies=True)
                self.reessayer_boss = False
            else:
                self.nouvelle_partie()
            self.temps_depuis_sauvegarde = 0.0
            self.etat = "jeu"
        elif action == "Quitter":
            self.sauvegarder_automatiquement()
            self.en_cours = False

    def ouvrir_menu_sauvegardes(self):
        """Affiche les cinq emplacements depuis le menu principal."""
        emplacements = {slot: None for slot in range(1, 6)}
        if self.sauvegarde_disponible:
            try:
                emplacements = db.lister_sauvegardes()
            except Exception:
                self.sauvegarde_disponible = False
        self.menu = MenuSauvegardes(emplacements)
        self.etat = "slots"

    def selectionner_sauvegarde(self, slot):
        """Charge le slot choisi ou démarre une nouvelle partie dans ce slot vide."""
        if not 1 <= slot <= 5:
            return False
        if not self.sauvegarde_disponible:
            self.slot_actif = slot
            self.nouvelle_partie()
            self.etat = "jeu"
            return True
        try:
            sauvegarde = db.charger_sauvegarde(slot)
        except Exception:
            return False

        self.slot_actif = slot
        self.nouvelle_partie()
        if sauvegarde is not None:
            self.joueur.score = sauvegarde["score"]
            if sauvegarde.get("niveau") in ("salle_boss", "boss_vaincu"):
                # Un combat chargé recommence à l'entrée avec les deux vies pleines.
                self.entrer_salle_boss(restaurer_vies=True)
                if sauvegarde["niveau"] == "boss_vaincu":
                    self.niveau.boss.vies = 0
                    self.niveau.boss.changer_etat("vaincu")
                    self.niveau.declenche = True
                    self.niveau.reveler_trophee()
            else:
                self.joueur.rect.topleft = (sauvegarde["x"], sauvegarde["y"])
                self.joueur.vies = max(1, sauvegarde["vies"])
            self.camera.update(self.joueur)

        self.temps_depuis_sauvegarde = 0.0
        self.etat = "jeu"
        return True

    def sauvegarder_automatiquement(self):
        """Met à jour automatiquement le slot actif, sans toucher aux autres."""
        if (not self.sauvegarde_disponible or self.etat != "jeu"
                or self.slot_actif is None):
            return False
        try:
            scene = self.scene
            joueur_sauve = self.joueur
            if scene == "salle_boss":
                vaincu = self.niveau.boss.vies == 0
                scene = "boss_vaincu" if vaincu else "salle_boss"
                # Pas de reprise au milieu d'une charge : checkpoint d'entrée.
                x, y = self.niveau.position_depart
                joueur_sauve = SimpleNamespace(
                    rect=pygame.Rect(x, y, 64, 64), vies=config.VIES_DEPART,
                    score=self.joueur.score if vaincu else self.score_entree_boss)
            db.sauvegarder(
                self.slot_actif,
                joueur_sauve,
                niveau=scene,
                gagne=False,
            )
            self.temps_depuis_sauvegarde = 0.0
            return True
        except Exception:
            self.sauvegarde_disponible = False
            return False
    # ------------------------------------------------------------------
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.sauvegarder_automatiquement()
                self.en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    self.sauvegarder_automatiquement()
                    self.en_cours = False
                elif self.etat == "jeu":
                    if self.transition is not None:
                        continue
                    if evenement.key == pygame.K_UP and self.commencer_entree():
                        continue
                    if evenement.key in (pygame.K_SPACE, pygame.K_UP):
                        self.joueur.sauter()
                else:
                    # Dans un menu : c'est le menu qui décide quoi faire de la touche
                    action = self.menu.gerer_touche(evenement.key)
                    self.executer_action(action)

    def verifier_collisions(self):
        for piece in pygame.sprite.spritecollide(self.joueur, self.niveau.pieces, True):
            self.joueur.ramasser(piece)

        for ennemi in pygame.sprite.spritecollide(self.joueur, self.niveau.ennemis, False):
            if self.joueur.vitesse_y > 0 and self.joueur.rect.bottom < ennemi.rect.centery:
                self.joueur.ecraser(ennemi)
            else:
                self.joueur.prendre_un_coup()

        for soin in pygame.sprite.spritecollide(self.joueur, self.niveau.soins, False):
            soin.ramasser(self.joueur)

    def mettre_a_jour(self):
        if self.etat != "jeu":
            return               # dans un menu, le jeu est "en pause"

        dt = min(self.horloge.get_time() / 1000 or 1 / config.FPS, 0.05)
        if self.transition is not None:
            avant = self.transition
            self.transition += dt
            if avant < 0.4 <= self.transition:
                self.entrer_salle_boss()
                self.sauvegarder_automatiquement()
            if self.transition >= 0.8:
                self.transition = None
            return

        self.temps_depuis_sauvegarde += self.horloge.get_time() / 1000
        if self.temps_depuis_sauvegarde >= self.intervalle_sauvegarde:
            self.sauvegarder_automatiquement()

        self.joueur.lire_clavier(pygame.key.get_pressed())
        ancien_rect = self.joueur.rect.copy()
        self.joueur.update(self.niveau.plateformes)
        self.niveau.ennemis.update(self.niveau.plateformes)
        self.niveau.pieces.update()
        self.niveau.soins.update(self.horloge.get_time() / 1000)
        self.verifier_collisions()
        if self.scene == "salle_boss" and self.joueur.vies > 0:
            if self.niveau.mettre_a_jour_boss(dt, self.joueur, ancien_rect):
                if self.niveau.boss.vies == 0:
                    self.joueur.score += self.niveau.boss.POINTS

        # Tombé dans un trou ? (le haut du joueur est sous le bas de l'écran)
        if self.joueur.rect.top > config.HAUTEUR:
            self.joueur.reapparaitre(*self.niveau.position_depart)

        self.camera.update(self.joueur)

        if self.joueur.est_mort():
            self.finir_partie(gagne=False)
        elif pygame.sprite.spritecollide(self.joueur, self.niveau.arrivee, False):
            self.finir_partie(gagne=True)

    # ------------------------------------------------------------------
    def dessiner_infos(self):
        texte = f"Score : {self.joueur.score}"
        couleur = (240, 228, 205) if self.scene == "salle_boss" else (40, 40, 60)
        image = self.police.render(texte, True, couleur)
        self.ecran.blit(image, (15, 12))
        self.affichage_sante.dessiner(self.ecran, self.joueur, y=10)
        police = pygame.font.Font(None, 26)
        if self.scene == "salle_boss":
            self.niveau.dessiner_infos(self.ecran, police)
        elif self.porte_proche():
            image = police.render("Haut : entrer dans la salle du boss", True, (255, 245, 210))
            fond = image.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR - 90)).inflate(24, 16)
            pygame.draw.rect(self.ecran, (35, 30, 50), fond, border_radius=8)
            self.ecran.blit(image, image.get_rect(center=fond.center))

    def dessiner(self):
        taille = self.tuile_fond.get_width()
        depart_x = -int(self.camera.offset_x * 0.25) % taille - taille
        for x in range(depart_x, config.LARGEUR, taille):
            for y in range(0, config.HAUTEUR, taille):
                self.ecran.blit(self.tuile_fond, (x, y))

        self.niveau.dessiner(self.ecran, self.camera)
        # Clignotement pendant l'invincibilité : visible 5 frames, caché 5 frames...
        if self.joueur.invincible == 0 or (self.joueur.invincible // 5) % 2 == 0:
            self.ecran.blit(self.joueur.image, self.camera.appliquer(self.joueur.rect))

        if self.etat == "jeu":
            self.dessiner_infos()
        else:
            self.menu.dessiner(self.ecran)   # le menu par-dessus tout le reste

        if self.transition is not None:
            opacite = 1 - abs(self.transition - 0.4) / 0.4
            voile = pygame.Surface(self.ecran.get_size())
            voile.fill((0, 0, 0))
            voile.set_alpha(round(255 * max(0, min(1, opacite))))
            self.ecran.blit(voile, (0, 0))

        pygame.display.flip()

    def lancer(self):
        while self.en_cours:
            self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            self.horloge.tick(config.FPS)
        pygame.quit()
