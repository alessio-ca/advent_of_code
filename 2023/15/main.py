from utils import read_input
import re
from typing import List, Tuple
from collections import defaultdict, deque


def hash_algorithm(sequence: str) -> int:
    queue = deque(sequence)
    value = 0
    while queue:
        c = ord(queue.popleft())
        value += c
        value *= 17
        value %= 256
    return value


def parse_sequences(sequences: List[str]) -> List[Tuple[str, int]]:
    list_seq = []
    for seq in sequences:
        x, y = re.split(r"-|=", seq)
        try:
            y = int(y)
        except ValueError:
            y = 0
        list_seq.append((x, y))
    return list_seq


class Boxes:
    def __init__(self, sequences) -> None:
        self.sequences = sequences
        # Labels are represented as {box: deque([labels])}
        self.dict_labels = defaultdict(deque)
        # Lenses are represented as {box: {label: focal}}
        self.dict_lenses = defaultdict(lambda: defaultdict(int))

    def perform_extraction(self, hash_box, idx):
        self.dict_labels[hash_box].rotate(-idx)
        self.dict_labels[hash_box].popleft()
        self.dict_labels[hash_box].rotate(idx)
        pass

    def process_sequence(self, step: Tuple[str, int]):
        label, focal = step
        hash_box = hash_algorithm(label)
        if focal == 0:
            # This corresponds to '-'
            # Find the idx of the label or set idx = -1
            try:
                idx = self.dict_labels[hash_box].index(label)
            except ValueError:
                idx = -1
            # If the label exist, do operations
            if idx >= 0:
                # Pop the label and shift everything
                self.perform_extraction(hash_box, idx)
                # Pop the label from the lenses
                self.dict_lenses[hash_box].pop(label)
        else:
            # This corresponds to '='
            # Add the label if needed
            if label not in self.dict_lenses[hash_box]:
                self.dict_labels[hash_box].append(label)
            # Update focal
            self.dict_lenses[hash_box][label] = focal

    def initialize(self):
        for seq in self.sequences:
            self.process_sequence(seq)
        pass

    def calculate_power(self):
        # Convert label dictionary to the same format as `dict_lenses`
        dict_order = {
            i: {label: seq.index(label) for label in seq}
            for i, seq in self.dict_labels.items()
        }
        total = 0
        for key, value in dict_order.items():
            if value:
                for label, slot in value.items():
                    total += (key + 1) * (slot + 1) * self.dict_lenses[key][label]
        return total


def main():
    sequences = read_input("2023/15/input.txt")[0].split(",")
    total_n = 0
    for seq in sequences:
        total_n += hash_algorithm(seq)
    print(f"Result of part 1: {total_n}")
    list_seq = parse_sequences(sequences)
    boxes = Boxes(list_seq)
    boxes.initialize()
    print(f"Result of part 2: {boxes.calculate_power()}")


if __name__ == "__main__":
    main()
