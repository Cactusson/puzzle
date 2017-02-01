import pygame as pg

from .label import Label


class GUI:
    def __init__(self, best_time, difficulty, hardcore):
        if best_time is not None:
            self.best_time_label = pg.sprite.Sprite()
            self.best_time_label.image = self.create_best_time_label(best_time)
            self.best_time_label.rect = self.best_time_label.image.get_rect(
                topleft=(850, 65))
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

    def create_best_time_label(self, best_time):
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
        return image

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

    def draw(self, surface):
        if self.best_time_label is not None:
            surface.blit(self.best_time_label.image, self.best_time_label.rect)
        surface.blit(self.difficulty_label.image, self.difficulty_label.rect)
        surface.blit(self.hardcore_label.image, self.hardcore_label.rect)
