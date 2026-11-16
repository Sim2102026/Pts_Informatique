from unittest import TestCase, main
import pygame
from Objets.Collision import Collision

class TestCollision(TestCase):
    def test_check(self):
        c = Collision()
        obj1 = type("Objet", (), {})
        obj2 = type("Objet", (), {})

        obj1.rect = pygame.Rect(0, 0, 50, 50)
        obj2.rect = pygame.Rect(25, 25, 50, 50)

        self.assertTrue(c.check(obj1, obj2))
        obj2.rect = pygame.Rect(100, 100, 50, 50)
        self.assertFalse(c.check(obj1, obj2))
if __name__ == "__main__":
    main()