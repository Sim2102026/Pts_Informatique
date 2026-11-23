"""Les menus : une classe MÈRE Menu et deux classes FILLES.

    Menu            (MÈRE : titre, options, sélection avec les flèches, dessin)
     ├── MenuAccueil   (FILLE : écran de départ, affiche les commandes)
     └── MenuFin       (FILLE : écran de victoire ou de défaite, affiche le score)
"""
import pygame

import config

BLANC = (255, 255, 255)
JAUNE = (255, 215, 80)
GRIS = (200, 200, 210)


class Menu:

    def __init__(self, titre, options):
        pygame.font.init()            # nécessaire pour écrire du texte
        self.titre = titre
        self.options = options        # ex: ["Jouer", "Quitter"]
        self.selection = 0            # numéro de l'option surlignée
        self.police_titre = pygame.font.Font(None, 80)
        self.police = pygame.font.Font(None, 48)
        self.petite_police = pygame.font.Font(None, 32)

    def gerer_touche(self, touche):
        """Réagit à une touche. Renvoie le nom de l'option choisie
        quand on valide avec Entrée, sinon None (= rien de choisi)."""
        if touche == pygame.K_DOWN:
            # % len(...) : après la dernière option, on revient à la première
            self.selection = (self.selection + 1) % len(self.options)
        elif touche == pygame.K_UP:
            self.selection = (self.selection - 1) % len(self.options)
        elif touche in (pygame.K_RETURN, pygame.K_SPACE):
            return self.options[self.selection]
        return None

    def lignes_infos(self):
        """Petites lignes de texte sous le titre. Vide par défaut :
        les classes filles la REDÉFINISSENT."""
        return []

    def ecrire_centre(self, ecran, texte, police, couleur, y):
        """Écrit un texte centré horizontalement à la hauteur y."""
        image = police.render(texte, True, couleur)
        ecran.blit(image, image.get_rect(center=(config.LARGEUR // 2, y)))

    def dessiner(self, ecran):
        # 1) Un voile noir à moitié transparent par-dessus le jeu.
        #    SRCALPHA = l'image accepte la transparence ; 190 = opacité (0 à 255)
        voile = pygame.Surface((config.LARGEUR, config.HAUTEUR), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 190))
        ecran.blit(voile, (0, 0))

        # 2) Le titre
        self.ecrire_centre(ecran, self.titre, self.police_titre, BLANC, 170)

        # 3) Les lignes d'infos (différentes selon la classe fille)
        y = 250
        for ligne in self.lignes_infos():
            self.ecrire_centre(ecran, ligne, self.petite_police, GRIS, y)
            y += 35

        # 4) Les options : celle qui est sélectionnée est en jaune avec des flèches
        y = 400
        for i, option in enumerate(self.options):
            if i == self.selection:
                self.ecrire_centre(ecran, f"> {option} <", self.police, JAUNE, y)
            else:
                self.ecrire_centre(ecran, option, self.police, BLANC, y)
            y += 60


class MenuAccueil(Menu):

    def __init__(self):
        super().__init__(config.TITRE, ["Jouer", "Sauvegardes", "Quitter"])

    def lignes_infos(self):
        return [
            "Flèches : courir     Espace : sauter",
            "Ramasse les fruits et atteins le trophée !",
        ]


class MenuFin(Menu):

    def __init__(self, gagne, score):
        if gagne:
            titre = "Bravo, tu as gagné !"
        else:
            titre = "Perdu..."
        super().__init__(titre, ["Rejouer", "Quitter"])
        self.gagne = gagne
        self.score = score

    def lignes_infos(self):
        return [f"Score : {self.score}"]

class MenuSauvegardes(Menu):
    """Écran de sélection des cinq emplacements de sauvegarde."""

    def __init__(self, emplacements):
        self.emplacements = emplacements
        options = []
        for slot in range(1, 6):
            donnees = emplacements.get(slot)
            if donnees:
                date = donnees.get("updated_at")
                if hasattr(date, "strftime"):
                    date_texte = date.strftime("%d/%m %H:%M")
                elif date:
                    date_texte = str(date)[:16]
                else:
                    date_texte = "date inconnue"
                options.append(
                    f"Slot {slot} | {donnees.get('niveau', 'niveau_1')} | "
                    f"{donnees.get('score', 0)} pts | {date_texte}"
                )
            else:
                options.append(f"Slot {slot}  |  Vide")
        options.append("Retour")
        super().__init__("Choisir une sauvegarde", options)
        self.police = pygame.font.Font(None, 29)
        self.petite_police = pygame.font.Font(None, 26)

    def lignes_infos(self):
        return ["Entrée : charger le slot choisi ou commencer une nouvelle partie"]

    def dessiner(self, ecran):
        voile = pygame.Surface((config.LARGEUR, config.HAUTEUR), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 205))
        ecran.blit(voile, (0, 0))
        self.ecrire_centre(ecran, self.titre, self.police_titre, BLANC, 125)
        self.ecrire_centre(ecran, self.lignes_infos()[0], self.petite_police, GRIS, 205)
        y = 285
        for i, option in enumerate(self.options):
            couleur = JAUNE if i == self.selection else BLANC
            texte = f"> {option} <" if i == self.selection else option
            self.ecrire_centre(ecran, texte, self.police, couleur, y)
            y += 48
