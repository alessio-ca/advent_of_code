from utils import read_input
from dataclasses import dataclass
from collections import Counter
from typing import Dict

DICT_VALUES = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
DICT_VALUES_PART_2 = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10}


@dataclass
class Card:
    face: str
    dict_values: Dict[str, int]

    def value(self) -> int:
        if self.face.isdigit():
            return int(self.face)
        else:
            return self.dict_values[self.face]


class Hand:
    def __init__(self, cards: str, bid: int, dict_values: Dict[str, int]) -> None:
        self.cards = cards
        self.bid = int(bid)
        self.counter = Counter(cards)
        self.dict_values = dict_values

    def define_hand(self):
        counts = [v for _, v in self.counter.most_common()]
        if counts[0] == 1:
            return 0  # high card
        elif counts[0] == 2:
            if counts[1] == 1:
                return 1  # single pair
            else:
                return 2  # double pair
        elif counts[0] == 3:
            if counts[1] == 1:
                return 3  # three of a kind
            else:
                return 4  # full house
        elif counts[0] == 4:
            return 5  # 4 of a kind
        else:
            return 6  # poker

    def define_hand_part_2(self):
        if "J" not in self.counter.keys():
            return self.define_hand()
        else:
            # Jacks can just be added to the most common card.
            # This optimises the uses of jacks
            n_j = self.counter["J"]
            # Only perform the addition if hand is not already a 5-a-kind
            if n_j < 5:
                jack_free = "".join(card for card in self.cards if card != "J")
                most_common, _ = Counter(jack_free).most_common(1)[0]
                self.counter = Counter(jack_free + most_common * n_j)
            return self.define_hand()

    def compute_total_values(self):
        """Assign total value by counting in base 14.
        This ensures full comparison between hands at once"""
        return sum(
            14 ** (len(self.cards) - i) * Card(x, self.dict_values).value()
            for i, x in enumerate(self.cards)
        )


def main():
    games = [line.split() for line in read_input("2023/07/input.txt")]
    hand_sets = [Hand(hand, bid, DICT_VALUES) for hand, bid in games]
    hand_tuples = [
        (hand.define_hand(), hand.compute_total_values(), hand.bid)
        for hand in hand_sets
    ]
    hand_tuples.sort(key=lambda t: (t[0], t[1]))
    print(f"Result of part 1: {sum((i+1)*j for i,(_,_,j) in enumerate(hand_tuples))}")

    hand_sets = [Hand(hand, bid, DICT_VALUES_PART_2) for hand, bid in games]
    hand_tuples = [
        (hand.define_hand_part_2(), hand.compute_total_values(), hand.bid)
        for hand in hand_sets
    ]
    hand_tuples.sort(key=lambda t: (t[0], t[1]))
    print(f"Result of part 2: {sum((i+1)*j for i,(_,_,j) in enumerate(hand_tuples))}")


if __name__ == "__main__":
    main()
