import pygame as pg

from .. import prepare, tools

from ..components import colors
from ..components.button_group import ButtonGroup
from ..components.choice_box import ChoiceBox
from ..components.label import Label
from ..components.tooltip import Tooltip


class Choose(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(50, 'CHOOSE YOUR DESTINY',
                           font_name='SourceCodePro-Bold',
                           center=(prepare.SCREEN_RECT.centerx, 65))

    def start(self):
        difficulty = ['EASY', 'NORMAL', 'HARD'][self.persist['difficulty']]
        hardcore = ['OFF', 'ON'][self.persist['hardcore']]

        rect = pg.rect.Rect(320, 165, 360, 100)
        text = ('Easy: 3x3 picture.', 'Normal: 4x4 picture.',
                'Hard: 5x5 picture.')
        tooltip = Tooltip(pg.rect.Rect(765, 140, 220, 110), text)
        self.difficulty_box = ChoiceBox(
            rect, 'DIFFICULTY:', ['EASY', 'NORMAL', 'HARD'], difficulty,
            tooltip=tooltip)
        rect = pg.rect.Rect(410, 290, 180, 100)
        text = "In hardcore mode pieces constantly flip and move around. Also lights sometimes go out."
        tooltip = Tooltip(pg.rect.Rect(765, 280, 220, 135), text)
        self.hardcore_box = ChoiceBox(
            rect, 'HARDCORE:', ['ON', 'OFF'], hardcore, tooltip=tooltip)
        rect = pg.rect.Rect(0, 0, 300, 100)
        rect.center = (prepare.SCREEN_RECT.centerx, 525)
        self.button_group = ButtonGroup(rect, ('PLAY', 'BACK'),
                                        self.button_call)

        self.toggle_block = (250, 135, 500, 285)
        self.buttons_block = rect.inflate(25, 25)

    def button_call(self, button_name):
        if button_name == 'PLAY':
            self.start_game()
        elif button_name == 'BACK':
            self.change_state('MENU')

    def start_game(self):
        """
        difficulty and hardcore choice boxes should always have an active
        value but we check here anyway, just to be sure. Then proceed to GAME.
        """
        difficulty = self.difficulty_box.get_active()
        hardcore = self.hardcore_box.get_active()
        if difficulty is None or hardcore is None:
            return
        self.change_state('GAME')

    def click(self):
        if self.difficulty_box.click(pg.mouse.get_pos()):
            difficulty = self.difficulty_box.get_active()
            self.persist['difficulty'] = ['EASY', 'NORMAL', 'HARD'].index(
                difficulty)
        if self.hardcore_box.click(pg.mouse.get_pos()):
            hardcore = self.hardcore_box.get_active()
            self.persist['hardcore'] = ['OFF', 'ON'].index(hardcore)
        self.button_group.click()

    def change_state(self, new_state):
        self.button_group.unhover()
        self.next = new_state
        self.done = True

    def startup(self, persist):
        self.persist = persist
        if self.previous == 'MENU':
            # be sure to start only once for every state, mb need to fix
            self.start()
            prepare.make_transition(self, 'CHOOSE')

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.change_state('MENU')
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click()

    def draw(self, surface):
        surface.fill(colors.BG_COLOR)
        surface.fill(colors.BLOCK_COLOR, self.toggle_block)
        surface.fill(colors.BLOCK_COLOR, self.buttons_block)
        self.title.draw(surface)
        self.difficulty_box.draw(surface)
        self.hardcore_box.draw(surface)
        self.button_group.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.difficulty_box.update(mouse_pos)
        self.hardcore_box.update(mouse_pos)
        self.button_group.update(mouse_pos)
        self.draw(surface)
