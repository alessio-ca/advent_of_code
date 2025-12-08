from utils import read_input
import numpy as np


def main(filename: str):
    data = [
        (1 if line[0] == "R" else -1) * int(line[1:]) for line in read_input(filename)
    ]
    operations = np.array(data, dtype=int)
    dial_positions = np.insert((50 + operations.cumsum()) % 100, 0, 50)
    print(f"Result of part 1: {np.count_nonzero(dial_positions == 0)}")

    corrected_positions = np.where(
        operations < 0, (dial_positions[:-1] - 1) % 100, dial_positions[:-1]
    )
    print(
        f"Result of part 1: {np.abs((corrected_positions + operations) // 100).sum()}"
    )


if __name__ == "__main__":
    main("2025/01/input.txt")
