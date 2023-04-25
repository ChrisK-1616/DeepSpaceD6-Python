"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       threat_deck.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Class that represents a 'deck' of threat cards (with available, discarded and destroyed lists of cards)
"""

# Imports
import json
from data_model.threats import Threat, ExternalThreat, InternalThreat
from data_model.rng import RNG


# Consts
# Globals
# Functions


# Classes
class ThreatDeck(RNG):
    def __init__(self, cards_file, reproducible=False, seed=None):
        super().__init__(reproducible=reproducible, seed=seed)

        self.__all_cards = []

        with open(cards_file) as json_file:
            cards = json.load(json_file)
            self.__populate_threats(cards)
            self.__populate_external_threats(cards)
            self.__populate_internal_threats(cards)

        self.__available_cards = []
        self.__discarded_cards = []
        self.__destroyed_cards = []

    @property
    def all_cards(self):
        return self.__all_cards

    @property
    def available_cards(self):
        return self.__available_cards

    @property
    def discarded_cards(self):
        return self.__discarded_cards

    @property
    def destroyed_cards(self):
        return self.__destroyed_cards

    def __populate_threats(self, cards):
        for card in cards["Threats"]:
            al = []
            for av in card["activation_list"]:
                al.append(av["activation_value"])

            self.__all_cards.append(Threat(name=card["name"],
                                           effect_text=card["effect_text"],
                                           activation_list=al,
                                           away_missions=card["away_missions"]))

    def __populate_external_threats(self, cards):
        for card in cards["ExternalThreats"]:
            al = []
            for av in card["activation_list"]:
                al.append(av["activation_value"])

            self.__all_cards.append(ExternalThreat(name=card["name"],
                                                   effect_text=card["effect_text"],
                                                   starting_health=card["starting_health"],
                                                   activation_list=al,
                                                   away_missions=card["away_missions"]))

    def __populate_internal_threats(self, cards):
        for card in cards["InternalThreats"]:
            al = []
            for av in card["activation_list"]:
                al.append(av["activation_value"])

            self.__all_cards.append(InternalThreat(name=card["name"],
                                                   effect_text=card["effect_text"],
                                                   activation_list=al,
                                                   away_missions=card["away_missions"]))

    def reset_deck(self):
        """
        Creates an available cards list with all cards including those that were destroyed
        :return: None
        """
        self.__available_cards = self.all_cards.copy()
        self.__discarded_cards.clear()
        self.__destroyed_cards.clear()

    def reform_deck(self):
        """
        Creates an available cards list with all cards except those that are destroyed
        :return: None
        """
        self.__available_cards = self.all_cards.copy()
        self.__discarded_cards.clear()

        for card in self.destroyed_cards:
            if card in self.available_cards:
                self.available_cards.remove(card)

    def shuffle_deck(self, use_reproducible=False):
        """
        The use_reproducible parameter determines if a reproducible rng used by the threat deck
        is activated or ignored (False - ignore, True - activate), this will allow multiple
        shuffles of the same order starting available cards to be shuffled in exactly the same
        way
        :param use_reproducible: boolean
        :return: None
        """
        if self.reproducible and use_reproducible:
            self._reset_rng()

        self._rng.shuffle(x=self.available_cards)

    def draw_card(self):
        """
        Pops the top card from the available cards list if there is one - otherwise returns
        a None
        :return: Threat
        """
        if len(self.available_cards) > 0:
            return self.available_cards.pop(0)

        return None

    def discard_card(self, card):
        if card in self.available_cards:
            self.available_cards.remove(card)

        if card not in self.discarded_cards:
            self.discarded_cards.append(card)

    def destroy_card(self, card):
        if card in self.available_cards:
            self.available_cards.remove(card)

        if card in self.discarded_cards:
            self.discarded_cards.remove(card)

        if card not in self.destroyed_cards:
            self.destroyed_cards.append(card)
