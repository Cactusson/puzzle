import pygame as pg
import random


BG_GAME_COLOR = pg.Color('#CEDCC3')
BUTTON_HOVER_TEXT_COLOR = pg.Color('#F6FAF7')

COLOR_PACKAGES = [
    {
        'BG_COLOR': pg.Color('#E7EAA8'),
        'BLOCK_COLOR': pg.Color('#B4BB72'),
        'BUTTON_HOVER_FILL_COLOR': pg.Color('#303E27'),
    },
    {
        'BG_COLOR': pg.Color('#e7dfd5'),
        'BLOCK_COLOR': pg.Color('#84a9ac'),
        'BUTTON_HOVER_FILL_COLOR': pg.Color('#3b6978'),
    },
    {
        'BG_COLOR': pg.Color('#d8ebb5'),
        'BLOCK_COLOR': pg.Color('#639a67'),
        'BUTTON_HOVER_FILL_COLOR': pg.Color('#2b580c'),
    },
]


def change_color_package():
    global BG_COLOR, BLOCK_COLOR, BUTTON_HOVER_FILL_COLOR
    package = random.choice(COLOR_PACKAGES)
    BG_COLOR = package['BG_COLOR']
    BLOCK_COLOR = package['BLOCK_COLOR']
    BUTTON_HOVER_FILL_COLOR = package['BUTTON_HOVER_FILL_COLOR']


change_color_package()
