"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       threats.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Classes for the various threat cards in the game
"""

# Imports
from data_model.identified_entity import IdentifiedEntity


# Consts
# Globals
# Functions


# Classes
class Threat(IdentifiedEntity):
    def __init__(self, name, effect_text, activation_list, away_missions):
        super().__init__()
        self.__name = name
        self.__effect_text = effect_text
        self.__activation_list = activation_list
        self.__away_missions = away_missions

    @property
    def name(self):
        return self.__name

    @property
    def effect_text(self):
        return self.__effect_text

    @property
    def activation_list(self):
        return self.__activation_list

    @property
    def away_missions(self):
        return self.__away_missions

    def __str__(self):
        s = "Threat-{0}> [{1}] [{2}] {3} {4}"
        return s.format(self.uid, self.name, self.effect_text, self.activation_list, self.away_missions)


class ExternalThreat(Threat):
    def __init__(self, name, effect_text, activation_list, away_missions, starting_health):
        super().__init__(name=name, effect_text=effect_text, activation_list=activation_list,
                         away_missions=away_missions)
        self.__starting_health = starting_health
        self.__health = self.starting_health

        # Flags if this external threat uses health or not, for instance the Solar-Winds external
        # threat does not use health whilst all other external threats do use health
        self.__uses_health = (self.starting_health > 0)

    @property
    def uses_health(self):
        return self.__uses_health

    @property
    def starting_health(self):
        return self.__starting_health

    @property
    def health(self):
        return self.__health

    def inc_health(self, delta):
        self.__health += delta
        self.__health = min(self.starting_health, self.health)

    def dec_health(self, delta):
        self.__health -= delta
        self.__health = max(0, self.health)

    def __str__(self):
        s = "External-Threat-{0}> [{1}] [{2}] [{3}] {4} {5}"
        return s.format(self.uid, self.name, self.effect_text, self.starting_health, self.activation_list,
                        self.away_missions)


class InternalThreat(Threat):
    def __init__(self, name, effect_text, activation_list, away_missions):
        super().__init__(name, effect_text, activation_list=activation_list, away_missions=away_missions)

    def __str__(self):
        s = "Internal-Threat-{0}> [{1}] [{2}] {3} {4}"
        return s.format(self.uid, self.name, self.effect_text, self.activation_list, self.away_missions)
