from typing import List

from utils import read_input_batch


def normal_combat(player_1: List[int], player_2: List[int]):
    # Create copy of decks
    player_1 = [card for card in player_1]
    player_2 = [card for card in player_2]
    while player_1 and player_2:
        card_1 = player_1.pop()
        card_2 = player_2.pop()
        if card_1 > card_2:
            player_1 = [card_2, card_1] + player_1
        else:
            player_2 = [card_1, card_2] + player_2

    winner = len(player_1) > len(player_2)
    winning_deck = player_1 if winner else player_2

    return winner, winning_deck


def recursive_combat(player_1: List[int], player_2: List[int]):
    # Create copy of decks
    player_1 = [card for card in player_1]
    player_2 = [card for card in player_2]

    deck_configurations = set()
    while player_1 and player_2:
        # Check if configuration has been already played
        if (tuple(player_1), tuple(player_2)) in deck_configurations:
            return 1, player_1
        else:
            deck_configurations.add((tuple(player_1), tuple(player_2)))
        # Deal cards
        card_1 = player_1.pop()
        card_2 = player_2.pop()
        # If possible, play another round of recursive combat
        if (len(player_1) >= card_1) & (len(player_2) >= card_2):
            winner, _ = recursive_combat(player_1[-card_1:], player_2[-card_2:])
        # Otherwise, the winner is the person with the highest card
        else:
            winner = card_1 > card_2

        if winner:
            player_1 = [card_2, card_1] + player_1
        else:
            player_2 = [card_1, card_2] + player_2

    winning_deck = player_1 if winner else player_2
    return winner, winning_deck


def main():
    input_file = read_input_batch("2020/22/input.txt", line_split=False)
    player_1 = list(reversed([int(card) for card in input_file[0][1:]]))
    player_2 = list(reversed([int(card) for card in input_file[1][1:]]))
    _, winning_deck = normal_combat(player_1, player_2)
    score = sum(
        [
            card * value
            for card, value in zip(range(1, len(winning_deck) + 1), winning_deck)
        ]
    )

    print(f"Result of part 1: {score}")

    _, winning_deck = recursive_combat(player_1, player_2)
    score = sum(
        [
            card * value
            for card, value in zip(range(1, len(winning_deck) + 1), winning_deck)
        ]
    )

    print(f"Result of part 2: {score}")


if __name__ == "__main__":
    main()
