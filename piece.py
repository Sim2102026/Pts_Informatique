"""La classe FILLE Piece : un fruit animé à ramasser."""
import config
from entite import Entite
from outils import charger_image, decouper_planche, agrandir


def charger_animation_fruit(nom="Apple"):
    planche = charger_image("Items", "Fruits", nom + ".png")
    images = decouper_planche(planche, 32, 32)       # Apple.png = 17 images
    return {"idle": [agrandir(img, config.ECHELLE) for img in images]}


class Piece(Entite):

    def __init__(self, x, y, animations=None):
        if animations is None:
            animations = charger_animation_fruit()
        super().__init__(x, y, animations)
        self.valeur = config.POINTS_FRUIT

    def update(self, plateformes=None):
        """REDÉFINITION COMPLÈTE : un fruit flotte dans les airs.
        On n'appelle PAS super().update() : pas de gravité, pas de
        déplacement. On garde seulement l'animation de la mère."""
        self.animer()
