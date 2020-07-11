import pygame as pg

from .. import prepare, tools

from ..components import colors
from ..components.button_group import ButtonGroup
from ..components.label import Label


class Menu(tools._State):
    def __init__(self):
        """
        Here we create only those things that we won't need to recreate again
        since this function will only run once.
        """
        tools._State.__init__(self)
        self.title = Label(60, 'PUZZLE', font_name='KaushanScript-Regular',
                           center=(prepare.SCREEN_RECT.centerx, 85))
        self.button_group_rect = pg.rect.Rect(0, 0, 400, 250)
        self.button_group_rect.center = (
            prepare.SCREEN_RECT.centerx,
            prepare.SCREEN_RECT.centery + self.title.rect.bottom // 2)
        self.block_rect = self.button_group_rect.inflate(100, 100)
        self.start()

    def start(self):
        """
        We create a new button group each time a possible color change occurs
        (meaning when we get to this state from GAME or PAUSE)
        """
        self.button_group = ButtonGroup(
            self.button_group_rect, ('PLAY', 'HIGH SCORE', 'SETTINGS', 'QUIT'),
            self.button_call)

    def button_call(self, button_name):
        if button_name == 'PLAY':
            self.change_state('CHOOSE')
        elif button_name == 'HIGH SCORE':
            self.change_state('HIGH_SCORE')
        elif button_name == 'SETTINGS':
            self.change_state('SETTINGS')
        elif button_name == 'QUIT':
            self.quit = True

    def change_state(self, new_state):
        self.button_group.unhover()
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous in ['CHOOSE', 'HIGH_SCORE', 'SETTINGS']:
            prepare.make_transition(self, 'MENU')
        elif self.previous in ['PAUSE', 'GAME']:
            colors.change_color_package()
            self.start()
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
        surface.fill(colors.BG_COLOR)
        surface.fill(colors.BLOCK_COLOR, self.block_rect)
        self.title.draw(surface)
        self.button_group.draw(surface)

    def update(self, surface, dt):
        self.button_group.update(pg.mouse.get_pos())
        self.draw(surface)
