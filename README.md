# Pts_Informatique — Environnement

Prototype Pygame simple pour la carte Trello « Class Environnement ».
Il utilise les images du pack **Kenney New Platformer Pack 1.1** fourni avec
le projet. Les images choisies et leur licence d'origine se trouvent dans
`Assets/Kenney/`.

## Lancer

Python 3.10 ou plus récent est nécessaire. Sous Windows, double-cliquer sur
`Lancer.bat`. Le script crée un dossier `.venv` dans le projet et installe
Pygame ; le premier lancement nécessite Internet.

Ou, dans un terminal ouvert dans le dossier :

```console
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe Main.py
```

Sous macOS/Linux, utiliser `.venv/bin/python` à la place de
`.venv\Scripts\python.exe`.

Commandes : gauche/droite ou A/D, Espace ou Haut pour
sauter, R pour revenir au départ et Échap pour quitter.
Q, W et Z ne sont pas des commandes du jeu.

## Animation du personnage

Au sol, un deplacement reel alterne `character_green_walk_a.png` et
`character_green_walk_b.png` toutes les 8 mises a jour. A l'arret ou contre un
mur, le personnage utilise `idle`. En l'air, il utilise `jump`. Les images sont
retournees horizontalement lorsqu'il regarde a gauche. Le compteur se remet
a zero a l'arret, en l'air et lors du retour au point de depart.

## Organisation

- `Environnement.py` : carte, chargement des images, décor, rectangles solides
  et collisions. La fonction `deplacer(rect, dx, dy)` **modifie** le rectangle
  fourni et retourne `(au_sol, choc_vertical)`.
- `Main.py` : boucle Pygame et `JoueurDemo`, un personnage provisoire pour
  vérifier l'environnement. À remplacer par la classe Joueur de l'équipe.
- `requirements.txt` : dépendance Pygame.

Créer la fenêtre avant d'instancier `Environnement` :

```python
pygame.init()
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
environnement = Environnement()
```

Le joueur transmet ses déplacements, puis utilise `choc_vertical` pour annuler
sa vitesse verticale et `au_sol` pour autoriser un saut. Pour dessiner, appeler
`environnement.dessiner(ecran)`, puis dessiner le joueur et actualiser l'écran.

## Carte et limites du prototype

`CARTE` contient 10 lignes de 16 caractères. Chaque case mesure 64 pixels :
`.` est vide, `#` est un bloc de terre et `=` une plateforme suspendue.
Changer ces caractères permet de construire un autre parcours. Utiliser au
moins deux `=` consécutifs pour garder les deux extrémités de l'image.

Tous les blocs sont fixes et solides sur leurs quatre faces. Les décorations
(arbustes, panneau, drapeau) ne provoquent pas de collision. Le drapeau est
un repère visuel ; il n'active pas de victoire. Le point de départ `(64, 450)`
est adapté à la carte actuelle : le déplacer si le sol de départ change.

La physique est volontairement simple : 60 images/seconde, 5 pixels par
image horizontalement, saut de -15 pixels/image et gravité de 0,7. La vitesse
verticale est limitée à 15 pixels/image. Le jeu ralentit si la machine ne
tient pas 60 images/seconde. La collision par `Rect.colliderect()` convient
à ces petits déplacements ; elle n'est pas conçue pour des téléportations ou
des mouvements qui traversent un bloc entier en une image.

Les sons du pack ne sont pas encore intégrés : ils peuvent être ajoutés avec
la classe Sonore. Les classes Ennemis, Jeu complet, Santé, Menu et Caméra
ne sont pas implémentées ici. La nouvelle interface de collision est plus
simple que celle de la première version : ne pas mélanger les deux versions.

## Vérification réalisée

21 contrôles automatiques ont passé : sol, plafond, murs, bords, contact au
repos, saut, absence de double saut, accès à la première plateforme, chute et
retour au départ, vitesse maximale, chemins d'images et dessin, ainsi que
l'alternance des deux images de marche, l'arret, le saut, le mur et le reset
de l'animation. Les commandes reelles de la boucle principale ont ete testees
dans 11 cas, dont Q sans deplacement et les touches A/D et fleches. La boucle de
jeu a également rendu 90 images avec des commandes simulées de déplacement,
saut et fermeture. Un essai manuel au clavier reste utile avant le rendu.

Les scripts de vérification de l'auteur restent séparés du code à présenter.
Le dossier de ce projet ne contient que le prototype et sa documentation.

Graphismes : Kenney, New Platformer Pack 1.1. Texte de licence d'origine :
`Assets/Kenney/License.txt`.
