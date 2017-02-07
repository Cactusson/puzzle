import random

from .hardcore_obj import HardcoreObj
from .piece import Piece


class PieceHardcore(Piece, HardcoreObj):
    def __init__(self, index, image, image2, center, turn_time):
        Piece.__init__(self, index, image, center)
        HardcoreObj.__init__(self, turn_time)
        self.image2 = image2
        self.show_image = random.choice([image, image2])

    def get_num_of_image(self):
        return 1 if self.show_image == self.image else 2

    def click(self, mouse_pos):
        Piece.click(self, mouse_pos)
        HardcoreObj.click(self)

    def unclick(self):
        Piece.unclick(self)
        HardcoreObj.unclick(self)

    def draw(self, surface):
        surface.blit(self.show_image, self.rect)

    def update(self, dt):
        HardcoreObj.update(self, dt)
