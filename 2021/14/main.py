from utils import read_input_batch
from collections import defaultdict
from typing import Iterable, Any, Dict, List


class CounterDict:
    def __init__(self, iterable: Iterable):
        self.count = defaultdict(int)
        self._initialize(iterable)

    def _initialize(self, iterable: Iterable):
        for el in iterable:
            self.count[el] += 1
        return self

    def add(self, el: Any, count: int):
        self.count[el] += count


def polymerise(
    rounds: int,
    bigrams: List[str],
    polymer: str,
    rules_dict: Dict[str, str],
) -> CounterDict:
    """Function to perform `rounds` polymerisation rounds"""

    # Create initial bigrams and letter counter
    bigrams_counter = CounterDict(bigrams)
    letter_counter = CounterDict(polymer)

    for _ in range(rounds):
        # Create new counter candidate
        temp_counter = CounterDict([])
        for bigram, count in bigrams_counter.count.items():
            # Fetch insertion
            insertion = rules_dict[bigram]

            # Augment the counter for the first and second bigram after insertion
            temp_counter.add(bigram[0] + insertion, count)
            temp_counter.add(insertion + bigram[1], count)

            # Update letter counter adding the count to the insertion
            letter_counter.add(insertion, count)

        # Make the counter candidate the new bigram counter
        bigrams_counter.count = temp_counter.count

    return letter_counter


def main():
    input_file = read_input_batch("2021/14/input.txt", line_split=False)
    polymer = input_file[0][0]
    rules = [tuple(line.split(" -> ")) for line in input_file[1]]
    bigrams = [c1 + c2 for c1, c2 in zip(polymer, polymer[1:])]

    # Convert rules to dictionary
    rules_dict = {}
    for bigram, insertion in rules:
        rules_dict[bigram] = insertion

    letter_counter = polymerise(10, bigrams, polymer, rules_dict)
    # Get min/max from letter counter
    min_count, max_count = min(letter_counter.count.values()), max(
        letter_counter.count.values()
    )
    print(f"Result of part 1: {max_count - min_count}")

    letter_counter = polymerise(40, bigrams, polymer, rules_dict)
    # Get min/max from letter counter
    min_count, max_count = min(letter_counter.count.values()), max(
        letter_counter.count.values()
    )
    print(f"Result of part 2: {max_count - min_count}")


if __name__ == "__main__":
    main()
