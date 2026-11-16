from unittest import TestCase, main
import pygame
from Objets.plateforme import Plateforme

class TesPlateforme(TestCase):
    def setUp(self):
        pygame.init()
        self.image = pygame.Surface((50, 50))
        self.plateforme = Plateforme([10, 20], self.image, "block")

    def test_position(self):
        self.assertEqual(self.plateforme.rect.topleft, (10, 20))

    def test_update(self):
        self.plateforme.x = 30
        self.plateforme.y = 40
        self.plateforme.update()
        self.assertEqual(self.plateforme.rect.topleft, (30, 40))

    if __name__ == "__main__":
        main()