import pygame as pg

from .. import prepare, tools
from ..components.button_group import ButtonGroup
from ..components.label import Label


class Menu(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(60, 'PUZZLE', font_name='KaushanScript-Regular',
                           center=(prepare.SCREEN_RECT.centerx, 85))
        rect = pg.rect.Rect(0, 0, 400, 220)
        rect.center = (
            prepare.SCREEN_RECT.centerx,
            prepare.SCREEN_RECT.centery + self.title.rect.bottom // 2)
        self.button_group = ButtonGroup(rect, ('PLAY', 'HIGH SCORE', 'QUIT'),
                                        self.button_call)
        width = 50
        self.block_rect = rect.inflate(width * 2, width * 2)

    def button_call(self, button_name):
        if button_name == 'PLAY':
            self.change_state('CHOOSE')
        elif button_name == 'HIGH SCORE':
            self.change_state('HIGH_SCORE')
        elif button_name == 'QUIT':
            self.quit = True

    def change_state(self, new_state):
        self.button_group.unhover()
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous in ['CHOOSE', 'HIGH_SCORE']:
            prepare.make_transition(self, 'MENU')
        elif self.previous == 'PAUSE':
            prepare.make_transition(self, 'MENU', True)

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
        surface.fill(prepare.BG_COLOR)
        surface.fill(prepare.BLOCK_COLOR, self.block_rect)
        self.title.draw(surface)
        self.button_group.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.button_group.update(mouse_pos)
        self.draw(surface)
