"""
This module contains the fundamental Control class and a prototype class
for States.  Also contained here are resource loading functions.
"""

import os
import pygame as pg

from .components.music_station import MusicStation

SCREEN_SIZE = (1000, 600)

music_station = MusicStation()


class Control(object):
    """
    Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here.
    """
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.fullscreen = False

    def setup_states(self, state_dict, start_state):
        """
        Given a dictionary of States and a State to start in,
        builds the self.state_dict.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup({})
        self.state.persist['difficulty'] = 1
        self.state.persist['hardcore'] = 0

    def update(self, dt):
        """
        Checks if a state is done or has called for a game quit.
        State is flipped if neccessary and State.update is called.
        """
        # you may want to pass self.keys to self.state.update
        state_flipped = False
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
            state_flipped = True
        if not state_flipped:
            self.state.update(self.screen, dt)
        music_station.update()

    def flip_state(self):
        """
        When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed.
        """
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(persist)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            pg.display.set_mode(SCREEN_SIZE, pg.FULLSCREEN)
        else:
            pg.display.set_mode(SCREEN_SIZE)

    def toggle_music(self):
        music_station.toggle_music()

    def event_loop(self):
        """
        Process all events and pass them down to current State.  The f5 key
        globally turns on/off the display of FPS in the caption
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    if pg.key.get_pressed()[pg.K_LALT]:
                        self.done = True
                elif event.key == pg.K_f:
                    self.toggle_fullscreen()
                # elif event.key == pg.K_m:
                #     self.toggle_music()
            self.state.get_event(event)

    def main(self):
        """
        Main loop for entire program.
        """
        while not self.done:
            time_delta = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(time_delta)
            pg.display.update()
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)


class _State(object):
    """
    This is a prototype class for States.  All states should inherit from it.
    No direct instances of this class should be created. get_event and update
    must be overloaded in the childclass.  startup and cleanup need to be
    overloaded when there is data that must persist between States.
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        """
        Processes events that were passed from the main event loop.
        Must be overloaded in children.
        """
        pass

    def startup(self, persistant):
        """
        Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time.
        """
        self.persist = persistant

    def cleanup(self):
        """
        Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False.
        """
        self.done = False
        return self.persist

    def update(self, surface):
        """
        Update function for state.  Must be overloaded in children.
        """
        pass


# Resource loading functions.
def load_all_gfx(directory, colorkey=(255, 0, 255),
                 accept=(".png", ".jpg", ".bmp")):
    """
    Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey.
    """
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics


def load_all_sfx(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


def load_all_music(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """
    Create a dictionary of paths to music files in given directory
    if their extensions are in accept.
    """
    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=(".ttf", '.otf')):
    """Create a dictionary of paths to font files in given directory
    if their extensions are in accept."""
    return load_all_music(directory, accept)


def time_to_text(time):
    if time == 0:
        return '---'
    minutes = str(time // 60)
    if len(minutes) == 1:
        minutes = '0' + minutes
    seconds = str(time % 60)
    if len(seconds) == 1:
        seconds = '0' + seconds
    return '{}:{}'.format(minutes, seconds)
