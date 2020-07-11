import pygame as pg

from . import colors


class Slider(pg.sprite.Sprite):
    def __init__(self, rect, top, bottom):
        self.rect = rect
        self.image = self.make_image()
        self.top = top
        self.bottom = bottom
        self.clicked = False
        self.mouse_offset = 0
        self.hover = False

    def make_image(self):
        image = pg.Surface(self.rect.size).convert()
        image.fill(colors.BUTTON_HOVER_FILL_COLOR)
        return image

    def get_top(self):
        return self.rect.top - self.top

    def click(self, mouse_pos):
        """
        Checks for hover in SlideBar.
        """
        self.clicked = True
        self.mouse_offset = self.rect.center[1] - mouse_pos[1]

    def unclick(self):
        self.clicked = False

    def update_position(self, mouse_pos):
        self.rect.centery = mouse_pos[1] + self.mouse_offset
        self.adjust_pos()

    def move_to(self, mouse_pos):
        self.rect.centery = mouse_pos[1]
        self.adjust_pos()

    def adjust_pos(self):
        # useless?
        if self.rect.top < self.top:
            self.rect.top = self.top
        if self.rect.bottom > self.bottom:
            self.rect.bottom = self.bottom

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        if self.clicked:
            self.update_position(mouse_pos)
