from utils import read_input
from typing import List, Set, Dict, Tuple
import re
import numpy as np


def format_cards(cards: List[str]) -> Dict[int, Tuple[Set[int], Set[int]]]:
    """Format input cards into a dictionary {id: (win_cards, my_cards)}"""
    cards_dict = {}
    for card in cards:
        id_tag, number_tag = card.split(": ")
        if (x := re.search(r"\d+", id_tag)) is not None:
            card_id = int(x.group(0))
        win_n, my_n = (
            set(map(int, re.findall(r"\d+", nums))) for nums in number_tag.split(" | ")
        )
        cards_dict[card_id] = (win_n, my_n)
    return cards_dict


def main():
    cards = format_cards(read_input("2023/04/input.txt"))
    # Create tracking arrays
    points_cards = np.zeros(shape=(len(cards)), dtype=int)
    counter_cards = np.ones(shape=(len(cards)), dtype=int)

    for id, (win_cards, my_cards) in cards.items():
        n_wins = len(win_cards & my_cards)
        points_cards[id - 1] = int(2 ** (n_wins - 1))
        counter_cards[id : id + n_wins] += 1 * counter_cards[id - 1]  # noqa: E203

    print(f"Result of part 1: {points_cards.sum()}")
    print(f"Result of part 2: {counter_cards.sum()}")


if __name__ == "__main__":
    main()
