from engine.consts import *
from data_model.die import Die
from data_model.threat_deck import ThreatDeck
from data_model.ship import Ship


def print_list(title, underline, lst):
    print(title)
    print(underline)

    if len(lst) > 0:
        count = 1
        for card in lst:
            print("{0:03}: {1}".format(count, card))
            count += 1
    else:
        print("000: Empty")

    print()


def main():
    ship = Ship(ship_file="assets/data/halcyon.json")
    print(ship)
    print()

    threat_deck = ThreatDeck(cards_file=GAME_THREAT_CARDS_DATA_PATH, reproducible=True)
    threat_deck.reset_deck()

    print_list(title="All Cards (Full - {0} card(s))".format(len(threat_deck.all_cards)),
               underline="=" * 72,
               lst=threat_deck.all_cards)

    threat_die = Die(name="Threat-Die", sides=6,
                     faces=["One", "Two", "Three", "Four", "Five", "Six"],
                     reproducible=False)
    crew_die = Die(name="Crew-Die", sides=6,
                   faces=["Commander", "Tactical", "Medical", "Science", "Engineering", "Threat-Detected"],
                   reproducible=False)

    rolls = threat_die.roll()
    faces = [threat_die.face_at_side(threat_die.last_roll)]

    for _ in range (10):
        rolls = ("{0}, {1}".format(rolls, threat_die.roll()))
        faces.append(threat_die.face_at_side(threat_die.last_roll))

    #print("{0} rolled {1}".format(threat_die, rolls))
    #print(faces)

    rolls = crew_die.roll()
    faces = [crew_die.face_at_side(crew_die.last_roll)]

    for _ in range (10):
        rolls = ("{0}, {1}".format(rolls, crew_die.roll()))
        faces.append(crew_die.face_at_side(crew_die.last_roll))

    #print("{0} rolled {1}".format(crew_die, rolls))
    #print(faces)

    print("Shuffle deck - first shuffle")
    threat_deck.shuffle_deck(use_reproducible=True)

    print_list(title="Available Cards (Full - {0} card(s))".format(len(threat_deck.available_cards)),
               underline="=" * 72,
               lst=threat_deck.available_cards)

    print("Shuffle deck - should be in same order as previous list")
    threat_deck.reset_deck()
    threat_deck.shuffle_deck(use_reproducible=True)

    print_list(title="Available Cards (Full - {0} card(s))".format(len(threat_deck.available_cards)),
               underline="=" * 72,
               lst=threat_deck.available_cards)

    print("Shuffle deck - should be in different order from previous list")
    threat_deck.reset_deck()
    threat_deck.shuffle_deck()

    print_list(title="Available Cards (Full - {0} card(s))".format(len(threat_deck.available_cards)),
               underline="=" * 72,
               lst=threat_deck.available_cards)

    print("Draw 2 cards - remove top two cards from previous list")
    drawn_card_0 = threat_deck.draw_card()
    drawn_card_1 = threat_deck.draw_card()
    print(drawn_card_0)
    print(drawn_card_1)
    print()

    print_list(title="Available Cards (Partial - {0} card(s))".format(len(threat_deck.available_cards)),
               underline="=" * 72,
               lst=threat_deck.available_cards)

    print_list(title="Discarded Cards (Empty - {0} card(s))".format(len(threat_deck.discarded_cards)),
               underline="=" * 72,
               lst=threat_deck.discarded_cards)

    print("Discard back to the threat deck the first card that was drawn from the threat deck")
    threat_deck.discard_card(drawn_card_0)

    print_list(title="Discarded Cards (Partial - {0} card(s))".format(len(threat_deck.discarded_cards)),
               underline="=" * 72,
               lst=threat_deck.discarded_cards)

    print_list(title="Destroyed Cards (Empty - {0} card(s))".format(len(threat_deck.destroyed_cards)),
               underline="=" * 72,
               lst=threat_deck.destroyed_cards)

    print("Destroy from the threat deck the second card that was drawn from the threat deck")
    threat_deck.destroy_card(drawn_card_1)

    print_list(title="Destroyed Cards (Empty - {0} card(s))".format(len(threat_deck.destroyed_cards)),
               underline="=" * 72,
               lst=threat_deck.destroyed_cards)

    print()

    # print("Discard 1000004")
    # card = threat_deck.all_cards[4]
    # threat_deck.discard_card(card=card)
    #
    # print("All Cards (Full)")
    # print("===========================")
    # for card in threat_deck.all_cards:
    #     print(card)
    # print()
    #
    # print("Available Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.available_cards:
    #     print(card)
    # print()
    #
    # print("Discarded Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.discarded_cards:
    #     print(card)
    # print()
    #
    # print("Destroyed Cards (Empty)")
    # print("===========================")
    # for card in threat_deck.destroyed_cards:
    #     print(card)
    # print()
    # print()
    #
    # print("Destroy 1000002")
    # card = threat_deck.all_cards[2]
    # threat_deck.destroy_card(card=card)
    #
    # print("All Cards (Full)")
    # print("===========================")
    # for card in threat_deck.all_cards:
    #     print(card)
    # print()
    #
    # print("Available Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.available_cards:
    #     print(card)
    # print()
    #
    # print("Discarded Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.discarded_cards:
    #     print(card)
    # print()
    #
    # print("Destroyed Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.destroyed_cards:
    #     print(card)
    # print()
    # print()
    #
    # print("Reform Deck")
    # threat_deck.reform_deck()
    #
    # print("All Cards (Full)")
    # print("===========================")
    # for card in threat_deck.all_cards:
    #     print(card)
    # print()
    #
    # print("Available Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.available_cards:
    #     print(card)
    # print()
    #
    # print("Discarded Cards (Empty)")
    # print("===========================")
    # for card in threat_deck.discarded_cards:
    #     print(card)
    # print()
    #
    # print("Destroyed Cards (Partial)")
    # print("===========================")
    # for card in threat_deck.destroyed_cards:
    #     print(card)
    # print()
    # print()
    #
    # print("Shuffle Deck")
    # print("Available Cards (Before)")
    # print("===========================")
    # for card in threat_deck.available_cards:
    #     print(card)
    # print()
    #
    # threat_deck.shuffle_deck()
    #
    # print("Available Cards (After)")
    # print("===========================")
    # for card in threat_deck.available_cards:
    #     print(card)
    # print()
    # print()

    # print("===========================================================")
    #
    # print("Ship Infirmary Count (No crew moved to Infirmary)")
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (One crew moved to Infirmary)")
    # ship.move_crew_to_infirmary()
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Six crew moved to Infirmary)")
    # ship.move_crew_to_infirmary(amount=5)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Eight crew moved to Infirmary)")
    # ship.move_crew_to_infirmary(amount=2)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Two crew moved from Infirmary)")
    # ship.move_crew_from_infirmary(amount=2)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Seven crew moved from Infirmary)")
    # ship.move_crew_from_infirmary(amount=5)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Eight crew moved from Infirmary)")
    # ship.move_crew_from_infirmary(amount=1)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Eight crew moved to Infirmary)")
    # ship.move_crew_to_infirmary(amount=8)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Nine crew moved from Infirmary)")
    # ship.move_crew_from_infirmary(amount=9)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Negative Nine crew moved from Infirmary)")
    # ship.move_crew_from_infirmary(amount=-9)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Negative Seven crew moved to Infirmary)")
    # ship.move_crew_from_infirmary(amount=-7)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Six crew moved to Infirmary)")
    # ship.move_crew_to_infirmary(amount=6)
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")
    #
    # print("Ship Infirmary Count (Infirmary cleared)")
    # ship.clear_infirmary()
    # print("Available Crew : {0}".format(ship.available_crew))
    # print("Infirmary Count: {0}".format(ship.infirmary_count))
    # print("-----------------------------------------------------------")


if __name__ == "__main__":
    main()
