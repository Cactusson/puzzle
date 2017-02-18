import os
import pygame as pg

from .. import prepare, tools

from ..components.label import Label


def uppath(_path, n):
    return os.sep.join(_path.split(os.sep)[:-n])


class Load(tools._State):
    """
    The game starts with this state.
    It shows the word "LOADING" on the screen while loading all pics.
    After that it moves on to MENU state.
    """
    def __init__(self):
        tools._State.__init__(self)
        self.label = Label(50, 'LOADING', font_name='SourceCodePro-Bold',
                           center=(prepare.SCREEN_RECT.center))

    def start(self):
        self.draw(pg.display.get_surface())
        pg.display.update()
        self.load_stuff()
        self.next = 'MENU'
        self.done = True

    def load_stuff(self):
        pics_path = os.path.join(uppath(__file__, 3), 'resources', 'graphics',
                                 'pictures')
        prepare.GFX['pictures'] = tools.load_all_gfx(pics_path)

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        pass

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        self.label.draw(surface)

    def update(self, surface, dt):
        pass
