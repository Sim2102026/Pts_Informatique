import pygame
import sys

class Jeu:
    def __init__(self):
        # 1. Initialisation de Pygame
        pygame.init()
        
        # 2. Configuration de la fenêtre
        self.largeur = 800
        self.hauteur = 600
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Projet ISEP - Jeu de Plateforme 2D")
        
        # 3. Gestion du temps (FPS)
        self.horloge = pygame.time.Clock()
        self.fps = 60
        
        # 4. État du jeu
        self.en_cours = True

    def gerer_evenements(self):
        """Écoute les actions du joueur (clavier, clic, fermeture)."""
        for event in pygame.event.get():
            # Si l'utilisateur clique sur la croix rouge de la fenêtre
            if event.type == pygame.QUIT:
                self.en_cours = False

    def mettre_a_jour(self):
        """Met à jour la logique du jeu (positions, physique, collisions)."""
        # C'est ici que tu mettras à jour la position de ton futur Joueur
        pass

    def dessiner(self):
        """Affiche les éléments visuels sur l'écran."""
        # Remplir le fond en bleu ciel (code couleur RGB)
        self.ecran.fill((135, 206, 235)) 
        
        # C'est ici que tu demanderas à la classe de Simon de dessiner l'environnement
        
        # Rafraîchir l'écran pour afficher la nouvelle image
        pygame.display.flip()

    def executer(self):
        """La boucle principale du jeu (Game Loop)."""
        while self.en_cours:
            self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            
            # Limite le jeu à 60 images par seconde
            self.horloge.tick(self.fps) 
        
        # Quitter proprement une fois la boucle terminée (croix rouge cliquée)
        pygame.quit()
        sys.exit()

# Lancement du jeu
if __name__ == "__main__":
    mon_jeu = Jeu()
    mon_jeu.executer()