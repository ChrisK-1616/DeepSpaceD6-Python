"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       game_sprite.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game sprite class
"""

# Imports
import pyglet


# Consts
# Globals
# Functions


# Classes
class GameSprite(pyglet.sprite.Sprite):
    def __init__(self, window=None, active=True, *args, **kwargs):
        """
        Initialiser for the GameSprite class, this is typically used as an abstract class that can be extended

        :attr _window: pyglet.window.Window object containing this sprite

        :attr _active: is this sprite currently active or inactive, use of this determined by the extended class

        :param window: window object containing this sprite
        :param active: initial active state of this sprite
        """
        super().__init__(*args, **kwargs)
        self._window = window
        self._active = active

    @property
    def window(self):
        return self._window

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if not value == self.active:
            old_value = self.active
            self._active = value
            self.on_active_changed(old_value)

    def on_active_changed(self, old_value):
        pass

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def updater(self, dt):
        pass
