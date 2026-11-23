"""Point d'entrée : c'est ce fichier qu'on lance avec  python3 main.py"""
from jeu import Jeu

# Ce "if" veut dire : "seulement si on lance CE fichier directement".
# Comme ça, si un tedu basst fait "import main", le jeu ne se lance pas tout seul.
if __name__ == "__main__":
    jeu = Jeu()
    jeu.lancer()
