import pygame as pg

from .button import Button


class ButtonPic(Button):
    """
    Same as Button but with pic instead of text.
    """
    def __init__(self, idle_image, hover_image, name, call,
                 topleft=None, center=None):
        pg.sprite.Sprite.__init__(self)
        self.call = call
        self.hover = False
        self.idle_image = idle_image
        self.hover_image = hover_image
        self.image = self.idle_image
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            self.rect = self.image.get_rect()
