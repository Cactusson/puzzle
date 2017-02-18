import pygame as pg

from .. import prepare, tools
from ..components.animation import Animation
from ..components.button_group import ButtonGroup
from ..components.calc import Calc
from ..components.label import Label


class Pause(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.animations = pg.sprite.Group()
        self.appear_time = 650

    def start(self):
        self.cover = pg.Surface(prepare.SCREEN_RECT.size).convert()
        self.calc = Calc(0, 255, self.appear_time, self.cover)

        self.main_block = pg.sprite.Sprite()
        self.main_block.rect = pg.rect.Rect(0, 0, 400, 500)
        self.main_block.image = pg.Surface(self.main_block.rect.size)
        self.main_block.rect.center = prepare.SCREEN_RECT.center
        self.title = Label(40, 'PAUSE', font_name='SourceCodePro-Bold',
                           center=(self.main_block.rect.width // 2, 75))
        rect = pg.rect.Rect(0, 0, 300, 250)
        rect.center = self.main_block.rect.width // 2, 300
        self.button_group = ButtonGroup(rect, ('RESUME', 'RESTART', 'QUIT'),
                                        self.button_call)

        animation = Animation(
            x=self.main_block.rect.x, y=self.main_block.rect.y,
            duration=self.appear_time, round_values=True,
            transition='out_cubic')
        self.main_block.rect.bottom = 0
        self.finish_pos = self.main_block.rect.topleft
        animation.callback = self.activate_buttons
        animation.start(self.main_block.rect)
        self.animations.add(animation)

        self.buttons_active = False

    def finish(self):
        self.buttons_active = False
        self.calc = Calc(255, 0, self.appear_time, self.cover)
        animation = Animation(
            x=self.finish_pos[0], y=self.finish_pos[1],
            duration=self.appear_time, round_values=True,
            transition='in_cubic')
        animation.callback = self.back_to_game
        animation.start(self.main_block.rect)
        self.animations.add(animation)

    def activate_buttons(self):
        self.buttons_active = True

    def back_to_game(self):
        if 'restart' in self.persist:
            self.persist['restart'] = 'DONE'
        self.next = 'GAME'
        self.done = True

    def button_call(self, button_name):
        if button_name == 'RESUME':
            self.finish()
        elif button_name == 'RESTART':
            self.persist['restart'] = 'INIT'
            self.next = 'GAME'
            self.done = True
        elif button_name == 'QUIT':
            self.next = 'MENU'
            self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if 'restart_screen' in self.persist:
            self.screen = self.persist['restart_screen']
            del self.persist['restart_screen']
            self.finish()
        else:
            self.screen = self.persist['screen']
            del self.persist['screen']
            self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.buttons_active:
                    self.finish()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.buttons_active:
                    self.button_group.click()

    def draw(self, surface):
        surface.blit(self.screen, (0, 0))
        surface.blit(self.cover, (0, 0))

        self.main_block.image.fill(prepare.BLOCK_COLOR)
        self.title.draw(self.main_block.image)
        self.button_group.draw(self.main_block.image)
        surface.blit(self.main_block.image, self.main_block.rect)

    def update(self, surface, dt):
        self.animations.update(dt * 1000)
        self.calc.update(dt * 1000)
        self.cover.set_alpha(self.calc.current)
        if self.buttons_active:
            mouse_pos = pg.mouse.get_pos()
            mouse_pos = (mouse_pos[0] - self.main_block.rect.x,
                         mouse_pos[1] - self.main_block.rect.y)
            self.button_group.update(mouse_pos)

        self.draw(surface)
