"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       game_state.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - GameState class to be extended by concrete game application states
"""

# Imports
import pyglet
from engine.consts import *
from fsm.state import State


# Consts
# Globals
# Functions


# Classes
class GameState(State):
    def __init__(self, name, app):
        """
        Initialiser for the GameState class

        :attr _app: reference to the main game app object
        :attr _game_objects_batch: drawing batch for game objects
        :attr _game_objects: list of all game objects
        :attr _ui_objects_batch: drawing batch for UI objects
        :attr _ui_objects: list of all UI objects

        :if DEBUG:
        :attr _fps_display: used during debug to show fps

        :param name: name of this state as a string
        :param app: main game app object
        """
        super().__init__(name)
        self._app = app
        self._game_objects_batch = pyglet.graphics.Batch()
        self._game_objects = []
        self._ui_objects_batch = pyglet.graphics.Batch()
        self._ui_objects = []

        if DEBUG:
            self._fps_display = pyglet.window.FPSDisplay(self.app.game_window)

    @property
    def app(self):
        return self._app

    @property
    def game_objects(self):
        return self._game_objects

    @property
    def ui_objects(self):
        return self._ui_objects

    def update(self, dt):
        """
        Update method that updates all game and UI objects, note: if overridden by derived classes then this behaviour
        must also be included in any polymorphic version (or use super())

        :param dt: delta time in milliseconds since last update

        :return nothing
        """
        for obj in self.ui_objects:
            if obj.active and obj.enabled:
                obj.updater(dt)

        for obj in self.game_objects:
            if obj.active:
                obj.updater(dt)

    def draw(self, window):
        """
        Draw method that draws all game and UI objects, note: if overridden by derived classes then this behaviour
        must also be included in any polymorphic version (or use super())

        :param window: pyglet.window.Window object into which any drawing should be done

        :return nothing:
        """
        window.clear()
        self._game_objects_batch.draw()
        self._ui_objects_batch.draw()

        if DEBUG:
            self._fps_display.draw()
