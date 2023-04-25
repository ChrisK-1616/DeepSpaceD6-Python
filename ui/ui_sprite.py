"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       ui_sprite.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - User interface (UI) sprite class
"""

# Imports
import pyglet
from shapely.geometry import Point, Polygon
from engine.game_sprite import GameSprite


# Consts
# Globals
# Functions


# Classes
class UISprite(GameSprite):
    def __init__(self, enabled=True, hit_area=None, *args, **kwargs):
        """
        Initialiser for the UISprite class

        :attr _enabled: boolean flag to state if this UI sprite is enabled or not, usually being enabled means that this
                        UI widget actually does something in the overall UI (determined by the derived classes of this
                        abstract UI sprite), NOTE: this will trigger the event on_enabled_changed() if the value of this
                        property changes

        :attr _hit_area: list of (x, y) coordinates that determines a "hittable" area for this UI sprite as it is
                         located within its container, for instance, this can be used to (in conjunction with the
                         mouse_inside property) establish if a mouse button event has occurred "inside" this UI widget,
                         NOTE: these coordinates will be converted to a shapely.geometry.Polygon when applying
                         any hit test

        :attr _mouse_inside: a boolean flag that shows if the current mouse position is determined to be "inside" this
                             UI sprite as it is located within its container and scaled accordingly, NOTE: this is
                             determined whenever the mouse is moved across this UI sprite and will trigger the events
                             on_mouse_entered() and on_mouse_left() accordingly

        :param enabled: initial enabled state of the UI sprite as a boolean
        :param hit_area: initial hit area of this UI sprite as a list of (x, y) position tuples that are relative to the
                         bounds of this UI sprite, the last entry in the list will become the "closing" coordinate, ie.
                         it must be the same as the first coordinate, NOTE: if None is provided then the hit area is
                         assumed to be an area that conforms to the bounds of the UI sprite
        """
        super().__init__(*args, **kwargs)
        self.key_handler = pyglet.window.key.KeyStateHandler()
        self._enabled = enabled
        self._mouse_inside = False

        # If no hit area provided then assume a rectangular, ie. box, hit area based on size of the UI sprite
        if not hit_area:
            self._hit_area = [(0, 0), (0, self.height - 1), (self.width - 1, self.height - 1), (self.width - 1, 0),
                              (0, 0)]
        else:
            self._hit_area = hit_area

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if not value == self.enabled:
            old_value = self.enabled
            self._enabled = value
            self.on_enabled_changed(old_value)

    def on_enabled_changed(self, old_value):
        pass

    @property
    def hit_area(self):
        return self._hit_area

    @hit_area.setter
    def hit_area(self, value):
        self._hit_area = value

    @property
    def mouse_inside(self):
        return self._mouse_inside

    def change_scale(self, scale_x, scale_y):
        """
        Use this mthod to rescale any UI widget so that its hit area is scaled accordingly

        :param scale_x: new scale for along x-axis as float number
        :param scale_y: new scale along y_axis as float number

        :return: nothing
        """
        self.scale_x = scale_x
        self.scale_y = scale_y

        new_hit_area = []

        for coord in self.hit_area:
            new_hit_area.append((coord[0] * self.scale_x, coord[1] * self.scale_y))

        self.hit_area = new_hit_area

    def establish_mouse_inside(self, x, y):
        # Transform the x,y position of the mouse to take into account the location of the sprite in its containing
        # window and any scaling that needs to be applied
        transformed_x = x - self.x
        transformed_y = y - self.y
        p = Polygon(self.hit_area)
        return p.contains(Point(transformed_x, transformed_y))

    def updater(self, dt):
        super().updater(dt)

    def on_mouse_motion(self, x, y,    dx, dy):
        # Only react to mouse motion if enabled
        if self.enabled:
            within_hit_area = self.establish_mouse_inside(x, y)

            if not self.mouse_inside and within_hit_area:
                self._mouse_inside = True
                self.on_mouse_entered()
                return pyglet.event.EVENT_HANDLED

            if self.mouse_inside and not within_hit_area:
                self._mouse_inside = False
                self.on_mouse_left()
                return pyglet.event.EVENT_HANDLED

            if within_hit_area:
                return pyglet.event.EVENT_HANDLED

    def on_mouse_entered(self):
        pass

    def on_mouse_left(self):
        pass
