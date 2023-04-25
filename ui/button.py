"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       button.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Button UI widget class
"""

# Imports
import pyglet
from ui.ui_sprite import UISprite


# Consts
# Globals
# Functions


# Classes
class Button(UISprite):
    def __init__(self, disabled_image=None, enabled_image=None, hover_image=None, command=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._disabled_image = disabled_image if disabled_image else self.image
        self._enabled_image = enabled_image if enabled_image else self.image
        self._hover_image = hover_image if hover_image else self.image
        self._command = command

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    def on_enabled_changed(self, old_value):
        if not self.enabled:
            self.image = self._disabled_image
        else:
            self.image = self._enabled_image

    def updater(self, dt):
        super().updater(dt)

    def on_mouse_entered(self):
        self.image = self._hover_image

    def on_mouse_left(self):
        self.image = self._enabled_image
