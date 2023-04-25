"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       push_button.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Push button UI widget class
"""

# Imports
import pyglet
from ui.button import Button


# Consts
# Globals
# Functions


# Classes
class PushButton(Button):
    def __init__(self, pressed_image=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pressed_image = pressed_image if pressed_image else self.image

    def on_mouse_press(self, x, y, button, modifiers):
        def reset(dt):
            # Only return to hover or enabled image if still enabled otherwise return to disabled image
            if self.enabled:
                # Only return to the hover image if mouse is inside the button otherwise return to enabled image, so
                # check this and act accordingly
                self.establish_mouse_inside(x, y)
                if self.mouse_inside:
                    self.image = self._hover_image
                else:
                    self.image = self._enabled_image
            else:
                self.image = self._disabled_image

        def cmd(dt):
            self.command(source=self, data=(x, y, button, modifiers))

        # Only react to mouse button press if enabled and if the mouse button is a left button press
        if self.enabled and button == pyglet.window.mouse.LEFT:
            if self._mouse_inside:
                self.image = self._pressed_image
                pyglet.clock.schedule_once(reset, 0.1)
                if self.command:
                    pyglet.clock.schedule_once(cmd, 0.2)
                return pyglet.event.EVENT_HANDLED

