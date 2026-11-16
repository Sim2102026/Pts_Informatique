"""Réglages communs à tous les tests (pytest lit ce fichier automatiquement)."""
import os
import sys

# Pendant les tests, on ne veut pas de vraie fenêtre qui s'ouvre :
# le pilote "dummy" fait semblant d'avoir un écran.
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Permet aux tests de faire "import jeu", "import outils"... depuis le dossier parent.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ... et "import aides" depuis le dossier tests.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
