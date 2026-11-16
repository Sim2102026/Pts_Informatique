class Camera:
#Caméra qui doit suivre joueur à importer dans le main.py
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, player):
        self.offset_x = player.rect.centerx - self.width // 2
        self.offset_y = 0

        if self.offset_x < 0:
            self.offset_x = 0

    def apply(self, rect):
        return rect.move(-self.offset_x,-self.offset_y)