import pygame as pg
import random

from .. import prepare

from . import settings
from .piece import Piece
from .section import Section


def get_size(amount):
    difference = float('inf')
    for i in range(1, amount + 1):
        if amount % i == 0:
            diff = abs(amount // i - i)
            if diff < difference:
                nums = amount // i, i
                difference = diff
    return min(nums), max(nums)


class Puzzle:
    def __init__(self, finished_callback, pic, amount):
        self.finished_callback = finished_callback
        self.pieces = self.make_pieces(pic, amount)
        self.spread_pieces()
        self.sections = []
        # objs = pieces + sections, for drawing in the right order
        self.objs = self.pieces.copy()
        self.grabbed = None
        self.finished = False

    def make_pieces(self, pic, amount):
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
                centerx = step_x * i + step_x // 2
                centery = step_y * j + step_y // 2
                center = (centerx, centery)
                piece = Piece((i, j), image, center)
                pieces.append(piece)

        for piece in pieces:
            piece.get_neighbors(pieces)
        return pieces

    def spread_pieces(self):
        centers = []
        for piece in self.pieces:
            centers.append(piece.rect.center)
        random.shuffle(centers)
        for piece, center in zip(self.pieces, centers):
            piece.rect.center = center

    def check_piece_on_pieces(self, current_piece):
        for piece in self.pieces:
            if piece is current_piece:
                continue
            if current_piece.is_joinable(piece):
                section = self.join_pieces(current_piece, piece)
                self.change_order(current_piece, piece, new=section)
                if settings.sound_on:
                    prepare.SFX['connect'].play()
                return True
        return False

    def check_piece_on_sections(self, current_piece):
        for section in self.sections:
            if current_piece in section.pieces:
                continue
            if section.can_add(current_piece):
                section.add_piece(current_piece)
                self.change_order(current_piece, jump=section)
                if settings.sound_on:
                    prepare.SFX['connect'].play()
                return True
        return False

    def check_section_on_pieces(self, current_section):
        for piece in self.pieces:
            if piece in current_section.pieces:
                continue
            if current_section.can_add(piece):
                current_section.add_piece(piece)
                self.change_order(piece, jump=current_section)
                if settings.sound_on:
                    prepare.SFX['connect'].play()
                return True
        return False

    def check_section_on_sections(self, current_section):
        for section in self.sections:
            if section is current_section:
                continue
            if current_section.can_add_section(section):
                current_section.add_section(section)
                self.change_order(section, jump=current_section)
                if settings.sound_on:
                    prepare.SFX['connect'].play()
                return True
        return False

    def click(self, mouse_pos):
        for obj in reversed(self.objs):
            if obj.check_collide(mouse_pos):
                self.grabbed = obj
                self.grabbed.click(mouse_pos)
                self.change_order(jump=self.grabbed)
                return

    def unclick(self):
        if not self.grabbed:
            return
        if isinstance(self.grabbed, Piece):
            if not self.check_piece_on_sections(self.grabbed):
                self.check_piece_on_pieces(self.grabbed)
        elif isinstance(self.grabbed, Section):
            if not self.check_section_on_sections(self.grabbed):
                self.check_section_on_pieces(self.grabbed)
        self.grabbed.unclick()
        self.grabbed = None
        if not self.finished:
            if self.check_finished():
                self.finished = True
                self.finished_callback()

    def join_pieces(self, piece1, piece2):
        for side in piece2.neighbors:
            if piece1 is piece2.neighbors[side]:
                if side == (-1, 0):
                    piece2.rect.right = piece1.rect.left
                    piece2.rect.top = piece1.rect.top
                elif side == (1, 0):
                    piece2.rect.left = piece1.rect.right
                    piece2.rect.top = piece1.rect.top
                elif side == (0, -1):
                    piece2.rect.left = piece1.rect.left
                    piece2.rect.bottom = piece1.rect.top
                elif side == (0, 1):
                    piece2.rect.left = piece1.rect.left
                    piece2.rect.top = piece1.rect.bottom

        section = Section((piece1, piece2))
        return section

    def change_order(self, *args, **kwargs):
        for obj in args:
            self.objs.remove(obj)
            if obj in self.pieces:
                self.pieces.remove(obj)
            elif obj in self.sections:
                self.sections.remove(obj)
        if 'new' in kwargs:
            new_obj = kwargs['new']
            self.objs.append(new_obj)
            self.sections.append(new_obj)
        if 'jump' in kwargs:
            jump_obj = kwargs['jump']
            self.objs.remove(jump_obj)
            self.objs.append(jump_obj)

    def check_finished(self):
        return not self.pieces and len(self.sections) == 1

    def draw(self, surface):
        for obj in self.objs:
            obj.draw(surface)
        # for piece in self.pieces:
        #     if piece is not self.grabbed:
        #         piece.draw(surface)
        # for section in self.sections:
        #     if section is not self.grabbed:
        #         section.draw(surface)
        # if self.grabbed is not None:
        #     self.grabbed.draw(surface)

    def update(self, mouse_pos, dt):
        if self.grabbed:
            self.grabbed.adjust_pos(mouse_pos)
