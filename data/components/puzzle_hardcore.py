import pygame as pg

from .puzzle import Puzzle, get_size
from .piece_hardcore import PieceHardcore
from .section_hardcore import SectionHardcore


class PuzzleHardcore(Puzzle):
    def __init__(self, finished_callback, pic, pic2, turn_time, amount=4):
        self.finished_callback = finished_callback
        self.turn_time = turn_time
        self.pieces = self.make_pieces(pic, pic2, amount)
        self.spread_pieces()
        self.sections = []
        # objs : pieces + sections, for drawing in the right order
        self.objs = self.pieces.copy()
        self.grabbed = None
        self.finished = False

    def make_pieces(self, pic, pic2, amount):
        width = 640
        height = 480
        rows, cols = get_size(amount)
        w = width // cols
        h = height // rows
        pieces = []
        step_x = 800 // cols
        step_y = 600 // rows
        for i in range(cols):
            for j in range(rows):
                image = pg.Surface((w, h)).convert()
                image.blit(pic, (0, 0), area=(i*w, j*h, w, h))
                image2 = pg.Surface((w, h)).convert()
                image2.blit(pic2, (0, 0), area=(i*w, j*h, w, h))
                centerx = step_x * i + step_x // 2
                centery = step_y * j + step_y // 2
                center = (centerx, centery)
                piece = PieceHardcore((i, j), image, image2, center,
                                      self.turn_time)
                pieces.append(piece)

        for piece in pieces:
            piece.get_neighbors(pieces)
        return pieces

    def click(self, mouse_pos):
        Puzzle.click(self, mouse_pos)

    def join_pieces(self, piece1, piece2):
        Puzzle.join_pieces(self, piece1, piece2)
        piece1.stop_turning()
        piece2.stop_turning()
        piece2.auto_turn(piece1.get_num_of_image())
        section = SectionHardcore((piece1, piece2), self.turn_time)
        return section

    def update(self, mouse_pos, dt):
        for obj in self.objs:
            if obj is not self.grabbed:
                obj.update(dt)
        Puzzle.update(self, mouse_pos, dt)
