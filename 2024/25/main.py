from utils import read_input_batch
import numpy as np
from itertools import product


def main(filename: str):

    schemes = read_input_batch(filename)
    keys = []
    locks = []
    size = len(schemes[0])
    for scheme in schemes:
        grid = np.array(list(map(list, scheme)), dtype="str") == "#"
        if any(grid[0]):
            # Lock
            locks.append((grid).sum(axis=0))
        else:
            # Key
            keys.append((grid).sum(axis=0))
    tot = 0
    for key, lock in product(keys, locks):
        if all(key + lock <= size):
            tot += 1

    print(f"Result of part 1: {tot}")


if __name__ == "__main__":
    main("2024/25/input.txt")
