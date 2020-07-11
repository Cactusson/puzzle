import pygame as pg

from .. import prepare

from . import settings
from .label import Label
from .toggle_button import ToggleButton


class ChoiceBox:
    """
    ChoiceBox has a bunch of options, only one of them can be active.
    Player can click on any option to activate it, deactivating the
    previous activated one.
    """
    def __init__(
            self, rect, title, options, default, tooltip=None, inline=False
    ):
        self.rect = rect
        self.title = Label(22, title, font_name='Quicksand-Bold')
        if inline:
            self.title.rect.bottomleft = self.rect.bottomleft
            self.title.rect.bottom -= 10
        else:
            self.title.rect.center = self.rect.centerx, 0
            self.title.rect.top = self.rect.top
        self.toggles = self.create_toggles(options, default, inline)
        self.tooltip = tooltip

    def create_toggles(self, options, default, inline):
        """
        Creates all toggles, determining their positions.
        Activates toggle with the same name as default.
        """
        toggles = [ToggleButton(option) for option in reversed(options)]

        if inline:
            width = self.title.rect.width + \
                sum([t.rect.width for t in toggles])
            gap = (self.rect.width - width) // (len(toggles))
            pos = self.rect.bottomright
        else:
            width = sum([t.rect.width for t in toggles])
            gap = (self.rect.width - width) // (len(toggles) - 1)
            pos = self.rect.bottomright

        # print(gap)

        for toggle in toggles:
            if toggle.name == default:
                toggle.activate()
            toggle.rect.bottomright = pos
            pos = pos[0] - (toggle.rect.width + gap), pos[1]
        return toggles

    def click(self, mouse_pos):
        """
        On click checks if mouse_pos inside one of the toggles.
        If yes, proceed to activate it.
        Returns True if click was successful, False otherwise.
        """
        for toggle in self.toggles:
            if toggle.rect.collidepoint(mouse_pos) and not toggle.active:
                self.change_toggle(toggle)
                if settings.sound_on:
                    prepare.SFX['select'].play()
                return True
        return False

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

    def update_tooltip(self):
        """
        Makes the tooltip visible/invisible depending on whether mouse is
        hovering over the choice box.
        """
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.tooltip.visible = True
        else:
            self.tooltip.visible = False

    def draw(self, surface):
        self.title.draw(surface)
        for toggle in self.toggles:
            toggle.draw(surface)
        if self.tooltip and self.tooltip.visible:
            self.tooltip.draw(surface)

    def update(self, mouse_pos):
        if self.tooltip:
            self.update_tooltip()
        for toggle in self.toggles:
            toggle.update(mouse_pos)
