from utils import read_input, timefunc
from typing import List, Tuple
import numpy as np
import itertools
from collections import Counter


def assign_blocks(
    x_array: np.ndarray, y_array: np.ndarray
) -> List[Tuple[np.ndarray, np.ndarray]]:
    blocks = []
    # Calculate diffs along x, give the non-zero elements
    diff_x = np.diff(x_array, prepend=x_array[0]).nonzero()[0]
    blocks_x = np.split(x_array, diff_x)
    blocks_y = np.split(y_array, diff_x)
    for x_row, y_row in zip(blocks_x, blocks_y):
        # Calculate diffs along y, give the non-zero elements
        diff_y = (np.diff(y_row, prepend=y_row[0] - 1) - 1).nonzero()[0]
        blocks_y = np.split(y_row, diff_y)
        blocks_x = np.split(x_row, diff_y)
        blocks.append(list(zip(blocks_x, blocks_y)))

    return list(itertools.chain(*blocks))


def assign_nn(
    blocks: List[Tuple[np.ndarray, np.ndarray]], matrix_shape: Tuple[int, int]
) -> List[Tuple[np.ndarray, np.ndarray]]:
    x_shape, y_shape = matrix_shape
    blocks_nn = []
    for block in blocks:
        x, y = block
        # Order of additions is:
        # - Upper row
        # - Lower row
        # - Left corners
        # - Right corners
        nn_x = np.concatenate(
            (
                x - 1,
                x + 1,
                np.arange(x.min() - 1, x.max() + 2),
                np.arange(x.min() - 1, x.max() + 2),
            )
        )
        nn_y = np.concatenate(
            (y, y, np.repeat(y[0] - 1, 3), np.repeat(y[-1] + 1, 3))
        )  # noqa: E501
        # Filter
        mask = (nn_x >= 0) & (nn_x < x_shape) & (nn_y >= 0) & (nn_y < y_shape)
        nn_x = nn_x[mask]
        nn_y = nn_y[mask]

        blocks_nn.append((nn_x, nn_y))

    return blocks_nn


def calculate_ratios(
    gears: List[Tuple[int, int]],
    matrix: np.ndarray,
    blocks: List[Tuple[np.ndarray, np.ndarray]],
    blocks_nn: List[Tuple[np.ndarray, np.ndarray]],
) -> List[int]:
    # Filter gears to iterate on
    counter_gears = Counter(
        (x, y)
        for block_x, block_y in blocks_nn
        for x, y in zip(block_x, block_y)  # noqa: E501
    )
    gears = [gear for gear in gears if counter_gears[gear] == 2]

    # Iterate over valid gears
    ratios: List[int] = []
    for gear in gears:
        a = -1
        b = 0
        block_list = zip(
            (int("".join(matrix[block])) for block in blocks),
            (
                set((x, y) for x, y in zip(block_x, block_y))
                for block_x, block_y in blocks_nn
            ),
        )
        while (a * b) <= 0:
            block, nn = next(block_list)
            if gear in nn:
                if a < 0:
                    a = block
                else:
                    b = block

        ratios.append(a * b)
    return ratios


@timefunc
def main():
    matrix = np.array([list(line) for line in read_input("2023/03/input.txt")])
    # Get array of non-zero (digit) elements
    x_digits, y_digits = np.array(
        [[s.isdigit() for s in row] for row in matrix]
    ).nonzero()
    # Assign blocks
    blocks = assign_blocks(x_digits, y_digits)
    # Calculate NNs
    blocks_nn = assign_nn(blocks, matrix.shape)

    # Perform loop
    res = 0
    for block, block_nn in zip(blocks, blocks_nn):
        if any(np.char.isdigit(matrix[block_nn]) | (matrix[block_nn] != ".")):
            res += int("".join(matrix[block]))
    print(f"Result of part 1: {res}")

    gears = list(zip(*((matrix == "*").nonzero())))
    # Calculate ratios
    ratios = calculate_ratios(gears, matrix, blocks, blocks_nn)
    print(f"Result of part 2: {sum(ratios)}")


if __name__ == "__main__":
    main()
