"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       game_main_board_sprite.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game main board sprite class
"""

# Imports
import pyglet
from engine.consts import *
from engine.game_sprite import GameSprite


# Consts
# Globals
# Functions


# Classes
class GameMainBoardSprite(GameSprite):
    def __init__(self, game_play_state, game_board_images, *args, **kwargs):
        """
        Initialiser for the GameMainBoardSprite class

        :attr _current_image_index: current index into the game board images list, ie. currently active game board image
        :attr _decorated_image_index: index into the game board images list of the current decorated game board image
        :attr _game_play_state: the game play state that contains this game board sprite
        :attr _game_board_images: list of images for the game board such that:-
                                    index 0 is main board

        :param game_play_state: game play state that contains this game main board sprite
        :param game_board_images: list of images for the game main board
        """
        self._decorated_image_index = 0
        self._current_image_index = self._decorated_image_index
        super().__init__(img=game_board_images[self._current_image_index], *args, **kwargs)
        self._game_play_state = game_play_state
        self._game_board_images = game_board_images
        self.image.anchor_x = 0
        self.image.anchor_y = 0

    @property
    def game_play_state(self):
        return self._game_play_state

    @property
    def unscaled_width(self):
        return self.width / self.scale

    @property
    def unscaled_height(self):
        return self.height / self.scale

    def reinitialise(self):
        self._decorated_image_index = 0
        self._current_image_index = self._decorated_image_index
        self.image = self._game_board_images[self._current_image_index]
        self.update(x=0, y=0, scale=1.0)

    def updater(self, dt):
        super().updater(dt)

    def on_key_press(self, symbol, modifiers):
        for obj in self.game_play_state.ui_objects:
            if obj.active and obj.enabled and obj.mouse_inside:
                return pyglet.event.EVENT_UNHANDLED

        if symbol == pyglet.window.key.ESCAPE:
            self.game_play_state._screen_capture = pyglet.image.get_buffer_manager().get_color_buffer()
            self.game_play_state.fire_transition(self.game_play_state.app.game_states["game_play_menu_screen"])
            return pyglet.event.EVENT_HANDLED

        # if symbol == pyglet.window.key.H:
        #     self._current_image_index = self._decorated_image_index if self._current_image_index == 0 else 0
        #     self.image = self._game_board_images[self._current_image_index]
        #     return pyglet.event.EVENT_HANDLED
        #
        # if symbol == pyglet.window.key.G:
        #     self._decorated_image_index += 1
        #     if self._decorated_image_index == len(self._game_board_images):
        #         self._decorated_image_index = 1
        #     self._current_image_index = self._decorated_image_index
        #     self.image = self._game_board_images[self._current_image_index]
        #     return pyglet.event.EVENT_HANDLED

    def on_text_motion(self, motion):
        for obj in self.game_play_state.ui_objects:
            if obj.active and obj.enabled and obj.mouse_inside:
                return pyglet.event.EVENT_UNHANDLED

        if motion == pyglet.window.key.MOTION_UP:
            if not self.height < self.window.height:
                self.y += 41
                self._constrain_y()
            return pyglet.event.EVENT_HANDLED

        if motion == pyglet.window.key.MOTION_DOWN:
            if not self.height < self.window.height:
                self.y -= 41
                self._constrain_y()
            return pyglet.event.EVENT_HANDLED

        if motion == pyglet.window.key.MOTION_RIGHT:
            if not self.width < self.window.width:
                self.x += 27
                self._constrain_x()
            return pyglet.event.EVENT_HANDLED

        if motion == pyglet.window.key.MOTION_LEFT:
            if not self.width < self.window.width:
                self.x -= 27
                self._constrain_x()
            return pyglet.event.EVENT_HANDLED

    def on_mouse_press(self, x, y, button, modifiers):
        for obj in self.game_play_state.ui_objects:
            if obj.active and obj.enabled and obj.mouse_inside:
                return pyglet.event.EVENT_UNHANDLED

        if not button == pyglet.window.mouse.MIDDLE:
            return pyglet.event.EVENT_UNHANDLED

        self.game_play_state._screen_capture = pyglet.image.get_buffer_manager().get_color_buffer()
        self.game_play_state.fire_transition(self.game_play_state.app.game_states["game_play_menu_screen"])
        return pyglet.event.EVENT_HANDLED

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for obj in self.game_play_state.ui_objects:
            if obj.active and obj.enabled and obj.mouse_inside:
                return pyglet.event.EVENT_UNHANDLED

        if buttons & pyglet.window.mouse.LEFT:
            if not self.width < self.window.width:
                self.x += dx
                self._constrain_x()

            if not self.height < self.window.height:
                self.y += dy
                self._constrain_y()

            return pyglet.event.EVENT_HANDLED

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for obj in self.game_play_state.ui_objects:
            if obj.active and obj.enabled and obj.mouse_inside:
                return pyglet.event.EVENT_UNHANDLED

        if scroll_y:
            if scroll_y > 0:
                if self.scale < 2.0:
                    self.scale += 0.1
            else:
                if self.scale > 0.5:
                    self.scale -= 0.1

            if self.width < self.window.width:
                self.x = 0
            else:
                self._constrain_x()

            if self.height < self.window.height:
                self.y = 0
            else:
                self._constrain_y()

        # :DEV: #
        # Display some debug info on the window caption (if not full screen)
        if not self.game_play_state.app.game_window.fullscreen:
            obj = self.game_play_state.app.game_window
            obj.set_caption("{0}   {1} [mouse:({2}, {3}) scale:{4:.2f}"
                            "  offset:({5}, {6})]".format(WINDOW_CAPTION, self.game_play_state.name, x, y, self.scale,
                                                          self.x, self.y))
        # :DEV: #

        return pyglet.event.EVENT_HANDLED

    def _constrain_x(self):
        if self.x < (self.window.width - self.width):
            self.x = self.window.width - self.width
        elif self.x > 0:
            self.x = 0

    def _constrain_y(self):
        if self.y < (self.window.height - self.height):
            self.y = self.window.height - self.height
        elif self.y > 0:
            self.y = 0

    def _constrain_xy(self):
        self._constrain_x()
        self._constrain_y()
