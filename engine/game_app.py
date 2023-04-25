"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       game_app.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Main game application class
"""

# Imports
import shutil
import pyglet
from configparser import ConfigParser
from engine.consts import *
from game_states.gs_splash_screen import GSSplashScreen
from game_states.gs_main_menu import GSMainMenu
from game_states.gs_new_game import GSNewGame
from game_states.gs_load_game import GSLoadGame
from game_states.gs_options import GSOptions
from game_states.gs_credits import GSCredits
from game_states.gs_extras import GSExtras
from game_states.gs_quit_screen import GSQuitScreen
from game_states.gs_game_play import GSGamePlay
from game_states.gs_game_play_menu import GSGamePlayMenu
from game_states.gs_save_game import GSSaveGame


# Consts
# Globals
# Functions


# Classes
class GameApp:
    def __init__(self):
        pyglet.resource.path = [ASSETS_PATH]
        pyglet.resource.reindex()
        self._app_settings = ConfigParser(strict=False)
        self._game_window = None
        self._game_states = {}
        self._current_game_state = None
        self._game_object_images = {}
        self._game_object_audio = {}
        self._ui_object_images = {}
        self._ui_object_audio = {}

    @property
    def settings_defaults(self):
        return "[display]\n" + \
               "id = " + str(DEFAULT_DISPLAY_ID).lower() + "\n" + \
               "width = " + str(DEFAULT_DISPLAY_WIDTH).lower() + "\n" + \
               "height = " + str(DEFAULT_DISPLAY_HEIGHT).lower() + "\n" + \
               "vsync = " + str(DEFAULT_VSYNC).lower() + "\n" + \
               "fullscreen = " + str(DEFAULT_FULLSCREEN).lower() + "\n\n" + \
               "[input]\n\n" + \
               "[key_bindings]\n\n" + \
               "[audio]\n\n" + \
               "[game_play]\n\n"

    @property
    def app_settings(self):
        return self._app_settings

    @property
    def display_id(self):
        return self.app_settings["display"].getint("id")

    @property
    def display_width(self):
        return self.app_settings["display"].getint("width")

    @property
    def display_height(self):
        return self.app_settings["display"].getint("height")

    @property
    def display_vsync(self):
        return self.app_settings["display"].getboolean("vsync")

    @property
    def display_fullscreen(self):
        return self.app_settings["display"].getboolean("fullscreen")

    @property
    def game_window(self):
        return self._game_window

    @property
    def os_user_settings_path(self):
        return self._os_user_settings_path

    @property
    def game_states(self):
        return self._game_states

    @property
    def current_game_state(self):
        return self._current_game_state

    @current_game_state.setter
    def current_game_state(self, value):
        self._current_game_state = value

    @property
    def game_object_images(self):
        return self._game_object_images

    @property
    def game_object_audio(self):
        return self._game_object_audio

    @property
    def ui_object_images(self):
        return self._ui_object_images

    @property
    def ui_object_audio(self):
        return self._ui_object_audio

    def _configure(self):
        os_user_data_path = pyglet.resource.get_settings_path("").replace(os.path.sep, "/")
        os_company_path = os_user_data_path + COMPANY_DIR_NAME
        os_game_name_path = os_company_path + GAME_NAME_DIR_NAME

        if DEBUG:
            self._os_user_settings_path = USER_SETTINGS_PATH
        else:
            self._os_user_settings_path = os_game_name_path + USER_SETTINGS_DIR_NAME

            if not os.path.isdir(os_company_path):
                os.mkdir(os_company_path)

            if not os.path.isdir(os_game_name_path):
                os.mkdir(os_game_name_path)

            if not os.path.isdir(self.os_user_settings_path):
                os.mkdir(self.os_user_settings_path)

        pyglet.resource.path.append(self.os_user_settings_path)
        pyglet.resource.reindex()

        try:
            self._app_settings.read_string(pyglet.resource.text(SETTINGS_FILENAME).text.lower())
        except (KeyError, pyglet.resource.ResourceNotFoundException):
            if not os.path.isfile(DEFAULT_SETTINGS_FILENAME):
                with open(self.os_user_settings_path + SETTINGS_FILENAME, "w") as sf:
                    self._app_settings.read_string(self.settings_defaults)
                    self._app_settings.write(sf)
            else:
                shutil.copy2(DEFAULT_SETTINGS_FILENAME, self.os_user_settings_path + SETTINGS_FILENAME)

            pyglet.resource.reindex()
            self._app_settings.read_string(pyglet.resource.text(SETTINGS_FILENAME).text.lower())

        if not self.app_settings.has_section("display"):
            self.app_settings.add_section("display")

        if not self.app_settings.has_option("display", "id"):
            self.app_settings["display"]["id"] = DEFAULT_DISPLAY_ID

        if not self.app_settings.has_option("display", "width"):
            self.app_settings["display"]["width"] = DEFAULT_DISPLAY_WIDTH

        if not self.app_settings.has_option("display", "height"):
            self.app_settings["display"]["height"] = DEFAULT_DISPLAY_HEIGHT

        if not self.app_settings.has_option("display", "vsync"):
            self.app_settings["display"]["vsync"] = DEFAULT_VSYNC

        if not self.app_settings.has_option("display", "fullscreen"):
            self.app_settings["display"]["fullscreen"] = DEFAULT_FULLSCREEN

        if not self.app_settings.has_section("input"):
            self.app_settings.add_section("input")

        if not self.app_settings.has_section("key_bindings"):
            self.app_settings.add_section("key_bindings")

        if not self.app_settings.has_section("audio"):
            self.app_settings.add_section("audio")

        if not self.app_settings.has_section("game_play"):
            self.app_settings.add_section("game_play")

    def _create_game_window(self):
        self._game_window = pyglet.window.Window(width=self.display_width, height=self.display_height,
                                                 caption=WINDOW_CAPTION,
                                                 resizable=False,
                                                 style=None,
                                                 fullscreen=self.display_fullscreen, visible=True,
                                                 vsync=self.display_vsync,
                                                 display=self.display_id, screen=None,
                                                 config=None, context=None, mode=None)

        # Centre the game window if it is not running full screen
        if not self.game_window.fullscreen:
            screen = pyglet.canvas.get_display().get_default_screen()

            loc_x = (screen.width - self.game_window.width) // 2
            loc_y = (screen.height - self.game_window.height) // 2

            # Ensure that the top left of the game window is within the extents of the monitor display screen
            loc_x = int(screen.width * 0.1) if loc_x < 0 else loc_x
            loc_y = int(screen.height * 0.1) if loc_y < 0 else loc_y

            # Make sure the game window's location ensures that the window caption bar is visible
            self.game_window.set_location(loc_x if loc_x > 10 else 10, loc_y if loc_y > 40 else 40)

        # Note that the colour RGB values are 0.0 -> 1.0 and not 0 -> 255, they need to be mapped accordingly
        pyglet.gl.glClearColor(WINDOW_COLOUR_R / 255, WINDOW_COLOUR_G / 255, WINDOW_COLOUR_B / 255, 1.0)

    def _build_game_states(self):
        # Instantiate game state objects
        game_state = GSSplashScreen("splash_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSMainMenu("main_menu_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSNewGame("new_game_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSLoadGame("load_game_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSOptions("options_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSCredits("credits_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSExtras("extras_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSQuitScreen("quit_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSGamePlay("game_play_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSGamePlayMenu("game_play_menu_screen", self)
        self.game_states[game_state.name] = game_state

        game_state = GSSaveGame("save_game_screen", self)
        self.game_states[game_state.name] = game_state

        # Wire-up game state transitions
        self.game_states["splash_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["main_menu_screen"].add_transition(self.game_states["new_game_screen"])
        self.game_states["new_game_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["new_game_screen"].add_transition(self.game_states["game_play_screen"])
        self.game_states["main_menu_screen"].add_transition(self.game_states["load_game_screen"])
        self.game_states["load_game_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["load_game_screen"].add_transition(self.game_states["game_play_screen"])
        self.game_states["main_menu_screen"].add_transition(self.game_states["options_screen"])
        self.game_states["options_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["main_menu_screen"].add_transition(self.game_states["credits_screen"])
        self.game_states["credits_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["main_menu_screen"].add_transition(self.game_states["extras_screen"])
        self.game_states["extras_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["main_menu_screen"].add_transition(self.game_states["quit_screen"])
        self.game_states["game_play_screen"].add_transition(self.game_states["main_menu_screen"])
        self.game_states["game_play_screen"].add_transition(self.game_states["game_play_menu_screen"])
        self.game_states["game_play_menu_screen"].add_transition(self.game_states["game_play_screen"])
        self.game_states["game_play_menu_screen"].add_transition(self.game_states["save_game_screen"])
        self.game_states["save_game_screen"].add_transition(self.game_states["game_play_menu_screen"])
        self.game_states["game_play_menu_screen"].add_transition(self.game_states["load_game_screen"])
        self.game_states["load_game_screen"].add_transition(self.game_states["game_play_menu_screen"])
        self.game_states["game_play_menu_screen"].add_transition(self.game_states["options_screen"])
        self.game_states["options_screen"].add_transition(self.game_states["game_play_menu_screen"])
        self.game_states["game_play_menu_screen"].add_transition(self.game_states["main_menu_screen"])

    def _load_assets(self):
        # Load game object images
        # Common game state game object images
        self._game_object_images["back_screen"] = pyglet.resource.image(BACK_SCREEN_IMAGE_PATH)

        # Splash screen game state game object images
        self._game_object_images["splash_screen"] = pyglet.resource.image(SPLASH_SCREEN_IMAGE_PATH)

        # Main menu game state game object images
        self._game_object_images["main_menu_screen"] = pyglet.resource.image(MAIN_MENU_IMAGE_PATH)

        # New game screen game state game object images
        self._game_object_images["new_game_screen"] = pyglet.resource.image(NEW_GAME_SCREEN_IMAGE_PATH)

        # Load game screen game state game object images
        self._game_object_images["load_game_screen"] = pyglet.resource.image(LOAD_GAME_SCREEN_IMAGE_PATH)

        # Options screen game state game object images
        self._game_object_images["options_screen"] = pyglet.resource.image(OPTIONS_SCREEN_IMAGE_PATH)

        # Credits screen game state game object images
        self._game_object_images["credits_screen"] = pyglet.resource.image(CREDITS_SCREEN_IMAGE_PATH)

        # Extras screen game state game object images
        self._game_object_images["extras_screen"] = pyglet.resource.image(EXTRAS_SCREEN_IMAGE_PATH)

        # Quit screen game state game object images
        self._game_object_images["quit_screen"] = pyglet.resource.image(QUIT_SCREEN_IMAGE_PATH)

        # Game play screen game state game object images
        self._game_object_images["game_play_screen"] = pyglet.resource.image(GAME_PLAY_SCREEN_IMAGE_PATH)

        # Game play menu screen game state game object images
        self._game_object_images["game_play_menu_mask"] = pyglet.resource.image(GAME_PLAY_MENU_MASK_IMAGE_PATH)
        self._game_object_images["game_play_menu_screen"] = pyglet.resource.image(GAME_PLAY_MENU_SCREEN_IMAGE_PATH)

        # Save game screen game state game object images
        self._game_object_images["save_game_screen"] = pyglet.resource.image(SAVE_GAME_SCREEN_IMAGE_PATH)

        # Game map game object images
        self._game_object_images["game_main_board"] = pyglet.resource.image(GAME_MAIN_BOARD_IMAGE_PATH)

        # Load UI object images
        # Common UI images
        self._ui_object_images["btn_missing"] = pyglet.resource.image(BTN_MISSING_IMAGE_PATH)
        self._ui_object_images["btn_back_d"] = pyglet.resource.image(BTN_BACK_D_IMAGE_PATH)
        self._ui_object_images["btn_back_e"] = pyglet.resource.image(BTN_BACK_E_IMAGE_PATH)
        self._ui_object_images["btn_back_h"] = pyglet.resource.image(BTN_BACK_H_IMAGE_PATH)
        self._ui_object_images["btn_back_p"] = pyglet.resource.image(BTN_BACK_P_IMAGE_PATH)
        self._ui_object_images["btn_start_d"] = pyglet.resource.image(BTN_START_D_IMAGE_PATH)
        self._ui_object_images["btn_start_e"] = pyglet.resource.image(BTN_START_E_IMAGE_PATH)
        self._ui_object_images["btn_start_h"] = pyglet.resource.image(BTN_START_H_IMAGE_PATH)
        self._ui_object_images["btn_start_p"] = pyglet.resource.image(BTN_START_P_IMAGE_PATH)
        self._ui_object_images["btn_confirm_d"] = pyglet.resource.image(BTN_CONFIRM_D_IMAGE_PATH)
        self._ui_object_images["btn_confirm_e"] = pyglet.resource.image(BTN_CONFIRM_E_IMAGE_PATH)
        self._ui_object_images["btn_confirm_h"] = pyglet.resource.image(BTN_CONFIRM_H_IMAGE_PATH)
        self._ui_object_images["btn_confirm_p"] = pyglet.resource.image(BTN_CONFIRM_P_IMAGE_PATH)

        # Main menu game state UI images
        self._ui_object_images["main_menu_btn_new_d"] = pyglet.resource.image(MAIN_MENU_BTN_NEW_D_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_new_e"] = pyglet.resource.image(MAIN_MENU_BTN_NEW_E_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_new_h"] = pyglet.resource.image(MAIN_MENU_BTN_NEW_H_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_new_p"] = pyglet.resource.image(MAIN_MENU_BTN_NEW_P_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_load_d"] = pyglet.resource.image(MAIN_MENU_BTN_LOAD_D_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_load_e"] = pyglet.resource.image(MAIN_MENU_BTN_LOAD_E_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_load_h"] = pyglet.resource.image(MAIN_MENU_BTN_LOAD_H_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_load_p"] = pyglet.resource.image(MAIN_MENU_BTN_LOAD_P_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_options_d"] = pyglet.resource.image(MAIN_MENU_BTN_OPTIONS_D_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_options_e"] = pyglet.resource.image(MAIN_MENU_BTN_OPTIONS_E_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_options_h"] = pyglet.resource.image(MAIN_MENU_BTN_OPTIONS_H_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_options_p"] = pyglet.resource.image(MAIN_MENU_BTN_OPTIONS_P_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_credits_d"] = pyglet.resource.image(MAIN_MENU_BTN_CREDITS_D_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_credits_e"] = pyglet.resource.image(MAIN_MENU_BTN_CREDITS_E_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_credits_h"] = pyglet.resource.image(MAIN_MENU_BTN_CREDITS_H_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_credits_p"] = pyglet.resource.image(MAIN_MENU_BTN_CREDITS_P_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_extras_d"] = pyglet.resource.image(MAIN_MENU_BTN_EXTRAS_D_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_extras_e"] = pyglet.resource.image(MAIN_MENU_BTN_EXTRAS_E_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_extras_h"] = pyglet.resource.image(MAIN_MENU_BTN_EXTRAS_H_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_extras_p"] = pyglet.resource.image(MAIN_MENU_BTN_EXTRAS_P_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_quit_d"] = pyglet.resource.image(MAIN_MENU_BTN_QUIT_D_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_quit_e"] = pyglet.resource.image(MAIN_MENU_BTN_QUIT_E_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_quit_h"] = pyglet.resource.image(MAIN_MENU_BTN_QUIT_H_IMAGE_PATH)
        self._ui_object_images["main_menu_btn_quit_p"] = pyglet.resource.image(MAIN_MENU_BTN_QUIT_P_IMAGE_PATH)

        # Game play menu game state UI images
        self._ui_object_images["game_play_menu_btn_resume_d"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_RESUME_D_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_resume_e"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_RESUME_E_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_resume_h"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_RESUME_H_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_resume_p"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_RESUME_P_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_save_d"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_SAVE_D_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_save_e"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_SAVE_E_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_save_h"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_SAVE_H_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_save_p"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_SAVE_P_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_load_d"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_LOAD_D_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_load_e"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_LOAD_E_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_load_h"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_LOAD_H_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_load_p"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_LOAD_P_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_options_d"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_OPTIONS_D_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_options_e"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_OPTIONS_E_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_options_h"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_OPTIONS_H_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_options_p"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_OPTIONS_P_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_main_d"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_MAIN_D_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_main_e"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_MAIN_E_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_main_h"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_MAIN_H_IMAGE_PATH)
        self._ui_object_images["game_play_menu_btn_main_p"] = pyglet.resource.image(
            GAME_PLAY_MENU_BTN_MAIN_P_IMAGE_PATH)

    def run(self):
        self._configure()
        self._create_game_window()
        self._build_game_states()
        self._load_assets()

        @self.game_window.event
        def on_key_press(symbol, modifiers):
            # If running in window then disable any escaped ESC key press as this will force close on the game window
            if not self.game_window.fullscreen:
                return pyglet.event.EVENT_HANDLED

        @self.game_window.event
        def on_draw():
            self.current_game_state.draw(self.game_window)

        @self.game_window.event
        def on_close():
            with open(self.os_user_settings_path + SETTINGS_FILENAME, "w") as sf:
                self._app_settings.write(sf)

        def update(dt):
            self.current_game_state.update(dt)

        # Launch into loading game state
        self.current_game_state = self.game_states["splash_screen"]
        self.current_game_state.enter(state=None)

        pyglet.clock.schedule_interval(update, 1 / 120.0)
        pyglet.app.run()
