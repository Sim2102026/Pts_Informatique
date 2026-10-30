import Images

class Plateforme:
    def __init__(self,position,image,name):
        self.position=position
        self.image=image
        self.name=name

position=[(300,200)]
block1=Plateforme(position,Images.block,"block1",)