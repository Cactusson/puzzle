"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare, tools
from .states import choose, game, load, menu, pause, transition


def main():
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {'CHOOSE': choose.Choose(),
                  'GAME': game.Game(),
                  'LOAD': load.Load(),
                  'MENU': menu.Menu(),
                  'PAUSE': pause.Pause(),
                  'TRANSITION': transition.Transition(),
                  }
    run_it.setup_states(state_dict, 'MENU')
    run_it.main()
