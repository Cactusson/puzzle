import pygame as pg

from .. import prepare
from .label import Label


class ToggleButton(pg.sprite.Sprite):
    """
    ToggleButton is a helper class used in ChoiceBox.
    """
    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image_off, self.image_on, self.image_hover = self.make_images()
        self.image = self.image_off
        self.rect = self.image.get_rect()
        self.active = False

    def make_images(self):
        width = 5
        gap = 5
        label = Label(20, self.name, font_name='Quicksand-Regular',
                      topleft=(width + gap, width + gap))
        image_on = prepare.transparent_surface(
            label.rect.width + 2 * (width + gap),
            label.rect.height + 2 * (width + gap))
        label.draw(image_on)
        rect = (0, 0, label.rect.width + 2 * (width + gap),
                label.rect.height + 2 * (width + gap))
        pg.draw.rect(image_on, prepare.BUTTON_HOVER_FILL_COLOR, rect, width)

        image_off = prepare.transparent_surface(
            label.rect.width + 2 * (width + gap),
            label.rect.height + 2 * (width + gap))
        label.draw(image_off)

        image_hover = prepare.transparent_surface(
            label.rect.width + 2 * (width + gap),
            label.rect.height + 2 * (width + gap))
        label.draw(image_hover)
        rect = (0, 0, label.rect.width + 2 * (width + gap),
                label.rect.height + 2 * (width + gap))
        pg.draw.rect(image_hover, pg.Color('white'), rect, width)

        return image_off, image_on, image_hover

    def activate(self):
        self.active = True
        self.image = self.image_on

    def deactivate(self):
        self.active = False
        self.image = self.image_off

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse_pos):
        if not self.active:
            hover = self.rect.collidepoint(mouse_pos)
            if hover:
                self.image = self.image_hover
            else:
                self.image = self.image_off
