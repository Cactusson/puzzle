import pygame as pg
import random

from .. import prepare
from .task import Task


class Darkness(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.tasks = pg.sprite.Group()
        self.max_vision = (int(prepare.SCREEN_RECT.width * 2.5),
                           int(prepare.SCREEN_RECT.width * 2.5))
        self.change_rate = (20, 20)
        # states = WAIT_TO_SHRINK, SHRINK, WAIT_TO_GROW, GROW, STOP
        self.active = True
        self.start()

    def start(self):
        min_radius = random.randint(300, 550)
        alpha = random.randint(235, 255)
        self.min_vision = (min_radius, min_radius)
        self.vision_rect = pg.rect.Rect((0, 0), self.max_vision)
        self.empty_cover = pg.Surface(prepare.SCREEN_SIZE).convert_alpha()
        self.empty_cover.fill((0, 0, 0, alpha))
        self.time_before_shrink = random.randint(4000, 8000)
        self.time_before_grow = random.randint(3000, 6000)
        self.prepare_to_shrink()

    def make_image(self, center):
        cover = self.empty_cover.copy()
        self.vision_rect.center = center
        pg.draw.circle(cover, (0, 0, 0, 0), self.vision_rect.center,
                       self.vision_rect.width // 2)
        return cover

    def prepare_to_shrink(self):
        self.state = 'WAIT_TO_SHRINK'
        task = Task(self.start_shrinking, self.time_before_shrink)
        self.tasks.add(task)

    def start_shrinking(self):
        self.state = 'SHRINK'
        self.tasks.empty()
        task = Task(self.shrink, 5, -1)
        self.tasks.add(task)

    def shrink(self):
        self.vision_rect.width -= self.change_rate[0]
        self.vision_rect.height -= self.change_rate[1]
        if (self.vision_rect.width <= self.min_vision[0] or
                self.vision_rect.height <= self.min_vision[1]):
            self.vision_rect.size = self.min_vision
            self.stop_shrinking()

    def stop_shrinking(self):
        self.tasks.empty()
        self.prepare_to_grow()

    def prepare_to_grow(self):
        self.state = 'WAIT_TO_GROW'
        task = Task(self.start_growing, self.time_before_grow)
        self.tasks.add(task)

    def start_growing(self):
        self.state = 'GROW'
        self.tasks.empty()
        task = Task(self.grow, 5, -1)
        self.tasks.add(task)

    def grow(self):
        self.vision_rect.width += self.change_rate[0]
        self.vision_rect.height += self.change_rate[1]
        if (self.vision_rect.width >= self.max_vision[0] or
                self.vision_rect.height >= self.max_vision[1]):
            self.vision_rect.size = self.max_vision
            self.stop_growing()

    def stop_growing(self):
        self.tasks.empty()
        if self.active:
            self.start()
        else:
            self.state = 'STOP'

    def stop(self):
        self.active = False
        if self.state == 'WAIT_TO_SHRINK':
            self.tasks.empty()
            self.state = 'STOP'
        elif self.state == 'SHRINK':
            self.stop_shrinking()
            self.change_rate = self.change_rate[0] * 2, self.change_rate[1] * 2
            self.start_growing()
        elif self.state == 'WAIT_TO_GROW':
            self.change_rate = self.change_rate[0] * 2, self.change_rate[1] * 2
            self.start_growing()

    def draw(self, surface):
        if self.state in ['SHRINK', 'GROW', 'WAIT_TO_GROW']:
            surface.blit(self.image, (0, 0))

    def update(self, center, dt):
        self.tasks.update(dt * 1000)
        if self.state in ['SHRINK', 'GROW', 'WAIT_TO_GROW']:
            self.image = self.make_image(center)
