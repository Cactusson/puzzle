import pygame as pg
import random

from .animation import Animation
from .task import Task


class HardcoreObj:
    """
    Class describes hardcore features like turning around and moving by itself.
    Both PieceHardcore and SectionHardcore inherit from it.
    """
    def __init__(self, turn_time):
        self.tasks = pg.sprite.Group()
        self.animations = pg.sprite.Group()
        self.turn_task = None
        self.move_task = None
        self.turn_time_min = turn_time[0]
        self.turn_time_max = turn_time[1]
        self.prepare_turn()
        self.prepare_to_move()

    def do_turn(self):
        if not hasattr(self, 'pieces'):
            if self.show_image == self.image:
                self.show_image = self.image2
            else:
                self.show_image = self.image
        else:
            for piece in self.pieces:
                if piece.show_image == piece.image:
                    piece.show_image = piece.image2
                else:
                    piece.show_image = piece.image
        self.prepare_turn()

    def prepare_turn(self):
        self.turn_task = Task(self.do_turn, random.randint(
            self.turn_time_min, self.turn_time_max))
        self.tasks.add(self.turn_task)

    def auto_turn(self, num):
        if not hasattr(self, 'pieces'):
            if num == 1 and self.show_image == self.image2:
                self.show_image = self.image
            elif num == 2 and self.show_image == self.image:
                self.show_image = self.image2
        else:
            for piece in self.pieces:
                piece.auto_turn(num)

    def stop_turning(self):
        if self.turn_task:
            self.turn_task.kill()

    def start_moving(self):
        pass

    def prepare_to_move(self):
        self.move_task = Task(self.start_moving, random.randint(
            self.turn_time_min * 2, self.turn_time_max * 2))
        self.tasks.add(self.move_task)

    def stop_moving(self):
        self.animations.empty()

    def update(self, dt):
        self.tasks.update(dt * 1000)
        self.animations.update(dt * 1000)
