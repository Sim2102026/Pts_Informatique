import unittest

import pygame

from Objets.Camera import Camera
from Objets.Ennemi import Boss, Ennemi
from Objets.Player import Player
from Objets.plateforme import Plateforme


class TestEnnemi(unittest.TestCase):
    def setUp(self):
        self.image = pygame.Surface((20, 20))
        self.sol = Plateforme([0, 100], pygame.Surface((150, 30)), "sol")
        self.ennemi = Ennemi([50, 80], self.image, "test", 1)
        self.boss = Boss([60, 80], self.image)
        self.joueur = Player([60, 65], self.image, "test", 3, 0)

    def test_patrouille_entre_les_bords(self):
        directions = set()
        for _ in range(200):
            self.ennemi.patrouiller([self.sol])
            directions.add(self.ennemi.direction)
            self.assertGreaterEqual(self.ennemi.rect.left, 0)
            self.assertLessEqual(self.ennemi.rect.right, 150)
            self.assertEqual(self.ennemi.rect.bottom, 100)
        self.assertEqual(directions, {-1, 1})

    def test_chute_et_mur(self):
        self.ennemi.y = 0
        self.ennemi.speed = 0
        for _ in range(50):
            self.ennemi.patrouiller([self.sol])
        self.assertTrue(self.ennemi.au_sol)
        mur = Plateforme([70, 80], self.image, "mur")
        self.ennemi.speed = 2
        self.ennemi.patrouiller([self.sol, mur])
        self.assertEqual(self.ennemi.direction, -1)

    def test_boss_trois_impacts_et_rebond(self):
        for vie in (2, 1, 0):
            self.joueur.y = 65
            self.joueur.update()
            self.boss.contact_joueur(self.joueur, 76)
            self.assertEqual(self.boss.life, vie)
            self.assertLess(self.joueur.vitesse_y, 0)
            if vie == 1:
                self.assertEqual(self.boss.speed, 4)
        position = self.boss.rect.copy()
        self.boss.patrouiller([self.sol])
        self.assertFalse(self.boss.is_alive)
        self.assertEqual(self.boss.rect, position)
        ecran = pygame.Surface((150, 150))
        ecran.fill("white")
        self.boss.draw(ecran)
        self.assertEqual(ecran.get_at(position.center), pygame.Color("white"))

    def test_contact_lateral(self):
        self.boss.contact_joueur(self.joueur, 85)
        self.assertEqual(self.joueur.rect.topleft, (50, 570))
        self.assertEqual(self.boss.life, 3)

    def test_barre_avec_camera(self):
        camera = Camera(150, 150)
        camera.offset_x = 30
        ecran = pygame.Surface((150, 150))
        self.boss.damage()
        self.boss.draw(ecran, camera)
        self.assertEqual(ecran.get_at((30, 70))[:3], (235, 75, 65))
        self.assertEqual(ecran.get_at((49, 70))[:3], (65, 30, 30))
