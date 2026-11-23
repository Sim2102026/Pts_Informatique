from pathlib import Path
import pygame

DOSSIER_MUSIQUE = Path(__file__).resolve().parent / "Assets" / "Music"
PLAYLIST = [
    "franzian.mp3",
    "mario_dubstep.mp3",
    "lbdlprod.mp3",
]


def initialiser(volume=0.5):
    """Initialise le mixer si nécessaire et règle le volume."""
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=16000)
    pygame.mixer.music.set_volume(volume)


def jouer(index=0, boucle=-1):
    """Joue le morceau demandé. boucle=-1 signifie lecture en boucle."""
    if not PLAYLIST:
        return
    index %= len(PLAYLIST)
    chemin = DOSSIER_MUSIQUE / PLAYLIST[index]
    if not chemin.exists():
        raise FileNotFoundError(f"Fichier musique absent : {chemin}")
    pygame.mixer.music.load(str(chemin))
    pygame.mixer.music.play(loops=boucle)


def pause():
    pygame.mixer.music.pause()


def reprendre():
    pygame.mixer.music.unpause()


def arreter():
    pygame.mixer.music.stop()


def volume(valeur):
    """Volume entre 0.0 et 1.0."""
    pygame.mixer.music.set_volume(max(0.0, min(1.0, valeur)))


if __name__ == "__main__":
    pygame.init()
    initialiser(0.5)
    jouer(0)
    print("Volume :", pygame.mixer.music.get_volume())
    print("Lecture active :", pygame.mixer.music.get_busy())

    try:
        while pygame.mixer.music.get_busy():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
            pygame.time.wait(50)
    finally:
        arreter()
        pygame.quit()
