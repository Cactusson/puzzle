import pygame as pg

from .. import prepare, tools
from ..components.button_group import ButtonGroup
from ..components.choice_box import ChoiceBox
from ..components.label import Label


class Choose(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(50, 'CHOOSE YOUR DESTINY',
                           font_name='SourceCodePro-Bold',
                           center=(prepare.SCREEN_RECT.centerx, 65))
        rect1 = pg.rect.Rect(300, 165, 400, 100)
        self.difficulty_box = ChoiceBox(
            rect1, 'DIFFICULTY:', ['EASY', 'NORMAL', 'HARD'], default='NORMAL')
        rect2 = pg.rect.Rect(350, 290, 300, 100)
        self.hardcore_box = ChoiceBox(rect2, 'HARDCORE:', ['ON', 'OFF'],
                                      default='OFF')
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
        Tries to get info from difficulty_box and hardcore_box.
        On success proceed to LOAD state.
        On failure does nothing.
        """
        difficulty = self.difficulty_box.get_active()
        if difficulty is None:
            return
        hardcore = self.hardcore_box.get_active()
        if hardcore is None:
            return
        self.persist['difficulty'] = ['EASY', 'NORMAL', 'HARD'].index(
            difficulty)
        self.persist['hardcore'] = ['OFF', 'ON'].index(hardcore)
        self.change_state('LOAD')

    def change_state(self, new_state):
        self.button_group.unhover()
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'MENU':
            prepare.make_transition(self, 'CHOOSE')

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.difficulty_box.click(event.pos)
                self.hardcore_box.click(event.pos)
                self.button_group.click()

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        surface.fill(prepare.BLOCK_COLOR, self.toggle_block)
        surface.fill(prepare.BLOCK_COLOR, self.buttons_block)
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
