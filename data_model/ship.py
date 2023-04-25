"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       ship.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Class for the Ship related data and functions of the game
"""

# Imports
import json
from data_model.identified_entity import IdentifiedEntity


# Consts
# Globals
# Functions


# Classes
class Ship(IdentifiedEntity):
    def __init__(self, ship_file):
        with open(ship_file) as json_file:
            ship = json.load(json_file)
            self.__name = ship["name"]
            self.__complement = ship["complement"]
            self.__available_crew = self.complement
            self.__full_shield_points = ship["shield_points"]
            self.__shield_points = self.full_shield_points
            self.__full_hull_points = ship["hull_points"]
            self.__hull_points = self.full_hull_points

        self.__external_threats = []
        self.__internal_threats = []
        self.__threats_detected = 0
        self.__infirmary_count = 0

    @property
    def name(self):
        return self.__name

    @property
    def complement(self):
        return self.__complement

    @property
    def full_shield_points(self):
        return self.__full_shield_points

    @property
    def shield_points(self):
        return self.__shield_points

    @property
    def full_hull_points(self):
        return self.__full_hull_points

    @property
    def hull_points(self):
        return self.__hull_points

    @property
    def external_threats(self):
        return self.__external_threats

    @property
    def internal_threats(self):
        return self.__internal_threats

    @property
    def threats_detected(self):
        return self.__threats_detected

    @property
    def infirmary_count(self):
        return self.__infirmary_count

    @property
    def available_crew(self):
        return self.__available_crew

    def move_crew_to_infirmary(self, amount=1):
        if amount < 0:
            amount = 0
        elif amount > self.available_crew:
            amount = self.available_crew

        self.__available_crew -= amount
        self.__infirmary_count += amount

    def move_crew_from_infirmary(self, amount=1):
        if amount < 0:
            amount = 0
        elif amount > self.infirmary_count:
            amount = self.infirmary_count

        self.__infirmary_count -= amount
        self.__available_crew += amount

    def clear_infirmary(self):
        self.__infirmary_count = 0
        self.__available_crew = self.complement

    def add_threats_detected(self, amount=1):
        if amount < 0:
            amount = 0

        self.__threats_detected += amount

    def remove_threats_detected(self, amount=1):
        if amount < 0:
            amount = 0

        self.__threats_detected -= amount

    def clear_threats_detected(self):
        self.__threats_detected = 0

    def __str__(self):
        return "Ship: {0} has {1} Crew, {2} Shield Points and {3} Hull Points".format(self.name,
                                                                                      self.complement,
                                                                                      self.shield_points,
                                                                                      self.hull_points)
