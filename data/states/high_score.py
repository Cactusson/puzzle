import pickle
import pygame as pg

from .. import prepare, tools

from ..components.button_group import ButtonGroup
from ..components.label import Label
from ..components.picture_button import PictureButton
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

        self.pic_buttons = pg.sprite.Group()
        for indx, row in enumerate(results):
            topleft = (20, indx * 100 + 7 + 50)
            picture = prepare.GFX['pictures']['pic0{}'.format(indx)]
            pic_button = PictureButton(topleft, picture, self.picture_click)
            self.pic_buttons.add(pic_button)

            # pic_button.draw(image_res)
            easy, normal, hard = row
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

    def picture_click(self, pic):
        self.persist['pic'] = pic.copy()
        self.persist['screen'] = pg.display.get_surface().copy()
        self.show_rect_top = self.show_rect.top
        self.slider_top = self.slide_bar.slider.rect.top
        self.change_state('SHOW_PIC')

    def start(self):
        self.simple_image = self.prepare_image()
        self.update_image()
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

    def adjust_moues_pos(self, mouse_pos):
        """
        Adjust mouse_pos according to self.show_rect.
        """
        pos = (mouse_pos[0] - self.image_rect[0] + self.show_rect[0],
               mouse_pos[1] - self.image_rect[1] + self.show_rect[1])
        return pos

    def button_call(self, button_name):
        if button_name == 'BACK':
            self.change_state('MENU')

    def update_image(self):
        self.image = self.simple_image.copy()
        for pic_button in self.pic_buttons:
            pic_button.draw(self.image)

    def change_state(self, new_state):
        self.button_group.unhover()
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        self.start()
        if self.previous == 'MENU':
            prepare.make_transition(self, 'HIGH_SCORE')
        elif self.previous == 'SHOW_PIC':
            self.show_rect.top = self.show_rect_top
            self.slide_bar.slider.rect.top = self.slider_top

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.change_state('MENU')
            elif event.key == pg.K_UP:
                self.move_show_rect(-130)
            elif event.key == pg.K_DOWN:
                self.move_show_rect(130)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.button_group.click()
                self.slide_bar.click(event.pos)
                self.update_show_rect()
                for pic_button in self.pic_buttons:
                    pic_button.click()
        elif event.type == pg.MOUSEBUTTONUP:
            self.slide_bar.unclick()

    def draw(self, surface):
        surface.fill(prepare.BG_COLOR)
        surface.fill(prepare.BLOCK_COLOR, self.buttons_block)
        self.title.draw(surface)
        self.button_group.draw(surface)
        self.update_image()
        surface.blit(self.image, self.image_rect, self.show_rect)
        self.slide_bar.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        if self.image_rect.collidepoint(mouse_pos):
            adjusted_mouse_pos = self.adjust_moues_pos(mouse_pos)
            for pic_button in self.pic_buttons:
                pic_button.update(adjusted_mouse_pos)
        self.button_group.update(mouse_pos)
        self.slide_bar.update(mouse_pos)
        if self.slide_bar.slider.clicked:
            self.update_show_rect()
        self.draw(surface)
