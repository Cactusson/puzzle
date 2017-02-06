import pygame as pg


def close_enough(value, target, tolerance=7):
    return target - tolerance <= value <= target + tolerance


class Piece(pg.sprite.Sprite):
    def __init__(self, index, image, center):
        pg.sprite.Sprite.__init__(self)
        self.index = index
        self.image = image
        self.rect = self.image.get_rect(center=center)
        self.mouse_offset = [0, 0]
        self.grabbed = False

    def get_neighbors(self, pieces):
        self.neighbors = {}
        # LEFT, RIGHT, UP, DOWN
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for piece in pieces:
            for offset in offsets:
                if (piece.index[0] + offset[0] == self.index[0] and
                        piece.index[1] + offset[1] == self.index[1]):
                    self.neighbors[offset] = piece
                    continue

    def is_joinable(self, piece):
        """
        Checks if this piece can be joined to the other one.
        """
        for side in self.neighbors:
            if self.neighbors[side] == piece:
                pos_pairs = {
                        (1, 0): ((self.rect.left, piece.rect.right),
                                 (self.rect.top, piece.rect.top)),
                        (-1, 0): ((self.rect.right, piece.rect.left),
                                  (self.rect.top, piece.rect.top)),
                        (0, 1): ((self.rect.left, piece.rect.left),
                                 (self.rect.top, piece.rect.bottom)),
                        (0, -1): ((self.rect.left, piece.rect.left),
                                  (self.rect.bottom, piece.rect.top))}
                if all((close_enough(*pair) for pair in pos_pairs[side])):
                    return True
        return False

    def check_collide(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def click(self, mouse_pos):
        self.grabbed = True
        self.mouse_offset[0] = self.rect.center[0] - mouse_pos[0]
        self.mouse_offset[1] = self.rect.center[1] - mouse_pos[1]

    def unclick(self):
        self.grabbed = False

    def adjust_pos(self, mouse_pos):
        self.rect.centerx = mouse_pos[0] + self.mouse_offset[0]
        self.rect.centery = mouse_pos[1] + self.mouse_offset[1]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
