"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       rng.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Either a reproducible or non-reproducible random number generator (RNG)
"""

# Imports
import random


# Consts
# Globals
# Functions


# Classes
class RNG:
    def __init__(self, reproducible=False, seed=None):
        self.__reproducible = reproducible

        if reproducible:
            if seed:
                self.__seed = seed
            else:
                import time
                self.__seed = time.time_ns()

            self._rng = random.Random(seed)

            # Store the initial state of the RNG so it can be reset back to this state
            # when required by reproducible RNGs
            self.__initial_state = self._rng.getstate()
        else:
            self.__seed = None
            self._rng = random.SystemRandom()

    @property
    def reproducible(self):
        return self.__reproducible

    @property
    def seed(self):
        return self.__seed

    def _reset_rng(self):
        """
        Use this to reset the RNG back to its initial state, note - this only works for
        reproducible RNGs, if not reproducible then it is ignored (as a non-reproducible
        RNG cannot be returned to initial state)
        :return: None
        """
        if self.reproducible:
            self._rng.setstate(self.__initial_state)
