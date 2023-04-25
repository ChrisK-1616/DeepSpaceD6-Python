"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       identified_entity.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Abstract class for any uniquely identified entity in the application
"""

# Imports
# Consts
# Globals
# Functions


# Classes
class IdentifiedEntity:
    _next_uid = 1000000000

    @staticmethod
    def get_next_uid():
        """
        Static method to establish and return the next allocated unique identifier, also advances the unique
        identifier value by a single step

        :return next_uid: next identifier to be allocated is returned
        """
        # Next identifier to be allocated
        next_uid = IdentifiedEntity._next_uid

        # Increment the _next_uid static attribute
        IdentifiedEntity._next_uid += 1

        return next_uid

    def __init__(self):
        """
        Initialiser that allocates a new identifier using the get_next_uid() static method

        :attr _uid: unique application wide identifier for this object
        """
        self._uid = IdentifiedEntity.get_next_uid()

    @property
    def uid(self):
        return self._uid
