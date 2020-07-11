"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare, tools
from .states.choose import Choose
from .states.game import Game
from .states.high_score import HighScore
from .states.load import Load
from .states.menu import Menu
from .states.pause import Pause
from .states.settings import Settings
from .states.show_pic import ShowPic
from .states.transition import Transition


def main():
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {
        'CHOOSE': Choose(),
        'GAME': Game(),
        'HIGH_SCORE': HighScore(),
        'LOAD': Load(),
        'MENU': Menu(),
        'PAUSE': Pause(),
        'SETTINGS': Settings(),
        'SHOW_PIC': ShowPic(),
        'TRANSITION': Transition(),
                  }
    run_it.setup_states(state_dict, 'LOAD')
    run_it.main()
