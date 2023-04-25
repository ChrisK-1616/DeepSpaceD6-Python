"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       gs_new_game.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game state to handle new game screen
"""

# Imports
from engine.game_state import GameState
from engine.consts import *
from game_objects.new_game_screen_sprite import NewGameScreenSprite
from ui.push_button import PushButton


# Consts
# Globals
# Functions


# Classes
class GSNewGame(GameState):
    def __init__(self, name, app):
        """
        Initialiser for the GSNewGame class

        :attr _screen_sprite: sprite for the credits screen

        :param name: name of this game state as a string
        :param app: main game app object
        """
        super().__init__(name, app)

        # Game objects
        self._screen_sprite = None

        # UI objects
        self._btn_back = None
        self._btn_start = None

    def enter(self, state):
        """
        enter method for the GSNewGame game state, note: objects will only be instantiated if they currently are not
        instantiated, therefore only on the first entry into this state will new objects be instantiated

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
            scale_x = self.app.game_window.width / self.app.game_object_images["new_game_screen"].width
            scale_y = self.app.game_window.height / self.app.game_object_images["new_game_screen"].height

            self._screen_sprite = NewGameScreenSprite(window=self.app.game_window,
                                                      img=self.app.game_object_images["new_game_screen"],
                                                      batch=self._game_objects_batch)
            self._screen_sprite.update(scale_x=scale_x, scale_y=scale_y)
            self._screen_sprite.update(x=0, y=self._screen_sprite.window.height - self._screen_sprite.height)
            self.game_objects.append(self._screen_sprite)

        # Build UI objects for the various functions of this game state
        if not self._btn_back:
            self._btn_back = PushButton(window=self.app.game_window,
                                        img=self.app.ui_object_images["btn_back_e"],
                                        disabled_image=self.app.ui_object_images["btn_back_d"],
                                        enabled_image=self.app.ui_object_images["btn_back_e"],
                                        hover_image=self.app.ui_object_images["btn_back_h"],
                                        pressed_image=self.app.ui_object_images["btn_back_p"],
                                        batch=self._ui_objects_batch,
                                        command=None,
                                        hit_area=None)
            self._btn_back.x = 48 * self._screen_sprite.scale_x
            self._btn_back.y = 27 * self._screen_sprite.scale_y
            self._btn_back.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_back)

        if not self._btn_start:
            self._btn_start = PushButton(window=self.app.game_window,
                                         img=self.app.ui_object_images["btn_start_e"],
                                         disabled_image=self.app.ui_object_images["btn_start_d"],
                                         enabled_image=self.app.ui_object_images["btn_start_e"],
                                         hover_image=self.app.ui_object_images["btn_start_h"],
                                         pressed_image=self.app.ui_object_images["btn_start_p"],
                                         batch=self._ui_objects_batch,
                                         command=None,
                                         hit_area=None)
            self._btn_start.x = 1672 * self._screen_sprite.scale_x
            self._btn_start.y = 27 * self._screen_sprite.scale_y
            self._btn_start.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_start)

        # Define the various UI commands
        def btn_back_cmd(source, data):
            x, y, button, modifiers = data
            print("Back - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            # The 'back' button goes back to the specific menu state it originated from
            self.fire_transition(self.app.game_states["main_menu_screen"])

        def btn_start_cmd(source, data):
            x, y, button, modifiers = data
            print("Start - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["game_play_screen"])

        # Ensure the correct instances of the button commands are wired up to their requisite buttons
        self._btn_back.command = btn_back_cmd
        self._btn_start.command = btn_start_cmd

        # Ensure all handlers for this game state are pushed onto the event stack of the game window
        self.app.game_window.push_handlers(self)
        for obj in self.game_objects:
            self.app.game_window.push_handlers(obj)

        for obj in self.ui_objects:
            self.app.game_window.push_handlers(obj)

    def leave(self, state):
        """
        leave method for the GSNewGame game state

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
