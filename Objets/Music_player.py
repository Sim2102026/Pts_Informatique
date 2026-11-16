import pygame
import os
pygame.init()
pygame.mixer.init(frequency=16000)
playlist = ["franzian.mp3","mario_dubstep.mp3","lbdlprod.mp3"]

index = 0
pygame.mixer.music.set_volume(0.5)
def jouer_musique(index):
    chemin = os.path.join("Assets", "Music", playlist[index])
    pygame.mixer.music.load(chemin)
    pygame.mixer.music.play()

jouer_musique(index)

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

pygame.quit()


print(pygame.mixer.music.get_volume())
print(pygame.mixer.music.get_busy())

