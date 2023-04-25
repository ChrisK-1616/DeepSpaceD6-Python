"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       die.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Represents a n-sided die that can be 'rolled' and produce a random value
"""

# Imports
from data_model.rng import RNG


# Consts
# Globals
# Functions


# Classes
class Die(RNG):
    def __init__(self, name, sides, faces=[], reproducible=False, seed=None):
        super().__init__(reproducible=reproducible, seed=seed)

        self.__name = name
        self.__sides = sides
        self.__faces = faces
        self.__last_roll = None

    @property
    def name(self):
        return self.__name

    @property
    def sides(self):
        return self.__sides

    @property
    def faces(self):
        return self.__faces

    @property
    def last_roll(self):
        return self.__last_roll

    def roll(self):
        if self.sides < 1:
            self.__last_roll = 1
        else:
            self.__last_roll = self._rng.randint(a=1, b=self.sides)

        return self.last_roll

    def face_at_side(self, side):
        if (side > 0) and (side <= self.sides) and (len(self.faces) >= side):
            return self.faces[side - 1]

        return None

    def __str__(self):
        rstr = "reproducible" if self.reproducible else "not reproducible"
        sstr = " with seed {0}".format(str(self.seed)) if self.reproducible else ""
        return "{0} sided {1} that is {2}{3}".format(self.sides, self.name, rstr, sstr)
