import os
import pygame as pg
import random

from .. import prepare, tools

from ..components.label import Label


def uppath(_path, n):
    return os.sep.join(_path.split(os.sep)[:-n])


class Load(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.pics_cache = {}
        self.label = Label(50, 'LOADING', font_name='SourceCodePro-Bold',
                           center=(prepare.SCREEN_RECT.center))

    def start(self):
        self.load_stuff()
        self.next = 'GAME'
        self.done = True

    def load_stuff(self):
        pic_num, pic = self.load_picture()
        self.persist['pic_num'] = pic_num
        self.persist['pic'] = pic
        if self.hardcore:
            while True:
                pic_num2, pic2 = self.load_picture()
                if pic_num != pic_num2:
                    break
            self.persist['pic2'] = pic2

    def load_picture(self):
        pic_num = random.randint(0, prepare.PICS_AMOUNT - 1)
        if pic_num in self.pics_cache:
            pic = self.pics_cache[pic_num]
            return pic_num, pic

        num = str(pic_num)
        if len(num) == 1:
            num = '0' + num
        pics_path = os.path.join(uppath(__file__, 3), 'resources', 'graphics',
                                 'pictures')
        pic = pg.image.load(os.path.join(pics_path, 'pic{}.jpg'.format(num)))
        pic = pg.transform.scale(pic, (640, 480))
        self.pics_cache[pic_num] = pic
        return pic_num, pic

    def startup(self, persistant):
        self.persist = persistant
        self.hardcore = self.persist['hardcore']
        if self.previous == 'CHOOSE':
            prepare.make_transition(self, 'LOAD')
        elif self.previous == 'TRANSITION':
            self.start()

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        self.label.draw(surface)

    def update(self, surface, dt):
        pass
