import itertools
import pygame as pg

from . import settings


class MusicStation:
    def __init__(self):
        self.active = False

    def create_playlist(self, songs):
        self.active = True
        self.playlist = itertools.cycle(songs)

    def play_next(self):
        self.current_song = next(self.playlist)
        pg.mixer.music.load(self.current_song)
        pg.mixer.music.play()

    def toggle_music(self):
        settings.music_on = not settings.music_on
        if not settings.music_on:
            pg.mixer.music.pause()
        else:
            pg.mixer.music.unpause()

    def update(self):
        if not settings.music_on or not self.active:
            return
        if not pg.mixer.music.get_busy():
            self.play_next()
