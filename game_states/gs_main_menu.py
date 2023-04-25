"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       gs_main_menu.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game state to handle main menu of the game application
"""

# Imports
from engine.game_state import GameState
from engine.consts import *
from game_objects.main_menu_sprite import MainMenuSprite
from ui.push_button import PushButton


# Consts
# Globals
# Functions


# Classes
class GSMainMenu(GameState):
    def __init__(self, name, app):
        """
        Initialiser for the GSMainMenu class

        :attr _screen_sprite: sprite for the main menu

        :param name: name of this game state as a string
        :param app: main game app object
        """
        super().__init__(name, app)

        # Game objects
        self._screen_sprite = None

        # UI objects
        self._btn_new = None
        self._btn_load = None
        self._btn_options = None
        self._btn_credits = None
        self._btn_extras = None
        self._btn_quit = None

    def enter(self, state):
        """
        enter method for the GSMainMenu game state, note: objects will only be instantiated if they currently are not
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
            scale_x = self.app.game_window.width / self.app.game_object_images["main_menu_screen"].width
            scale_y = self.app.game_window.height / self.app.game_object_images["main_menu_screen"].height

            self._screen_sprite = MainMenuSprite(window=self.app.game_window,
                                                 img=self.app.game_object_images["main_menu_screen"],
                                                 batch=self._game_objects_batch)
            self._screen_sprite.update(scale_x=scale_x, scale_y=scale_y)
            self._screen_sprite.update(x=0, y=self._screen_sprite.window.height - self._screen_sprite.height)
            self.game_objects.append(self._screen_sprite)

        # Build UI objects for the various menu options
        if not self._btn_new:
            self._btn_new = PushButton(window=self.app.game_window,
                                       img=self.app.ui_object_images["main_menu_btn_new_e"],
                                       disabled_image=self.app.ui_object_images["main_menu_btn_new_d"],
                                       enabled_image=self.app.ui_object_images["main_menu_btn_new_e"],
                                       hover_image=self.app.ui_object_images["main_menu_btn_new_h"],
                                       pressed_image=self.app.ui_object_images["main_menu_btn_new_p"],
                                       batch=self._ui_objects_batch,
                                       command=None,
                                       hit_area=None)
            self._btn_new.x = 1250 * self._screen_sprite.scale_x
            self._btn_new.y = 900 * self._screen_sprite.scale_y
            self._btn_new.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_new)

        if not self._btn_load:
            self._btn_load = PushButton(window=self.app.game_window,
                                        img=self.app.ui_object_images["main_menu_btn_load_e"],
                                        disabled_image=self.app.ui_object_images["main_menu_btn_load_d"],
                                        enabled_image=self.app.ui_object_images["main_menu_btn_load_e"],
                                        hover_image=self.app.ui_object_images["main_menu_btn_load_h"],
                                        pressed_image=self.app.ui_object_images["main_menu_btn_load_p"],
                                        batch=self._ui_objects_batch,
                                        command=None,
                                        hit_area=None)
            self._btn_load.x = 1250 * self._screen_sprite.scale_x
            self._btn_load.y = 780 * self._screen_sprite.scale_y
            self._btn_load.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_load)

        if not self._btn_options:
            self._btn_options = PushButton(window=self.app.game_window,
                                           img=self.app.ui_object_images["main_menu_btn_options_e"],
                                           disabled_image=self.app.ui_object_images["main_menu_btn_options_d"],
                                           enabled_image=self.app.ui_object_images["main_menu_btn_options_e"],
                                           hover_image=self.app.ui_object_images["main_menu_btn_options_h"],
                                           pressed_image=self.app.ui_object_images["main_menu_btn_options_p"],
                                           batch=self._ui_objects_batch,
                                           command=None,
                                           hit_area=None)
            self._btn_options.x = 1250 * self._screen_sprite.scale_x
            self._btn_options.y = 660 * self._screen_sprite.scale_y
            self._btn_options.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_options)

        if not self._btn_credits:
            self._btn_credits = PushButton(window=self.app.game_window,
                                           img=self.app.ui_object_images["main_menu_btn_credits_e"],
                                           disabled_image=self.app.ui_object_images["main_menu_btn_credits_d"],
                                           enabled_image=self.app.ui_object_images["main_menu_btn_credits_e"],
                                           hover_image=self.app.ui_object_images["main_menu_btn_credits_h"],
                                           pressed_image=self.app.ui_object_images["main_menu_btn_credits_p"],
                                           batch=self._ui_objects_batch,
                                           command=None,
                                           hit_area=None)
            self._btn_credits.x = 1250 * self._screen_sprite.scale_x
            self._btn_credits.y = 540 * self._screen_sprite.scale_y
            self._btn_credits.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_credits)

        if not self._btn_extras:
            self._btn_extras = PushButton(window=self.app.game_window,
                                          img=self.app.ui_object_images["main_menu_btn_extras_e"],
                                          disabled_image=self.app.ui_object_images["main_menu_btn_extras_d"],
                                          enabled_image=self.app.ui_object_images["main_menu_btn_extras_e"],
                                          hover_image=self.app.ui_object_images["main_menu_btn_extras_h"],
                                          pressed_image=self.app.ui_object_images["main_menu_btn_extras_p"],
                                          batch=self._ui_objects_batch,
                                          command=None,
                                          hit_area=None)
            self._btn_extras.x = 1250 * self._screen_sprite.scale_x
            self._btn_extras.y = 420 * self._screen_sprite.scale_y
            self._btn_extras.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_extras)

        if not self._btn_quit:
            self._btn_quit = PushButton(window=self.app.game_window,
                                        img=self._app.ui_object_images["main_menu_btn_quit_e"],
                                        disabled_image=self.app.ui_object_images["main_menu_btn_quit_d"],
                                        enabled_image=self.app.ui_object_images["main_menu_btn_quit_e"],
                                        hover_image=self.app.ui_object_images["main_menu_btn_quit_h"],
                                        pressed_image=self.app.ui_object_images["main_menu_btn_quit_p"],
                                        batch=self._ui_objects_batch,
                                        command=None,
                                        hit_area=None)
            self._btn_quit.x = 1250 * self._screen_sprite.scale_x
            self._btn_quit.y = 300 * self._screen_sprite.scale_y
            self._btn_quit.change_scale(self._screen_sprite.scale_x, self._screen_sprite.scale_y)
            self.ui_objects.append(self._btn_quit)

        # Define the various UI commands
        def btn_new_cmd(source, data):
            x, y, button, modifiers = data
            print("New Game - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["new_game_screen"])

        def btn_load_cmd(source, data):
            x, y, button, modifiers = data
            print("Load Game - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["load_game_screen"])

        def btn_options_cmd(source, data):
            x, y, button, modifiers = data
            print("Options - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["options_screen"])

        def btn_credits_cmd(source, data):
            x, y, button, modifiers = data
            print("Credits - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["credits_screen"])

        def btn_extras_cmd(source, data):
            x, y, button, modifiers = data
            print("Extras - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["extras_screen"])

        def btn_quit_cmd(source, data):
            x, y, button, modifiers = data
            print("Quit - ({0}, {1}) : {2} {3}".format(x, y, button, modifiers))
            self.fire_transition(self.app.game_states["quit_screen"])

        # Ensure the correct instances of the button commands are wired up to their requisite buttons
        self._btn_new.command = btn_new_cmd
        self._btn_load.command = btn_load_cmd
        self._btn_options.command = btn_options_cmd
        self._btn_credits.command = btn_credits_cmd
        self._btn_extras.command = btn_extras_cmd
        self._btn_quit.command = btn_quit_cmd

        # Ensure all handlers for this game state are pushed onto the event stack of the game window
        self.app.game_window.push_handlers(self)
        for obj in self.game_objects:
            self.app.game_window.push_handlers(obj)

        for obj in self.ui_objects:
            self.app.game_window.push_handlers(obj)

    def leave(self, state):
        """
        leave method for the GSMainMenu game state

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
