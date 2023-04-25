"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       game_play_screen_sprite.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Game play screen sprite class
"""

# Imports
from engine.game_sprite import GameSprite


# Consts
# Globals
# Functions


# Classes
class GamePlayScreenSprite(GameSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image.anchor_x = 0
        self.image.anchor_y = 0

    def updater(self, dt):
        super().updater(dt)

    def delete(self):
        super().delete()
