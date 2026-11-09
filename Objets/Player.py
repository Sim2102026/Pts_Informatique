
class Player:
    def __init__(self,position,image,name,life,compteur_piece):
        self.position=position
        self.image=image
        self.name=name
        self.life=life
        self.compteur_piece=compteur_piece
    #ICI il faudra réorganiser le code, Les attributs de la classe Player doivent contenir un attribut x et y
    def move_right(self):
        pass
    def move_left(self):
        pass

    def collect_piece(self):
        pass

    def damage(self):
        pass
position_player=[50, 744]