"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       gs_splash_screen.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game state to handle initial loading of the game application (beyond configuration and main game window
                  creation)
"""

# Imports
import pyglet
from engine.game_state import GameState
from engine.consts import *
from game_objects.splash_screen_sprite import SplashScreenSprite


# Consts
# Globals
# Functions


# Classes
class GSSplashScreen(GameState):
    def __init__(self, name, app):
        """
        Initialiser for the GSSplashScreen class

        :attr _screen_sprite: sprite for the splash screen

        :param name: name of this game state as a string
        :param app: main game app object
        """
        super().__init__(name, app)

        # Game objects
        self._screen_sprite = None

        # UI objects

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE or \
                symbol == pyglet.window.key.RETURN or \
                symbol == pyglet.window.key.NUM_ENTER or \
                symbol == pyglet.window.key.ESCAPE:
            self.fire_transition()
            return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        for obj in self.ui_objects:
            if obj.active and obj.enabled and obj.mouse_inside:
                return pyglet.event.EVENT_UNHANDLED

        self.fire_transition()
        return pyglet.event.EVENT_HANDLED

    def enter(self, state):
        """
        enter method for the GSSplashScreen game state, note: objects will only be instantiated if they currently are
        not instantiated, therefore only on the first entry into this state will new objects be instantiated

        :param state: fsm.state.State object that was left before entering this state

        :return nothing:
        """
        # This state now becomes the current game state
        self.app.current_game_state = self

        # :DEV: #
        if not self.app.game_window.fullscreen:
            self.app.game_window.set_caption("{0}   {1} - ({2}, {3})".format(WINDOW_CAPTION, self.name, 0, 0))
        # :DEV: #

        # Build game objects associated with this game state
        if not self._screen_sprite:
            scale_x = self.app.game_window.width / self.app.game_object_images["splash_screen"].width
            scale_y = self.app.game_window.height / self.app.game_object_images["splash_screen"].height

            self._screen_sprite = SplashScreenSprite(window=self.app.game_window,
                                                     img=self.app.game_object_images["splash_screen"],
                                                     batch=self._game_objects_batch)
            self._screen_sprite.update(scale_x=scale_x, scale_y=scale_y)
            self._screen_sprite.update(x=0, y=self._screen_sprite.window.height - self._screen_sprite.height)
            self.game_objects.append(self._screen_sprite)

        # Ensure all handlers for this game state are pushed onto the event stack of the game window
        self.app.game_window.push_handlers(self)
        for obj in self.game_objects:
            self.app.game_window.push_handlers(obj)

        for obj in self.ui_objects:
            self.app.game_window.push_handlers(obj)

    def leave(self, state):
        """
        leave method for the GSSplashScreen game state

        :param state: fsm.state.State object that will be entered after leaving this state

        :return nothing:
        """
        # Any event handlers specific to this game state that are on the event stack need to be removed from the game
        # window event stack so they don't fire
        for _ in range(len(self.game_objects) + len(self.ui_objects) + 1):
            self.app.game_window.pop_handlers()

    # :DEV: #
    def on_mouse_motion(self, x, y,    dx, dy):
        # Display some debug info on the window caption (if not full screen)
        if not self.app.game_window.fullscreen:
            self.app.game_window.set_caption("{0}   {1} [mouse:({2}, {3})]".format(WINDOW_CAPTION, self.name, x, y))
    # :DEV: #
