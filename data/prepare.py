import os
import sys
import pygame as pg

from . import tools


SCREEN_SIZE = (1000, 600)
ORIGINAL_CAPTION = 'Puzzle'

# pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

PICS_AMOUNT = 10
DIFFICULTY_SIZE = (9, 16, 25)
TURN_TIME = [(3000, 6000), (4000, 8000), (5000, 10000)]
TRANSITION_TIME = 800

BG_COLOR = pg.Color('#E7EAA8')
BG_GAME_COLOR = pg.Color('#CEDCC3')
BLOCK_COLOR = pg.Color('#B4BB72')
BUTTON_HOVER_FILL_COLOR = pg.Color('#303E27')
BUTTON_HOVER_TEXT_COLOR = pg.Color('#F6FAF7')


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("resources", "graphics")
    GFX = {}
    for directory in directories:
        if directory == 'pictures':
            continue
        if getattr(sys, 'frozen', False):
            path = os.path.join(os.path.dirname(sys.executable), 'graphics',
                                directory)
        else:
            path = os.path.join(base_path, directory)
        GFX[directory] = tools.load_all_gfx(path)
    return GFX

_SUB_DIRECTORIES = ['gui', 'mini', 'pictures']
GFX = graphics_from_directories(_SUB_DIRECTORIES)

fonts_path = os.path.join('resources', 'fonts')
FONTS = tools.load_all_fonts(fonts_path)

# sfx_path = os.path.join('resources', 'sounds')
# SFX = tools.load_all_sfx(sfx_path)

# music_path = os.path.join('resources', 'music')
# MUSIC = tools.load_all_music(music_path)


def transparent_surface(width, height, alpha=0):
    surface = pg.Surface((width, height)).convert()
    surface.set_alpha(alpha)
    return surface.convert_alpha()


def make_transition(state, name, alpha_transition=False):
    image = pg.Surface(SCREEN_RECT.size).convert()
    state.draw(image)
    state.persist['next_state'] = name
    state.persist['next_image'] = image
    if alpha_transition:
        state.persist['alpha_transition'] = True
    state.next = 'TRANSITION'
    state.done = True
