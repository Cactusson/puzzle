import os
import sys
import pygame as pg

from . import tools


SCREEN_SIZE = (1000, 600)
ORIGINAL_CAPTION = 'Puzzle'

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

PICS_AMOUNT = 10
DIFFICULTY_SIZE = (9, 16, 25)
TURN_TIME = [(5000, 10000), (4000, 8000), (3000, 6000)]
TRANSITION_TIME = 700


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("resources", "graphics")
    GFX = {}
    for directory in directories:
        if getattr(sys, 'frozen', False):
            path = os.path.join(os.path.dirname(sys.executable), 'graphics',
                                directory)
        else:
            path = os.path.join(base_path, directory)
        GFX[directory] = tools.load_all_gfx(path)
    return GFX


_SUB_DIRECTORIES = ['gui']
GFX = graphics_from_directories(_SUB_DIRECTORIES)

fonts_path = os.path.join('resources', 'fonts')
FONTS = tools.load_all_fonts(fonts_path)

sfx_path = os.path.join('resources', 'sounds')
SFX = tools.load_all_sfx(sfx_path)

music_path = os.path.join('resources', 'music')
MUSIC = tools.load_all_music(music_path)

tools.music_station.create_playlist(MUSIC.values())


def transparent_surface(width, height, alpha=0):
    surface = pg.Surface((width, height)).convert()
    surface.set_alpha(alpha)
    return surface.convert_alpha()


def make_transition(state, name, alpha_transition=False, duration=None):
    image = pg.Surface(SCREEN_RECT.size).convert()
    state.draw(image)
    state.persist['next_state'] = name
    state.persist['next_image'] = image
    if alpha_transition:
        state.persist['alpha_transition'] = True
    if duration:
        state.persist['duration'] = duration
    state.next = 'TRANSITION'
    state.done = True
