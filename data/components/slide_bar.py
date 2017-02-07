import pygame as pg

from .. import prepare
from .slider import Slider


class SlideBar:
    def __init__(self, rect, rate):
        self.rect = rect
        self.rate = rate
        height = int(self.rect.height * self.rate)
        slider_rect = pg.rect.Rect(
            self.rect.topleft, (self.rect.width, height))
        self.slider = Slider(slider_rect, self.rect.top, self.rect.bottom)

    def get_top(self):
        return self.slider.get_top() // self.rate

    def move_step(self, step):
        self.slider.rect.top += int(step * self.rate)
        self.slider.adjust_pos()

    def click(self, mouse_pos):
        if self.slider.hover:
            self.slider.click(mouse_pos)
        elif self.rect.collidepoint(mouse_pos):
            self.slider.move_to(mouse_pos)

    def unclick(self):
        self.slider.unclick()

    def draw(self, surface):
        surface.fill(prepare.BLOCK_COLOR, self.rect)
        self.slider.draw(surface)

    def update(self, mouse_pos):
        self.slider.update(mouse_pos)
