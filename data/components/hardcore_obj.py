import pygame as pg
import random

from .. import prepare
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
        self.speed = 0.4
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
        distance, direction = self.get_move_data()
        self.move(distance, direction, self.prepare_to_move)

    def move(self, distance, direction, callback=None):
        if not hasattr(self, 'pieces'):
            if direction == 'x':
                x = self.rect.x + distance
                y = self.rect.y
            else:
                x = self.rect.x
                y = self.rect.y + distance
            duration = abs(distance) // self.speed
            animation = Animation(x=x, y=y, duration=duration,
                                  round_values=True)
            if callback:
                animation.callback = callback
            animation.start(self.rect)
            self.animations.add(animation)
        else:
            set_callback = True
            for piece in self.pieces:
                if set_callback:
                    piece.move(distance, direction, self.prepare_to_move)
                    set_callback = False
                else:
                    piece.move(distance, direction)

    def get_move_data(self):
        min_dist = 100
        borders = [prepare.SCREEN_RECT.left, prepare.SCREEN_RECT.right,
                   prepare.SCREEN_RECT.top, prepare.SCREEN_RECT.bottom]
        if not hasattr(self, 'pieces'):
            sides = [self.rect.left, self.rect.right,
                     self.rect.top, self.rect.bottom]
        else:
            sides = [min([piece.rect.left for piece in self.pieces]),
                     max([piece.rect.right for piece in self.pieces]),
                     min([piece.rect.top for piece in self.pieces]),
                     max([piece.rect.bottom for piece in self.pieces])]

        distances = [border-side for side, border in zip(sides, borders)]
        possible = [num for num, dist in enumerate(distances)
                    if abs(dist) >= min_dist]
        num = random.choice(possible)
        direction = 'x' if num == 0 or num == 1 else 'y'
        distance = random.randint(min_dist, abs(distances[num]))
        if distances[num] < 0:
            distance *= -1
        return distance, direction

    def prepare_to_move(self):
        self.move_task = Task(self.start_moving, random.randint(
            self.turn_time_min, self.turn_time_max))
        self.tasks.add(self.move_task)

    def stop_moving(self):
        self.animations.empty()

    def click(self):
        self.tasks.empty()
        self.animations.empty()

    def unclick(self):
        self.prepare_turn()
        self.prepare_to_move()

    def update(self, dt):
        self.tasks.update(dt * 1000)
        if not hasattr(self, 'pieces'):
            self.animations.update(dt * 1000)
        else:
            for piece in self.pieces:
                piece.animations.update(dt * 1000)
