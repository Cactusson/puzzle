import pickle
import pygame as pg

from .. import prepare, tools

from ..components import colors
from ..components.button_group import ButtonGroup
from ..components.label import Label
from ..components.picture_button import PictureButton
from ..components.slide_bar import SlideBar


class HighScore(tools._State):
    def __init__(self):
        tools._State.__init__(self)
        self.labels = self.create_labels()

    def start(self):
        rect = pg.rect.Rect(0, 0, 150, 50)
        rect.center = (prepare.SCREEN_RECT.centerx, 565)
        self.button_group = ButtonGroup(rect, ('BACK',), self.button_call)
        self.buttons_block = rect.inflate(10, 10).move(0, -8)

        self.simple_image = self.prepare_image()
        self.update_image()
        self.image_rect = pg.rect.Rect(0, 0, 550, 385)
        self.image_rect.topleft = (225, 130)
        self.show_rect = pg.rect.Rect(0, 0, 550, 385)

        rect = pg.rect.Rect(self.image_rect.right + 1, self.image_rect.top,
                            25, self.image_rect.height)
        rate = rect.height / self.image.get_height()
        self.slide_bar = SlideBar(rect, rate)

    def create_labels(self):
        title = Label(
            50, 'HIGH SCORE', font_name='SourceCodePro-Bold',
            center=(prepare.SCREEN_RECT.centerx, 40)
        )
        easy = Label(21, 'EASY', font_name='Quicksand-Bold', center=(450, 108))
        normal = Label(21, 'NORMAL', font_name='Quicksand-Bold', center=(575, 108))
        hard = Label(21, 'HARD', font_name='Quicksand-Bold', center=(700, 108))
        return [title, easy, normal, hard]

    def prepare_image(self):
        image = pg.Surface((550, 1000)).convert()
        image.fill(colors.BLOCK_COLOR)

        try:
            results_file = open('results', 'rb')
            results = pickle.load(results_file)
        except FileNotFoundError:
            # results coded this way:
            # for each pic [0, 0, 0] (for EASY, NORMAL, HARD)
            # hardcore mode doesn't use results
            results = [[0, 0, 0] for _ in range(prepare.PICS_AMOUNT)]

        self.pic_buttons = pg.sprite.Group()
        for indx, row in enumerate(results):
            picture = prepare.GFX['pictures']['pic0{}'.format(indx)]
            pic_button = PictureButton(picture, self.picture_click)
            pic_button.rect.left = 35
            pic_button.rect.centery = indx * 100 + 50
            self.pic_buttons.add(pic_button)

            easy, normal, hard = row
            label_easy = Label(
                20, tools.time_to_text(easy), font_name='Quicksand-Regular',
                center=(225, indx * 100 + 50))
            label_easy.draw(image)

            label_normal = Label(
                20, tools.time_to_text(normal), font_name='Quicksand-Regular',
                center=(350, indx * 100 + 50))
            label_normal.draw(image)

            label_hard = Label(
                20, tools.time_to_text(hard), font_name='Quicksand-Regular',
                center=(475, indx * 100 + 50))
            label_hard.draw(image)

        return image

    def picture_click(self, pic):
        self.persist['pic'] = pic.copy()
        self.persist['screen'] = pg.display.get_surface().copy()
        self.change_state('SHOW_PIC')

    def move_show_rect(self, step):
        if self.show_rect.top + step < 0:
            step = -self.show_rect.top
        elif self.show_rect.bottom + step > self.image.get_height():
            step = self.image.get_height() - self.show_rect.bottom
        self.show_rect.top += step
        self.slide_bar.move_step(step)

    def update_show_rect(self):
        self.show_rect.top = self.slide_bar.get_top()

    def adjust_mouse_pos(self, mouse_pos):
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

    def update_picture_buttons(self):
        # makes sure that picture buttons are hovered/unhovered properly
        if self.image_rect.collidepoint(pg.mouse.get_pos()):
            adjusted_mouse_pos = self.adjust_mouse_pos(pg.mouse.get_pos())
            for pic_button in self.pic_buttons:
                pic_button.update(adjusted_mouse_pos)
        else:
            for pic_button in self.pic_buttons:
                pic_button.unhover()

    def change_state(self, new_state):
        self.button_group.unhover()
        for pic_button in self.pic_buttons:
            pic_button.unhover()
        self.next = new_state
        self.done = True

    def click(self):
        self.button_group.click()
        if self.slide_bar.click(pg.mouse.get_pos()):
            self.update_show_rect()
        for pic_button in self.pic_buttons:
            pic_button.click()

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'MENU':
            self.start()
            prepare.make_transition(self, 'HIGH_SCORE')

    def cleanup(self):
        self.done = False
        return self.persist

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.change_state('MENU')
            elif event.key == pg.K_UP:
                self.move_show_rect(-80)
            elif event.key == pg.K_DOWN:
                self.move_show_rect(80)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click()
            elif event.button == 4:
                self.move_show_rect(-80)
            elif event.button == 5:
                self.move_show_rect(80)
        elif event.type == pg.MOUSEBUTTONUP:
            self.slide_bar.unclick()

    def draw(self, surface):
        surface.fill(colors.BG_COLOR)
        for label in self.labels:
            label.draw(surface)
        surface.fill(colors.BLOCK_COLOR, self.buttons_block)
        self.button_group.draw(surface)
        self.update_image()
        surface.blit(self.image, self.image_rect, self.show_rect)
        self.slide_bar.draw(surface)

    def update(self, surface, dt):
        mouse_pos = pg.mouse.get_pos()
        self.update_picture_buttons()
        self.button_group.update(mouse_pos)
        self.slide_bar.update(mouse_pos)
        if self.slide_bar.slider.clicked:
            self.update_show_rect()
        self.draw(surface)
