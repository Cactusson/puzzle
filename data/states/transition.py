import pygame as pg
import random

from .. import prepare, tools
from ..components.animation import Animation
from ..components.calc import Calc


class Transition(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.animations = pg.sprite.Group()
        rect = prepare.SCREEN_RECT
        self.positions = [((0, -rect.height), (0, rect.height)),
                          ((-rect.width, 0), (rect.width, 0)),
                          ((rect.width, 0), (-rect.width, 0)),
                          ((0, rect.height), (0, -rect.height))]

    def start(self):
        (next_x, next_y), (prev_x, prev_y) = random.choice(self.positions)

        self.previous_rect = self.previous_image.get_rect()
        self.next_rect = self.next_image.get_rect(
            topleft=(next_x, next_y))
        self.calcs = []

        animation = Animation(
            x=prev_x, y=prev_y,
            duration=prepare.TRANSITION_TIME, round_values=True)
        animation.callback = self.finish
        animation.start(self.previous_rect)
        self.animations.add(animation)

        animation = Animation(
            x=0, y=0,
            duration=prepare.TRANSITION_TIME, round_values=True)
        animation.start(self.next_rect)
        self.animations.add(animation)

    def start_alpha(self):
        self.previous_rect = self.previous_image.get_rect()
        self.next_rect = self.next_image.get_rect()
        self.next_image.set_alpha(0)
        previous_calc = Calc(255, 0, 1000, self.previous_image)
        next_calc = Calc(0, 255, 1000, self.next_image)
        next_calc.callback = self.finish
        self.calcs = [previous_calc, next_calc]

    def finish(self):
        self.animations.empty()
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        self.next = self.persist['next_state']
        self.next_image = self.persist['next_image']
        self.previous_image = pg.display.get_surface().copy()
        del self.persist['next_state']
        del self.persist['next_image']
        if 'alpha_transition' in self.persist:
            del self.persist['alpha_transition']
            self.start_alpha()
        else:
            self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        surface.blit(self.previous_image, self.previous_rect)
        surface.blit(self.next_image, self.next_rect)

    def update(self, surface, dt):
        self.animations.update(dt * 1000)
        for calc in self.calcs:
            calc.update(dt * 1000)
        self.draw(surface)
