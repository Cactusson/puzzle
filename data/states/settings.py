import pygame as pg

from .. import prepare, tools

from ..components import colors
from ..components import settings
from ..components.button_group import ButtonGroup
from ..components.choice_box import ChoiceBox
from ..components.label import Label


class Settings(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(50, 'SETTINGS', font_name='SourceCodePro-Bold')

    def start_from_menu(self):
        self.bg_color = colors.BG_COLOR

        self.title.rect.center = prepare.SCREEN_RECT.centerx, 60

        self.block_rect = pg.rect.Rect(0, 0, 400, 300)
        self.block_rect.center = (
            prepare.SCREEN_RECT.centerx,
            prepare.SCREEN_RECT.centery + self.title.rect.bottom // 2)

        self.create_choice_boxes()
        self.create_button_group()

    def start_from_pause(self):
        self.bg_color = pg.Color('black')

        self.title.rect.center = prepare.SCREEN_RECT.centerx, 150

        self.block_rect = pg.rect.Rect(0, 0, 400, 500)
        self.block_rect.center = prepare.SCREEN_RECT.center

        self.create_choice_boxes()
        self.create_button_group()

    def create_choice_boxes(self):
        rect = pg.rect.Rect(400, 240, 245, 50)
        music_on = 'ON' if settings.music_on else 'OFF'
        self.music_box = ChoiceBox(
            rect, 'MUSIC:', ['ON', 'OFF'], music_on, inline=True)

        rect = pg.rect.Rect(400, 320, 245, 50)
        sound_on = 'ON' if settings.sound_on else 'OFF'
        self.sound_box = ChoiceBox(
            rect, 'SOUND:', ['ON', 'OFF'], sound_on, inline=True)

    def create_button_group(self):
        rect = pg.rect.Rect(0, 0, 150, 50)
        rect.center = (prepare.SCREEN_RECT.centerx, 450)
        self.button_group = ButtonGroup(rect, ('BACK',), self.button_call)

    def button_call(self, button_name):
        if button_name == 'BACK':
            self.button_group.unhover()
            self.next = self.next_state
            self.done = True

    def click(self):
        if self.music_box.click(pg.mouse.get_pos()):
            tools.music_station.toggle_music()
        if self.sound_box.click(pg.mouse.get_pos()):
            sound = self.sound_box.get_active()
            settings.sound_on = True if sound == 'ON' else False
        self.button_group.click()

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'MENU':
            self.next_state = 'MENU'
            self.start_from_menu()
            prepare.make_transition(self, 'SETTINGS')
        elif self.previous == 'PAUSE':
            self.next_state = 'PAUSE'
            self.start_from_pause()

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
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_group.click()

    def draw(self, surface):
        surface.fill(self.bg_color)
        surface.fill(colors.BLOCK_COLOR, self.block_rect)
        self.title.draw(surface)
        self.music_box.draw(surface)
        self.sound_box.draw(surface)
        self.button_group.draw(surface)

    def update(self, surface, dt):
        self.button_group.update(pg.mouse.get_pos())
        self.music_box.update(pg.mouse.get_pos())
        self.sound_box.update(pg.mouse.get_pos())
        self.draw(surface)
