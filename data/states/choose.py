import pygame as pg

from .. import prepare, tools
from ..components.button import Button
from ..components.choice_box import ChoiceBox
from ..components.label import Label


class Choose(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(50, 'CHOOSE YOUR DESTINY',
                           font_name='OpenSans-Bold',
                           center=(prepare.SCREEN_RECT.centerx, 75))

    def start(self):
        rect = pg.rect.Rect(300, 175, 400, 125)
        self.difficulty_box = ChoiceBox(rect, 'DIFFICULTY:',
                                        ['EASY', 'NORMAL', 'HARD'])
        rect = pg.rect.Rect(350, 325, 300, 125)
        self.hardcore_box = ChoiceBox(rect, 'HARDCORE:', ['ON', 'OFF'],
                                      default='OFF')
        self.buttons = self.create_buttons()

    def create_buttons(self):
        play = Button(20, 'PLAY', self.button_call, font_name='OpenSans-Bold',
                      center=(prepare.SCREEN_RECT.centerx, 500))
        back = Button(20, 'BACK', self.button_call, font_name='OpenSans-Bold',
                      center=(prepare.SCREEN_RECT.centerx, 550))
        buttons = pg.sprite.Group(play, back)
        return buttons

    def button_call(self, button_name):
        if button_name == 'PLAY':
            self.start_game()
        elif button_name == 'BACK':
            self.back_to_menu()

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
        self.done = True
        self.next = 'LOAD'

    def back_to_menu(self):
        self.done = True
        self.next = 'MENU'

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
                self.difficulty_box.click(event.pos)
                self.hardcore_box.click(event.pos)
                for button in self.buttons:
                    button.click()

    def draw(self, surface):
        surface.fill(pg.Color('lightblue'))
        self.title.draw(surface)
        self.difficulty_box.draw(surface)
        self.hardcore_box.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.difficulty_box.update(mouse_pos)
        self.hardcore_box.update(mouse_pos)
        for button in self.buttons:
            button.update(mouse_pos)
        self.draw(surface)
