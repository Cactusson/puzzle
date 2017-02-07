import pickle
import pygame as pg

from .. import prepare, tools

from ..components.button_group import ButtonGroup
from ..components.label import Label
from ..components.slide_bar import SlideBar


class HighScore(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.title = Label(50, 'HIGH SCORE', font_name='SourceCodePro-Bold',
                           center=(prepare.SCREEN_RECT.centerx, 60))
        rect = pg.rect.Rect(0, 0, 150, 50)
        rect.center = (prepare.SCREEN_RECT.centerx, 565)
        self.button_group = ButtonGroup(rect, ('BACK',), self.button_call)
        self.buttons_block = rect.inflate(25, 25).move(0, -8)

    def prepare_image(self):
        # this function is so messy, omg

        image = pg.Surface((600, 1050)).convert()

        image_title = pg.Surface((600, 50)).convert()
        image_title.fill(prepare.BLOCK_COLOR)
        label_easy = Label(
            23, 'EASY', font_name='Quicksand-Bold',
            center=(275, 25))
        label_easy.draw(image_title)

        label_normal = Label(
            23, 'NORMAL', font_name='Quicksand-Bold',
            center=(400, 25))
        label_normal.draw(image_title)

        label_hard = Label(
            23, 'HARD', font_name='Quicksand-Bold',
            center=(525, 25))
        label_hard.draw(image_title)

        image_res = pg.Surface((600, 1000)).convert()
        image_res.fill(prepare.BLOCK_COLOR)
        try:
            results_file = open('results', 'rb')
            results = pickle.load(results_file)
        except:
            # results coded this way:
            # for each pic [0, 0, 0] (for EASY, NORMAL, HARD)
            # hardcore mode doesn't use results
            results = [[0, 0, 0] for _ in
                       range(prepare.PICS_AMOUNT)]
        mini_height = 76
        gap = (100 - mini_height) // 2
        for indx, row in enumerate(results):
            easy, normal, hard = row
            mini = prepare.GFX['mini']['mini0{}'.format(indx)]
            topleft = (25, indx * 100 + gap)
            image_res.blit(mini, topleft)

            label_easy = Label(
                20, tools.time_to_text(easy), font_name='Quicksand-Regular',
                center=(275, indx * 100 + 50))
            label_easy.draw(image_res)

            label_normal = Label(
                20, tools.time_to_text(normal), font_name='Quicksand-Regular',
                center=(400, indx * 100 + 50))
            label_normal.draw(image_res)

            label_hard = Label(
                20, tools.time_to_text(hard), font_name='Quicksand-Regular',
                center=(525, indx * 100 + 50))
            label_hard.draw(image_res)

        image.blit(image_title, (0, 0))
        image.blit(image_res, (0, 50))
        return image

    def start(self):
        self.image = self.prepare_image()
        self.image_rect = pg.rect.Rect(0, 0, 600, 400)
        self.image_rect.topleft = (200, 115)
        self.show_rect = pg.rect.Rect(0, 0, 600, 400)

        rect = pg.rect.Rect(self.image_rect.right + 1, self.image_rect.top,
                            50, self.image_rect.height)
        rate = rect.height / self.image.get_height()
        self.slide_bar = SlideBar(rect, rate)

    def move_show_rect(self, step):
        if self.show_rect.top + step < 0:
            step = -self.show_rect.top
        elif self.show_rect.bottom + step > self.image.get_height():
            step = self.image.get_height() - self.show_rect.bottom
        self.show_rect.top += step
        self.slide_bar.move_step(step)

    def update_show_rect(self):
        self.show_rect.top = self.slide_bar.get_top()

    def button_call(self, button_name):
        if button_name == 'BACK':
            self.change_state('MENU')

    def change_state(self, new_state):
        self.button_group.unhover()
        self.next = new_state
        self.done = True

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
            elif event.key == pg.K_UP:
                self.move_show_rect(-130)
            elif event.key == pg.K_DOWN:
                self.move_show_rect(130)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_group.click()
                self.slide_bar.click(event.pos)
                self.update_show_rect()
        elif event.type == pg.MOUSEBUTTONUP:
            self.slide_bar.unclick()

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        surface.fill(prepare.BLOCK_COLOR, self.buttons_block)
        self.title.draw(surface)
        self.button_group.draw(surface)
        surface.blit(self.image, self.image_rect, self.show_rect)
        self.slide_bar.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.button_group.update(mouse_pos)
        self.slide_bar.update(mouse_pos)
        if self.slide_bar.slider.clicked:
            self.update_show_rect()
        self.draw(surface)
