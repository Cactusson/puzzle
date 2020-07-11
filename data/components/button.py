import pygame as pg

from .. import prepare

from . import colors
from . import settings


class Button(pg.sprite.Sprite):
    """
    Button is some text on a bg. If you click on it, call (function)
    will be called.
    """
    def __init__(self, font_size, text, call, font_name=None, topleft=None,
                 center=None, width=None, height=None):
        pg.sprite.Sprite.__init__(self)
        self.name = text
        self.call = call
        self.hover = False
        if font_name is not None:
            self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        else:
            self.font = pg.font.Font(None, font_size)
        self.idle_image, self.hover_image = self.make_images(
            self.name, width, height)
        self.image = self.idle_image
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            self.rect = self.image.get_rect()

    def make_images(self, text, width, height):
        """
        Button changes its image depending if the player is hovering it or not.
        """
        idle_color = pg.Color('black')
        hover_color = colors.BUTTON_HOVER_TEXT_COLOR
        hover_fill = colors.BUTTON_HOVER_FILL_COLOR

        if width and height:
            idle_image = prepare.transparent_surface(width, height)
            idle_text = self.font.render(text, True, idle_color)
            idle_image.blit(idle_text, idle_text.get_rect(
                center=idle_image.get_rect().center))
            hover_image = pg.Surface((width, height)).convert()
            hover_image.fill(hover_fill)
            hover_text = self.font.render(text, True, hover_color, hover_fill)
            hover_image.blit(hover_text, hover_text.get_rect(
                center=hover_image.get_rect().center))
        else:
            idle_image = self.font.render(text, True, idle_color)
            hover_image = self.font.render(text, True, hover_color, hover_fill)
        return idle_image, hover_image

    def click(self):
        if self.hover:
            if hasattr(self, 'name') and self.name is not None:
                if settings.sound_on:
                    prepare.SFX['click'].play()
                self.call(self.name)
            else:
                self.call()

    def unhover(self):
        self.hover = False
        self.image = self.idle_image

    def update(self, mouse_pos):
        """
        Check if the button is hovered.
        """
        if hasattr(self, 'collide_rect'):
            rect = self.collide_rect
        else:
            rect = self.rect
        hover = rect.collidepoint(mouse_pos)
        if hover:
            self.image = self.hover_image
        else:
            self.image = self.idle_image
        self.hover = hover

    def draw(self, surface):
        surface.blit(self.image, self.rect)
