#!/bin/bash
# Finder ouvre ce fichier dans Terminal. Les espaces du chemin sont acceptes.
cd -- "$(dirname -- "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3.10 or newer is required. Python 3.12 is recommended."
    echo "Install Python from https://www.python.org/downloads/macos/"
    read -r -p "Press Enter to close... "
    exit 1
fi
python3 "./lancer_jeu.py" "$@"
game_exit=$?
if [ "$game_exit" -ne 0 ]; then
    echo
    echo "The game could not start or stopped with an error. Read the message above."
    read -r -p "Press Enter to close... "
fi
exit "$game_exit"
