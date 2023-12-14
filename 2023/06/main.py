from utils import read_input
import numpy as np
import re


def race_distance(race):
    """Solve a quadratic equation.
    Apply constraints"""
    t_max, record = race
    delta = -0.5 * t_max
    block = np.sqrt(delta**2 - record - 0.1)

    x1 = np.ceil(-delta - block).astype(int)
    x2 = np.floor(-delta + block).astype(int)

    return x2 - x1 + 1


def main():
    races = np.array(
        [
            list(map(int, re.findall(r"\d+", line)))
            for line in read_input("2023/06/input.txt")
        ],
        dtype="int",
    ).T

    n = 1
    for race in races:
        n *= race_distance(race)
    print(f"Result of part 1: {n}")

    X = tuple(
        int("".join(re.findall(r"\d+", line)))
        for line in read_input("2023/06/input.txt")
    )
    print(f"Result of part 2: {race_distance(X)}")


if __name__ == "__main__":
    main()
