import pygame as pg

from .. import prepare, tools
from ..components.button_pic import ButtonPic


class ShowPic(tools._State):
    def __init__(self):
        tools._State.__init__(self)

    def start(self):
        self.pic_pos = (
            (prepare.SCREEN_RECT.width - self.pic.get_width()) // 2,
            (prepare.SCREEN_RECT.height - self.pic.get_height()) // 2)
        button_center = self.pic_pos[0] + self.pic.get_width(), self.pic_pos[1]
        width = 70
        idle_image = prepare.transparent_surface(width, width)
        pg.draw.circle(idle_image, pg.Color('black'),
                       (width // 2, width // 2), width // 2)
        idle_image.blit(prepare.GFX['gui']['cross'],
                        ((width - 50) // 2, (width - 50) // 2))

        hover_image = prepare.transparent_surface(width, width)
        pg.draw.circle(hover_image, pg.Color('red'),
                       (width // 2, width // 2), width // 2)
        hover_image.blit(prepare.GFX['gui']['cross'],
                         ((width - 50) // 2, (width - 50) // 2))

        self.button = ButtonPic(idle_image, hover_image, 'CLOSE',
                                self.finish, center=button_center)

    def finish(self):
        self.next = 'HIGH_SCORE'
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'HIGH_SCORE':
            self.screen = self.persist['screen']
            self.pic = self.persist['pic']
            del self.persist['screen']
            del self.persist['pic']
            self.start()
            prepare.make_transition(self, 'SHOW_PIC', True, 500)

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.button.click()

    def draw(self, surface):
        surface.blit(self.screen, (0, 0))
        surface.blit(self.pic, self.pic_pos)
        self.button.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.button.update(mouse_pos)
        self.draw(surface)
