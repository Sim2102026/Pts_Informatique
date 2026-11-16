import pygame


class Ennemi:
    def __init__(self, position, image, name, life, speed=2):
        self.position = list(position)
        self.image = image
        self.name = name
        self.life = max(0, life)
        self.x, self.y = self.position

        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = image.get_rect(topleft=self.position)

        self.speed = abs(speed)
        self.direction = 1
        self.vitesse_y = 0
        self.gravity = 0.8
        self.vitesse_chute_max = 12
        self.au_sol = False

    def update(self):
        """Synchroniser la position et le rectangle."""
        self.position[:] = [self.x, self.y]
        self.rect.topleft = (round(self.x), round(self.y))

    def faire_demi_tour(self):
        self.direction *= -1

    def vide_devant(self, platforms):
        if self.direction > 0:
            x = self.rect.right
        else:
            x = self.rect.left - 1

        y = self.rect.bottom

        return not any(
            platform.rect.collidepoint(x, y)
            for platform in platforms
        )

    def patrouiller(self, platforms):
        """Avancer, tomber et rester sur les plateformes."""
        if not self.is_alive:
            return

        self.update()

        # Verifier si l'ennemi est pose sur une plateforme.
        self.au_sol = any(
            self.rect.move(0, 1).colliderect(platform.rect)
            for platform in platforms
        )

        if self.au_sol and self.vide_devant(platforms):
            self.faire_demi_tour()

        # Avancer par petits pas pour detecter les murs.
        distance = self.speed

        while distance > 0:
            pas = min(1, distance) * self.direction
            self.x += pas
            self.update()

            obstacles = [
                platform.rect for platform in platforms
                if self.rect.colliderect(platform.rect)
            ]

            if obstacles:
                if self.direction > 0:
                    self.rect.right = min(
                        rect.left for rect in obstacles
                    )
                else:
                    self.rect.left = max(
                        rect.right for rect in obstacles
                    )

                self.x = self.rect.x
                self.faire_demi_tour()
                break

            distance -= abs(pas)

            if self.au_sol and self.vide_devant(platforms):
                self.faire_demi_tour()
                break

        # Appliquer la gravite.
        self.vitesse_y = min(
            self.vitesse_y + self.gravity,
            self.vitesse_chute_max
        )

        self.y += self.vitesse_y
        self.update()
        self.au_sol = False

        obstacles = [
            platform.rect for platform in platforms
            if self.rect.colliderect(platform.rect)
        ]

        if obstacles:
            if self.vitesse_y > 0:
                self.rect.bottom = min(
                    rect.top for rect in obstacles
                )
                self.au_sol = True

            elif self.vitesse_y < 0:
                self.rect.top = max(
                    rect.bottom for rect in obstacles
                )

            self.y = self.rect.y
            self.vitesse_y = 0

        self.update()

    @property
    def is_alive(self):
        return self.life > 0

    def damage(self, amount=1):
        if amount < 0:
            raise ValueError(
                "Les degats doivent etre positifs ou nuls."
            )

        self.life = max(0, self.life - amount)

    def draw(self, screen, camera=None):
        if self.is_alive:
            if camera is not None:
                rect = camera.apply(self.rect)
            else:
                rect = self.rect

            screen.blit(self.image, rect)


class Boss(Ennemi):
    pass
