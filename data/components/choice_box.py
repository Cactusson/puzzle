import pygame as pg

from .label import Label
from .toggle_button import ToggleButton


class ChoiceBox:
    """
    ChoiceBox has a bunch of options, only one of them can be active.
    Player can click on any option to activate it, deactivating the
    previous activated one.
    """
    def __init__(self, rect, title, options, default=None):
        self.rect = rect
        self.title = Label(22, title, center=(self.rect.centerx, 0),
                           font_name='OpenSans-Bold')
        self.title.rect.top = self.rect.top
        self.toggles = self.create_toggles(options, default)

    def create_toggles(self, options, default):
        """
        Creates all toggles, determining their positions.
        If default is given, activates toggle with the same name as default.
        """
        toggles = []
        for option in options:
            toggle = ToggleButton(option)
            toggles.append(toggle)
        width = sum([t.rect.width for t in toggles])
        gap = (self.rect.width - width) // (len(toggles) - 1)
        pos = [self.rect.left,
               self.rect.bottom - toggles[0].rect.height]
        for toggle in toggles:
            if toggle.name == default:
                toggle.activate()
            toggle.rect.bottomleft = pos
            pos[0] += toggle.rect.width + gap
        return toggles

    def click(self, mouse_pos):
        """
        On click checks if mouse_pos inside one of the toggles.
        If yes, proceed to activate it.
        """
        for toggle in self.toggles:
            if toggle.rect.collidepoint(mouse_pos):
                self.change_toggle(toggle)
                return

    def change_toggle(self, new_toggle):
        """
        Finds an activated toggle (if any), deactivates it,
        then activates the new one.
        """
        if new_toggle.active:
            return
        for toggle in self.toggles:
            if toggle.active:
                toggle.deactivate()
                break
        new_toggle.activate()

    def get_active(self):
        """
        Returns the name of the activated toggle.
        If there is no active toggle, returns None.
        """
        for toggle in self.toggles:
            if toggle.active:
                return toggle.name
        return None

    def draw(self, surface):
        self.title.draw(surface)
        for toggle in self.toggles:
            toggle.draw(surface)

    def update(self, mouse_pos):
        pass
