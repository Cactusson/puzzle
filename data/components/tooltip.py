import pygame as pg

from . import colors
from .label import ListLabel, MultilineLabel


class Tooltip:
    def __init__(self, rect, text):
        self.rect = rect
        self.image = pg.Surface((rect.width, rect.height)).convert()
        self.image.fill(colors.BUTTON_HOVER_FILL_COLOR)
        self.image.fill(colors.BLOCK_COLOR, (5, 5, self.rect.width - 10, self.rect.height - 10))
        if isinstance(text, str):
            label = MultilineLabel(text, 18, font_name='Quicksand-Regular', align='left')
        else:
            label = ListLabel(text, 18, 8, font_name='Quicksand-Regular')
        label.rect.topleft = (13, 11)
        label.draw(self.image)
        self.visible = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
