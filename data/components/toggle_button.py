import pygame as pg

from .label import Label


class ToggleButton(pg.sprite.Sprite):
    """
    ToggleButton is a helper class used in ChoiceBox.
    """
    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image_off, self.image_on = self.make_images()
        self.image = self.image_off
        self.rect = self.image.get_rect()
        self.active = False

    def make_images(self):
        label = Label(20, self.name, font_name='OpenSans-Regular',
                      topleft=(0, 0))
        image_on = label.image.copy()
        label = Label(20, self.name, font_name='OpenSans-Bold',
                      topleft=(0, 0), bg=pg.Color('purple'))
        image_off = label.image.copy()
        return image_on, image_off

    def activate(self):
        self.active = True
        self.image = self.image_on

    def deactivate(self):
        self.active = False
        self.image = self.image_off

    def draw(self, surface):
        surface.blit(self.image, self.rect)
