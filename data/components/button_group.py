import pygame as pg

from .. import prepare
from .button import Button


class ButtonGroup:
    def __init__(self, rect, names, callback):
        self.rect = rect
        self.callback = callback
        self.font_name = 'Quicksand-Bold'
        self.font_size = 23
        self.buttons = self.make_buttons(names)

    def make_buttons(self, names):
        buttons = pg.sprite.Group()
        width, height = self.get_button_size(names)
        gap = (self.rect.height - len(names) * height) // (len(names) - 1)
        for indx, name in enumerate(names):
            center = (self.rect.centerx,
                      self.rect.top + (height + gap) * indx + height // 2)
            button = Button(self.font_size, name, self.callback,
                            font_name=self.font_name, center=center,
                            width=width, height=height)
            buttons.add(button)
        return buttons

    def get_button_size(self, names):
        width = 0
        height = 0
        for name in names:
            button = Button(self.font_size, name, None,
                            font_name=self.font_name)
            if button.rect.width > width:
                width = button.rect.width
            if button.rect.height > height:
                height = button.rect.height
        if width == 0:
            width = None
        else:
            width *= 1.6
        if height == 0:
            height = None
        else:
            height *= 1.3
        return width, height

    def click(self):
        for button in self.buttons:
            button.click()

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)

    def update(self, mouse_pos):
        for button in self.buttons:
            button.update(mouse_pos)
