from utils import read_input
import numpy as np
from functools import reduce


def forward_value(seq: np.ndarray) -> int:
    n = 0
    while np.any(seq):
        n += seq[-1]
        seq = np.diff(seq)
    return n


def backward_value(seq: np.ndarray) -> int:
    values = []
    while np.any(seq):
        values.append(seq[0])
        seq = np.diff(seq)
    return reduce(lambda a, b: b - a, reversed(values), 0)


def main():
    hists = [
        np.array(list(map(int, line.split())), dtype="int")
        for line in read_input("2023/09/input.txt")
    ]
    print(f"Result of part 1: {sum(forward_value(hist) for hist in hists)}")
    print(f"Result of part 2: {sum(backward_value(hist) for hist in hists)}")


if __name__ == "__main__":
    main()
