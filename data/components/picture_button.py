import pygame as pg

from .. import prepare


class PictureButton(pg.sprite.Sprite):
    """
    Used in HIGH_SCORE state. It's a picture that works like a button.
    On click it calls provided callback function giving it the pic as an arg.
    """
    def __init__(self, topleft, pic, callback):
        pg.sprite.Sprite.__init__(self)
        self.big_pic = pic
        self.callback = callback
        mini_width = 150
        mini_height = 76
        self.idle_image, self.hover_image = self.make_images(
            mini_width, mini_height)
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=topleft)
        self.hovered = False

    def make_images(self, width, height):
        gap = 5
        mini_pic = pg.transform.scale(self.big_pic, (width, height)).convert()
        idle_image = prepare.transparent_surface(
            width + gap * 2, height + gap * 2)
        idle_image.blit(mini_pic, (gap, gap))
        hover_image = pg.Surface((width + gap * 2, height + gap * 2)).convert()
        hover_image.fill(prepare.BUTTON_HOVER_TEXT_COLOR)
        hover_image.blit(mini_pic, (gap, gap))
        return idle_image, hover_image

    def hover(self):
        if self.hovered:
            return
        self.hovered = True
        self.image = self.hover_image

    def unhover(self):
        if not self.hovered:
            return
        self.hovered = False
        self.image = self.idle_image

    def click(self):
        if self.hovered:
            self.callback(self.big_pic)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hover()
        else:
            self.unhover()
