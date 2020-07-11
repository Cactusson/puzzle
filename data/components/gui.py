import pygame as pg

from .animation import Animation
from .button import Button
from .label import Label


class GUI:
    def __init__(self, best_time, difficulty, hardcore, finish_callback):
        self.animations = pg.sprite.Group()
        if best_time is not None:
            self.create_best_time_label(best_time)
        else:
            self.best_time_label = None

        self.difficulty_label = pg.sprite.Sprite()
        self.difficulty_label.image = self.create_difficulty_label(difficulty)
        self.difficulty_label.rect = self.difficulty_label.image.get_rect(
            topleft=(850, 540))
        self.hardcore_label = pg.sprite.Sprite()
        self.hardcore_label.image = self.create_hardcore_label(hardcore)
        self.hardcore_label.rect = self.hardcore_label.image.get_rect(
            topleft=(850, 560))

        self.finish_button = Button(
            30, 'Well done! Click here to continue', finish_callback,
            font_name='Quicksand-Regular', topleft=(35, 650))
        self.finish_button.hover_image = self.finish_button.idle_image
        self.finish_button.name = None

    def create_best_time_label(self, best_time):
        self.best_time_label = pg.sprite.Sprite()

        image = pg.Surface((140, 30)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        first_label = Label(
            15, 'Best time:',
            font_name='OpenSans-Bold', topleft=(0, 0))
        second_label = Label(
            15, '{}'.format(best_time),
            font_name='OpenSans-Regular', topleft=(85, 0))
        first_label.draw(image)
        second_label.draw(image)

        self.best_time_label.image = image
        self.best_time_label.rect = image.get_rect(topleft=(850, 70))

    def create_difficulty_label(self, difficulty):
        text = ['EASY', 'NORMAL', 'HARD'][difficulty]
        image = pg.Surface((150, 30)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        first_label = Label(
            15, 'Difficulty:',
            font_name='OpenSans-Bold', topleft=(0, 0))
        second_label = Label(
            15, '{}'.format(text),
            font_name='OpenSans-Regular', topleft=(80, 0))
        first_label.draw(image)
        second_label.draw(image)
        return image

    def create_hardcore_label(self, hardcore):
        text = ['OFF', 'ON'][hardcore]
        image = pg.Surface((140, 30)).convert()
        image.set_alpha(0)
        image = image.convert_alpha()
        first_label = Label(
            15, 'Hardcore:',
            font_name='OpenSans-Bold', topleft=(0, 0))
        second_label = Label(
            15, '{}'.format(text),
            font_name='OpenSans-Regular', topleft=(80, 0))
        first_label.draw(image)
        second_label.draw(image)
        return image

    def click(self):
        self.finish_button.click()

    def show_finish_button(self):
        animation = Animation(
            x=self.finish_button.rect.x, y=550, duration=1000,
            round_values=True, transition='in_back')
        animation.start(self.finish_button.rect)
        self.animations.add(animation)

    def draw(self, surface):
        if self.best_time_label is not None:
            surface.blit(self.best_time_label.image, self.best_time_label.rect)
        surface.blit(self.difficulty_label.image, self.difficulty_label.rect)
        surface.blit(self.hardcore_label.image, self.hardcore_label.rect)
        self.finish_button.draw(surface)

    def update(self, mouse_pos, dt):
        self.animations.update(dt * 1000)
        self.finish_button.update(mouse_pos)
