"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       gs_game_play.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game state to handle game play screen
"""

# Imports
import pyglet
from engine.game_state import GameState
from engine.consts import *
from game_objects.game_play_screen_sprite import GamePlayScreenSprite
from game_objects.game_main_board_sprite import GameMainBoardSprite
from ui.push_button import PushButton


# Consts
# Globals
# Functions


# Classes
class GSGamePlay(GameState):
    def __init__(self, name, app):
        """
        Initialiser for the GSGamePlay class

        :attr _screen_sprite: sprite for the game play screen
        :attr _screen_capture: image of the current game play to use as back screen for game play menu state
        :attr _btn_back: push button to move back from this state
        :attr _reentry: determines if the originating state forces an initialisation of the state (False) or not (True)
        :attr _game_main_board: the current game main board for this game play scenario


        :param name: name of this game state as a string
        :param app: main game app object
        """
        super().__init__(name, app)

        # Game objects
        self._screen_sprite = None
        self._screen_capture = None
        self._game_main_board = None
        self._ordered_groups = [pyglet.graphics.Group(i) for i in range(2)]

        # UI objects
        self._btn_back = None

        # State specific properties
        self._reentry = False

    @property
    def screen_capture(self):
        return self._screen_capture

    @screen_capture.setter
    def screen_capture(self, value):
        self._screen_capture = value

    def enter(self, state):
        """
        enter() method for the GSGamePlay game state, note: objects will only be instantiated if they currently are not
        instantiated, therefore only on the first entry into this state will new objects be instantiated

        :param state: fsm.state.State object that was left before entering this state

        :return nothing:
        """
        # Check which state the game play state is entered from, if this is GSNewGame or GSLoadGame state then it is
        # the first time the game play has been entered and all game play and UI objects should be initialised,
        # however, if the game play state is entered from the GSGamePlayMenu state then it is a 'resume' and so the
        # current game and UI objects should not be re-initialised.
        from game_states.gs_new_game import GSNewGame
        from game_states.gs_load_game import GSLoadGame
        self._reentry = False if (type(state) is GSNewGame or type(state) is GSLoadGame) else True

        # This state now becomes the current game state
        self.app.current_game_state = self

        # :DEV: #
        if not self.app.game_window.fullscreen:
            self.app.game_window.set_caption("{0}   {1} - ({2}, {3})".format(WINDOW_CAPTION, self.name, 0, 0))
        # :DEV: #

        if not self._reentry:
            # Build game objects associated with this game state
            if not self._screen_sprite:
                self._screen_sprite = GamePlayScreenSprite(window=self.app.game_window,
                                                           img=self.app.game_object_images["game_play_screen"],
                                                           batch=self._game_objects_batch,
                                                           group=self._ordered_groups[0])
                self.game_objects.append(self._screen_sprite)
            else:
                self._screen_sprite.image = self.app.game_object_images["game_play_screen"]

            scale_x = self.app.game_window.width / self.app.game_object_images["game_play_screen"].width
            scale_y = self.app.game_window.height / self.app.game_object_images["game_play_screen"].height
            self._screen_sprite.update(x=0, y=self._screen_sprite.window.height - self._screen_sprite.height,
                                       scale_x=scale_x, scale_y=scale_y)

            if not self._game_main_board:
                images = [self.app.game_object_images["game_main_board"]]
                self._game_main_board = GameMainBoardSprite(game_play_state=self,
                                                            game_board_images=images,
                                                            window=self.app.game_window,
                                                            batch=self._game_objects_batch,
                                                            group=self._ordered_groups[1])
                self.game_objects.append(self._game_main_board)

            self._game_main_board.reinitialise()

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
                self._ui_objects.append(self._btn_back)

        # Define the various UI commands
        def btn_back_cmd(source, data):
            x, y, button, modifiers = data
            print("Back - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["main_menu_screen"])

        # Ensure the correct instances of the button commands are wired up to their requisite buttons
        self._btn_back.command = btn_back_cmd

        # Ensure all handlers for this game state are pushed onto the event stack of the game window
        self.app.game_window.push_handlers(self)
        for obj in self.game_objects:
            self.app.game_window.push_handlers(obj)

        for obj in self.ui_objects:
            self.app.game_window.push_handlers(obj)

    def leave(self, state):
        """
        leave method for the GSGamePlay game state

        :param state: fsm.state.State object that will be entered after leaving this state

        :return nothing:
        """
        # Any event handlers specific to this game state that are on the event stack need to be removed from the game
        # window event stack so they don't fire
        for _ in range(len(self.game_objects) + len(self.ui_objects) + 1):
            self.app.game_window.pop_handlers()

    # :DEV: #
    def on_mouse_motion(self, x, y, dx, dy):
        # Display some debug info on the window caption (if not full screen)
        if not self.app.game_window.fullscreen:
            obj = self.app.game_window
            obj.set_caption("{0}   {1} [mouse:({2}, {3}) scale:{4:.2f}"
                            "  offset:({5}, {6})]".format(WINDOW_CAPTION, self.name, x, y, self._game_main_board.scale,
                                                          self._game_main_board.x, self._game_main_board.y))
# :DEV: #
