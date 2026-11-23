"""Lance le jeu complet sur Windows/macOS avec un environnement local.

Usage : python lancer_jeu.py
        python lancer_jeu.py --boss   (essai rapide du boss)
        python lancer_jeu.py --check  (installation et verification seulement)
"""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import venv


RACINE = Path(__file__).resolve().parent
ENVIRONNEMENT = RACINE / ".venv-game"


def executer(arguments):
    """Les listes d'arguments acceptent les chemins contenant des espaces."""
    return subprocess.run(arguments, cwd=str(RACINE), check=True)


def preparer_python():
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required (Python 3.12 recommended).")
    exigences = RACINE / "requirements.txt"
    if not exigences.is_file() or not (RACINE / "main.py").is_file():
        raise RuntimeError(
            "Place these launchers next to main.py and requirements.txt "
            "in the fully extracted test project. Do not run inside a ZIP."
        )

    python = ENVIRONNEMENT / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        if ENVIRONNEMENT.exists():
            raise RuntimeError(
                "The .venv-game folder is incomplete or belongs to another OS. "
                "Remove only that generated folder, then launch again."
            )
        print("First launch: creating the game environment...", flush=True)
        venv.EnvBuilder(with_pip=True).create(str(ENVIRONNEMENT))

    # Ne pas inclure les bibliotheques locales dans les futurs commits Git.
    (ENVIRONNEMENT / ".gitignore").write_text("*\n", encoding="utf-8")
    empreinte = hashlib.sha256(exigences.read_bytes()).hexdigest()
    marqueur = ENVIRONNEMENT / ".requirements-sha256"
    dernier = marqueur.read_text(encoding="utf-8").strip() if marqueur.exists() else ""

    verification = subprocess.run(
        [str(python), "-c", "import pygame, psycopg, pytest"],
        cwd=str(RACINE), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if dernier != empreinte or verification.returncode != 0:
        print("Installing game dependencies (Internet required)...", flush=True)
        executer([str(python), "-m", "pip", "install", "--disable-pip-version-check",
                  "-r", str(exigences)])
        # Aucun marqueur de succes si l'installation a echoue.
        executer([str(python), "-c", "import pygame, psycopg, pytest"])
        marqueur.write_text(empreinte, encoding="utf-8")
    return python


def main():
    parser = argparse.ArgumentParser(description="Start the complete Platformer game")
    choix = parser.add_mutually_exclusive_group()
    choix.add_argument("--boss", action="store_true", help="Start directly in the boss room")
    choix.add_argument("--check", action="store_true", help="Install and check without opening the game")
    args = parser.parse_args()
    try:
        python = preparer_python()
        if args.check:
            executer([str(python), "-c", "from jeu import Jeu; print('Game imports: OK')"])
            print("Ready. Start Lancer_Windows.bat or Lancer_Mac.command.", flush=True)
            return 0
        entree = RACINE / ("demo_boss.py" if args.boss else "main.py")
        if not entree.is_file():
            raise RuntimeError("Missing game entry point: " + entree.name)
        print("Starting " + entree.name + "...", flush=True)
        # Pas besoin d'activer l'environnement : son interpreteur est utilise directement.
        return subprocess.run([str(python), str(entree)], cwd=str(RACINE)).returncode
    except (OSError, RuntimeError, subprocess.CalledProcessError) as erreur:
        print("\nLaunch failed: " + str(erreur), file=sys.stderr, flush=True)
        print("Check the error above. On first launch, an Internet connection is required.",
              file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
