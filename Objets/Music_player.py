import pygame
import os
pygame.init()
pygame.mixer.init(frequency=16000)

pygame.mixer.music.load(os.path.join('Pts_Informatique/Objets/Assets/Music','franzian.mp3'))
pygame.mixer.music.load(os.path.join('Pts_Informatique/Objets/Assets/Music','mario_dubstep.mp3'))
pygame.mixer.music.load(os.path.join('Pts_Informatique/Objets/Assets/Music','lbdlprod.mp3'))
pygame.mixer.music.play(loops=0, start=250.0, fade_ms=0)
while pygame.mixer.music.get_busy() == True:
    pygame.mixer.music.queue(os.path.join('Pts_Informatique/Objets/Assets/Music','mario_dubstep.mp3'))
    pygame.mixer.music.queue(os.path.join('Pts_Informatique/Objets/Assets/Music','lbdlprod.mp3'))
    continue
pygame.mixer.music.rewind()
pygame.mixer.music.set_volume(0.5)
print(pygame.mixer.music.get_volume())
print(pygame.mixer.music.get_busy())

