import pygame as pg

from .. import prepare
from .label import Label
from .task import Task


class Timer(pg.sprite.Sprite):
    def __init__(self, topleft):
        pg.sprite.Sprite.__init__(self)
        self.empty_image = self.make_empty_image()
        self.rect = self.empty_image.get_rect(topleft=topleft)
        self.on = False
        self.current_time = 0
        self.tasks = pg.sprite.Group()
        self.update_image()

    def make_empty_image(self):
        image = pg.Surface((184, 64)).convert()
        # image.fill(pg.Color('lightgreen'))
        image.set_alpha(0)
        image = image.convert_alpha()
        image.blit(prepare.GFX['gui']['stopwatch'], (0, 0))
        return image

    def start(self):
        self.on = True
        task = Task(self.next_second, 1000, -1)
        self.tasks.add(task)

    def stop(self):
        self.on = False

    def next_second(self):
        self.current_time += 1
        self.update_image()

    def time_to_text(self):
        minutes = str(self.current_time // 60)
        if len(minutes) == 1:
            minutes = '0' + minutes
        seconds = str(self.current_time % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        return '{}:{}'.format(minutes, seconds)

    def update_image(self):
        self.image = self.empty_image.copy()
        text = self.time_to_text()
        label = Label(40, text, font_name='OpenSans-Bold', topleft=(72, 5))
        label.draw(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, dt):
        if self.on:
            self.tasks.update(dt * 1000)
