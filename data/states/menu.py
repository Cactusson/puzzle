import pygame as pg

from .. import prepare, tools
from ..components.button_group import ButtonGroup
from ..components.label import Label


class Menu(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(30, 'PUZZLE', font_name='OpenSans-Bold',
                           center=(prepare.SCREEN_RECT.centerx, 200))

    def start(self):
        rect = pg.rect.Rect(0, 0, 500, 250)
        rect.center = prepare.SCREEN_RECT.centerx, 450
        self.button_group = ButtonGroup(rect, ('PLAY', 'HIGH SCORE', 'QUIT'),
                                        self.button_call)

    def button_call(self, button_name):
        if button_name == 'PLAY':
            self.next = 'CHOOSE'
            self.done = True
        elif button_name == 'HIGH SCORE':
            pass
        elif button_name == 'QUIT':
            self.quit = True

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_group.click()

    def draw(self, surface):
        surface.fill(pg.Color('lightblue'))
        self.title.draw(surface)
        self.button_group.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.button_group.update(mouse_pos)
        self.draw(surface)
