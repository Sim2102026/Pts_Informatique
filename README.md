
**Test d'intégration**:

L'application est un jeu-vidéo développé sur python avec ses bibliothèques.Il sera une interférence graphique.
Pour le faire fonctionner, il faudra avoir installer les paquets nécessaires comme pygame,os,unittest,psycopg2....
Si vous n'avez pas d'IDE, il faudra lancer des commandes dans le bash:
```bash
  pip install pygame
  pip install psycopg2
  pip install unittest
```
Sinon avec un IDE, l'installation se fait plus facilement sur votre ordinateur.
Puis il faudra lancer le jeu dans avec le fichier "main.py" (dans un ide de préférence)
L'utilisateur aura la possibilité de contrôler le joueur avec les flèches directionnelles du clavier. La touche «f» permettra à l'utilisateur de voir les hitbox qui sont des carrés en rouge.
Nous avions dit dans nos spécifications qu'il sera possiible de l'exécuter sur ordinateur. Il sera possible de l'exécuter sur tous les systèmes d'exploitation.

Lorsque l'utilisateur lance le programme main.py, le joueur aura un menu avec des options telles que quitter,jouer,.......

✅ Menu fonctionne

L'utilisateur pourra contrôler le joueur avec 4 options. Il y a 3 flèches directionnelles. La flèche du haut permet au joueur de sauter. La flèche de droite permet d'aller vers l'avant et la flèche de gauche permet de reculer. La touche «backspace» permet aussi de sauter

✅ Les mouvements du joueur

Les plateformes, les ennemis et le joueur sont des objets. Tous les objets ont des hitbox. Les hitbox sont des objets géométrique pour gérer les collisions.Si le joueur entre collision avec un autre objet, il sera bloqué. Dans le jeu, le joueur est soumis à une gravité qui le fait chuter continuellement mais comme il est sur des plateformes, il ne tombe pas.

✅Gravité, collisions, hitbox

Quand le joueur se déplace, la caméra bouge aussi. 

✅Le joueur peut entrer en collision avec les ennemis
Il peut collecter des objets. Pour chaque objets il gagne un dix points.

✅Score augmenter de 100 points pour le joueur

✅ Le joueur saute dans le vide → réinitialisation

✅ Eliminier ennemis

✅ Trophée





