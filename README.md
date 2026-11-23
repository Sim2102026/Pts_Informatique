
# Test d'intégration:

## 1. Objectif

Ce cahier valide, par des tests d'intégration, que les fonctionnalités principales visibles dans le projet s'enchaînent correctement.

L'application est un jeu-vidéo développé sur python avec ses bibliothèques.Il sera une interférence graphique.
Pour le faire fonctionner, il faudra avoir installer les paquets nécessaires comme pygame,os,unittest,psycopg2....

Sinon avec un IDE, l'installation se fait plus facilement sur votre ordinateur.
Puis il faudra lancer le jeu dans avec le fichier "main.py" (dans un ide de préférence)
L'utilisateur aura la possibilité de contrôler le joueur avec les flèches directionnelles du clavier. La touche «f» permettra à l'utilisateur de voir les hitbox qui sont des carrés en rouge.
Nous avions dit dans nos spécifications qu'il sera possiible de l'exécuter sur ordinateur. Il sera possible de l'exécuter sur tous les systèmes d'exploitation.

Lorsque l'utilisateur lance le programme main.py, il fait appel au fichier `jeu.py`. Le fichier `jeu.py` rassemblent l'ensemble des fonctionnalités permisisent par l'utilisateur dont les intéractions se feront par `Niveau.py`, `Joueur.py`, `Camera.py`, les menus et les vies.

> Dans le projet, il y de nombreux tests unitaires effectués par les concepteurs. Toutes les classes en possèdent.

## 2. Tutoriel : fonctionnement attendu

### Étape 1 — Lancement
1. Installer les dépendances via votre IDE (...) ou taper ses commandes sur dans le termnial de votre environnement virtuel:
```bash
  pip install pygame
  pip install psycopg2
  pip install unittest
```
2. Lancer `python main.py`.
3. ✅ une fenêtre s'ouvre
4. ✅ Le jeu doit afficher le menu d'accueil avec 3 options (Jouer, Sauvegardes, quitter).

**Attendu :** L'utilisateur « le jeu » avec les options « Jouer », « Sauvegardes » et « Quitter ».

### Étape 2 — Démarrer une partie
1. Dans le menu d'accueil, l'option « Jouer » est sélectionnée.
2. Appuyer sur Entrée ou Espace.
3. Le niveau est construit depuis `CARTE_LONGUE`.
4. Le joueur apparaît sur une case.

**Attendu :** L'état du jeu passe de `accueil` à `jeu`.

### Étape 3 — Se déplacer et sauter
1. Utiliser la flèche gauche pour aller à gauche.
2. Utiliser la flèche droite pour aller à droite.
3. Utiliser Espace ou flèche du haut pour sauter
4. Le joueur doit être soumis à la gravité (modifiable dans class joueur).
5. Les plateformes doivent empêcher le joueur de les traverser.
6. La caméra doit suivre horizontalement le joueur.

**Attendu :** déplacement, saut, collisions et caméra fonctionnent ensemble.

### Étape 4 — Collecter un fruit et avoir un score
1. Voir un fruit.
2. Le toucher et gagner des points.
3. Le fruit disparaît.
4. Le score augmente de `POINTS_FRUIT` (10 dans `config.py`).

**Attendu :** collision + logique de score + suppression du sprite sont cohérentes.

### Étape 5 — Gérer les ennemis
1. Toucher un ennemi par le côté.
2. Le joueur perd une vie.
3. Après un coup, une période d'invincibilité est active.
4. Si le joueur tombe sur l'ennemi, l'ennemi disparaît et le joueur rebondit.
5. Le score augmente de 10.

**Attendu :** les deux types de collision produisent des résultats différents.

### Étape 6 — Gérer les soins
1. Le joueur perd une vie.
2. Il atteint un cœur.
3. Une vie est restaurée si le joueur n'est pas déjà au maximum.
4. Le cœur disparaît seulement si le soin a réellement été appliqué.

**Attendu :** la vie ne dépasse jamais 3.

### Étape 7 — Chute et réapparition
1. Faire tomber le joueur dans un trou.
2. Une vie est retirée.
3. Le joueur revient à la position initale.

**Attendu :** la chute est traitée comme une perte de vie et non comme une fermeture du jeu.

### Étape 8 — Victoire
1. Atteindre le trophée d'arrivée.
2. Le jeu passe à l'état `fin`.
3. Le menu de fin indique la victoire.
4. Le score final est affiché.

**Attendu :** le parcours de jeu peut se terminer normalement.

### Étape 9 — Choix d'un emplacement, sauvegarde automatique et reprise
1. Depuis le menu principal, choisir « Jouer » ou « Sauvegardes ».
2. Le sélecteur affiche les cinq emplacements (1 à 5), avec le niveau et le score pour les slots occupés.
3. Choisir un slot vide pour démarrer une nouvelle partie, ou un slot occupé pour reprendre cette partie.
4. Pendant la partie, le jeu enregistre automatiquement toutes les 5 secondes dans le seul slot actif.
5. Revenir au menu et sélectionner « Sauvegardes » pour choisir une autre partie.

**Attendu :** les cinq emplacements sont indépendants. Le chargement d'un slot restaure la position, les vies et le score ; l'écriture dans un slot ne modifie pas les quatre autres.

### Étape 10 — Défaite et rejouer
1. Amener les vies à zéro.
2. Le jeu passe à l'écran de défaite.
3. Choisir « Rejouer ».
4. Un nouveau niveau et un nouveau joueur sont créés.
5. Le score revient à 0 et les vies à 3.

**Attendu :** une nouvelle partie est indépendante de la précédente.
