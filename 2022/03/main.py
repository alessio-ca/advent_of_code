from itertools import zip_longest
from typing import List

from utils import read_input


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks.

    >>> grouper('ABCDEFG', 3, 'x')
    ['ABC', 'DEF', 'Gxx']
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def item_priorities(items: List[str]) -> List[int]:
    upper_base, lower_base = ord("A"), ord("a")
    return [
        ord(item) - upper_base + 27 if item.isupper() else ord(item) - lower_base + 1
        for item in items
    ]


def main(filename: str):
    X_raw = read_input(filename, line_strip=False)
    # Create rucksacks
    rucksacks = [
        (line[:size], line[size:])
        for line, size in zip(X_raw, [int(len(line) / 2) for line in X_raw])
    ]
    # Obtain wrong items
    wrong_items = []
    for sack_1, sack_2 in rucksacks:
        wrong_items.append(set(sack_1).intersection(set(sack_2)).pop())

    print(f"Result of part 1: {sum(item_priorities(wrong_items))}")
    # Obtain group badges
    group_rucksacks = grouper(X_raw, 3)
    group_badges = []
    for sack_1, sack_2, sack_3 in group_rucksacks:
        group_badges.append(
            set(sack_1).intersection(set(sack_2)).intersection(set(sack_3)).pop()
        )
    print(f"Result of part 2: {sum(item_priorities(group_badges))}")


if __name__ == "__main__":
    main("2022/03/input.txt")
