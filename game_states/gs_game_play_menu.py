"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       gs_game_play_menu.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game state to handle game play menu of the game application
"""

# Imports
import pyglet
from engine.game_state import GameState
from engine.game_sprite import GameSprite
from engine.consts import *
from game_objects.game_play_menu_screen_sprite import GamePlayMenuScreenSprite
from ui.push_button import PushButton


# Consts
# Globals
# Functions


# Classes
class GSGamePlayMenu(GameState):
    def __init__(self, name, app):
        """
        Initialiser for the GSGamePlayMenu class

        :attr _screen_sprite: sprite that is initialised from the game play screen captured at the time the game play
                              menu state is transition to
        :attr _mask_sprite: a sprite for the overlay of the background screen for the game play menu
        :attr _game_play_menu_screen_sprite: a sprite for the background of the game play menu items

        :param name: name of this game state as a string
        :param app: main game app object
        """
        super().__init__(name, app)

        # Game objects
        self._screen_sprite = None
        self._mask_sprite = None
        self._game_play_menu_screen_sprite = None
        self._ordered_groups = [pyglet.graphics.Group(i) for i in range(3)]

        # UI objects
        self._btn_resume = None
        self._btn_save = None
        self._btn_load = None
        self._btn_options = None
        self._btn_main_menu = None

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.fire_transition(self.app.game_states["game_play_screen"])

    def enter(self, state):
        """
        enter method for the GSGamePlayMenu game state, note: objects will only be instantiated if they currently are not
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
            self._screen_sprite = GamePlayMenuScreenSprite(window=self.app.game_window,
                                                           img=state.screen_capture,
                                                           batch=self._game_objects_batch,
                                                           group=self._ordered_groups[0])
            self._screen_sprite.update(x=0,
                                       y=self._screen_sprite.window.height - self._screen_sprite.height)
            self.game_objects.append(self._screen_sprite)

        # Only renew the screen capture if entering directly from the game play state (as other states do not have the
        # screen capture available)
        from game_states.gs_game_play import GSGamePlay
        if type(state) is GSGamePlay:
            self._screen_sprite.image = state.screen_capture

        if not self._mask_sprite:
            scale_x = self.app.game_window.width / self.app.game_object_images["game_play_menu_mask"].width
            scale_y = self.app.game_window.height / self.app.game_object_images["game_play_menu_mask"].height

            self._mask_sprite = GameSprite(window=self.app.game_window,
                                           img=self.app.game_object_images["game_play_menu_mask"],
                                           batch=self._game_objects_batch,
                                           group=self._ordered_groups[1])
            self._mask_sprite.update(scale_x=scale_x, scale_y=scale_y)
            self._mask_sprite.update(x=0, y=self._mask_sprite.window.height - self._mask_sprite.height)
            self.game_objects.append(self._mask_sprite)

        if not self._game_play_menu_screen_sprite:
            scale_x = self.app.game_window.width / self.app.game_object_images["game_play_menu_mask"].width
            scale_y = self.app.game_window.height / self.app.game_object_images["game_play_menu_mask"].height

            self._game_play_menu_screen_sprite = GameSprite(window=self.app.game_window,
                                                            img=self.app.game_object_images["game_play_menu_screen"],
                                                            batch=self._game_objects_batch,
                                                            group=self._ordered_groups[2])
            self._game_play_menu_screen_sprite.update(scale_x=scale_x, scale_y=scale_y)
            self._game_play_menu_screen_sprite.update(x=670 * scale_x, y=210 * scale_y)
            self.game_objects.append(self._game_play_menu_screen_sprite)

        # Build UI objects for the various menu options
        if not self._btn_resume:
            self._btn_resume = PushButton(window=self.app.game_window,
                                          img=self.app.ui_object_images["game_play_menu_btn_resume_e"],
                                          disabled_image=self.app.ui_object_images["game_play_menu_btn_resume_d"],
                                          enabled_image=self.app.ui_object_images["game_play_menu_btn_resume_e"],
                                          hover_image=self.app.ui_object_images["game_play_menu_btn_resume_h"],
                                          pressed_image=self.app.ui_object_images["game_play_menu_btn_resume_p"],
                                          batch=self._ui_objects_batch,
                                          command=None,
                                          hit_area=None)
            self._btn_resume.x = 710 * self._mask_sprite.scale_x
            self._btn_resume.y = 700 * self._mask_sprite.scale_y
            self._btn_resume.change_scale(self._mask_sprite.scale_x, self._mask_sprite.scale_y)
            self.ui_objects.append(self._btn_resume)

        if not self._btn_save:
            self._btn_save = PushButton(window=self.app.game_window,
                                        img=self.app.ui_object_images["game_play_menu_btn_save_e"],
                                        disabled_image=self.app.ui_object_images["game_play_menu_btn_save_d"],
                                        enabled_image=self.app.ui_object_images["game_play_menu_btn_save_e"],
                                        hover_image=self.app.ui_object_images["game_play_menu_btn_save_h"],
                                        pressed_image=self.app.ui_object_images["game_play_menu_btn_save_p"],
                                        batch=self._ui_objects_batch,
                                        command=None,
                                        hit_area=None)
            self._btn_save.x = 710 * self._mask_sprite.scale_x
            self._btn_save.y = 600 * self._mask_sprite.scale_y
            self._btn_save.change_scale(self._mask_sprite.scale_x, self._mask_sprite.scale_y)
            self.ui_objects.append(self._btn_save)

        if not self._btn_load:
            self._btn_load = PushButton(window=self.app.game_window,
                                        img=self.app.ui_object_images["game_play_menu_btn_load_e"],
                                        disabled_image=self.app.ui_object_images["game_play_menu_btn_load_d"],
                                        enabled_image=self.app.ui_object_images["game_play_menu_btn_load_e"],
                                        hover_image=self.app.ui_object_images["game_play_menu_btn_load_h"],
                                        pressed_image=self.app.ui_object_images["game_play_menu_btn_load_p"],
                                        batch=self._ui_objects_batch,
                                        command=None,
                                        hit_area=None)
            self._btn_load.x = 710 * self._mask_sprite.scale_x
            self._btn_load.y = 500 * self._mask_sprite.scale_y
            self._btn_load.change_scale(self._mask_sprite.scale_x, self._mask_sprite.scale_y)
            self.ui_objects.append(self._btn_load)

        if not self._btn_options:
            self._btn_options = PushButton(window=self.app.game_window,
                                           img=self.app.ui_object_images["game_play_menu_btn_options_e"],
                                           disabled_image=self.app.ui_object_images["game_play_menu_btn_options_d"],
                                           enabled_image=self.app.ui_object_images["game_play_menu_btn_options_e"],
                                           hover_image=self.app.ui_object_images["game_play_menu_btn_options_h"],
                                           pressed_image=self.app.ui_object_images["game_play_menu_btn_options_p"],
                                           batch=self._ui_objects_batch,
                                           command=None,
                                           hit_area=None)
            self._btn_options.x = 710 * self._mask_sprite.scale_x
            self._btn_options.y = 400 * self._mask_sprite.scale_y
            self._btn_options.change_scale(self._mask_sprite.scale_x, self._mask_sprite.scale_y)
            self.ui_objects.append(self._btn_options)

        if not self._btn_main_menu:
            self._btn_main_menu = PushButton(window=self.app.game_window,
                                             img=self._app.ui_object_images["game_play_menu_btn_main_e"],
                                             disabled_image=self.app.ui_object_images["game_play_menu_btn_main_d"],
                                             enabled_image=self.app.ui_object_images["game_play_menu_btn_main_e"],
                                             hover_image=self.app.ui_object_images["game_play_menu_btn_main_h"],
                                             pressed_image=self.app.ui_object_images["game_play_menu_btn_main_p"],
                                             batch=self._ui_objects_batch,
                                             command=None,
                                             hit_area=None)
            self._btn_main_menu.x = 710 * self._mask_sprite.scale_x
            self._btn_main_menu.y = 300 * self._mask_sprite.scale_y
            self._btn_main_menu.change_scale(self._mask_sprite.scale_x, self._mask_sprite.scale_y)
            self.ui_objects.append(self._btn_main_menu)

        # Define the various UI commands
        def btn_resume_cmd(source, data):
            x, y, button, modifiers = data
            print("Resume - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["game_play_screen"])

        def btn_save_cmd(source, data):
            x, y, button, modifiers = data
            print("Save Game - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["save_game_screen"])

        def btn_load_cmd(source, data):
            x, y, button, modifiers = data
            print("Load Game - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["load_game_screen"])

        def btn_options_cmd(source, data):
            x, y, button, modifiers = data
            print("Options - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["options_screen"])

        def btn_main_menu_cmd(source, data):
            x, y, button, modifiers = data
            print("Main Menu - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["main_menu_screen"])

        # Ensure the correct instances of the button commands are wired up to their requisite buttons
        self._btn_resume.command = btn_resume_cmd
        self._btn_save.command = btn_save_cmd
        self._btn_load.command = btn_load_cmd
        self._btn_options.command = btn_options_cmd
        self._btn_main_menu.command = btn_main_menu_cmd

        # Ensure all handlers for this game state are pushed onto the event stack of the game window
        self.app.game_window.push_handlers(self)
        for obj in self.game_objects:
            self.app.game_window.push_handlers(obj)

        for obj in self.ui_objects:
            self.app.game_window.push_handlers(obj)

    def leave(self, state):
        """
        leave method for the GSGamePlayMenu game state

        :param state: fsm.state.State object that will be entered after leaving this state

        :return nothing:
        """
        # Any event handlers specific to this game state that are on the event stack need to be removed from the game
        # window event stack so they don't fire
        for _ in range(len(self.game_objects) + len(self.ui_objects) + 1):
            self.app.game_window.pop_handlers()

    # :DEV: #
    def on_mouse_press(self, x, y, button, modifiers):
        pass
    # :DEV: #

    # :DEV: #
    def on_mouse_motion(self, x, y,    dx, dy):
        # Display some debug info on the window caption (if not full screen)
        if not self.app.game_window.fullscreen:
            self.app.game_window.set_caption("{0}   {1} [mouse:({2}, {3})]".format(WINDOW_CAPTION, self.name, x, y))
    # :DEV: #
