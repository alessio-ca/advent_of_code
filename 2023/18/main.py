from utils import read_input, CoordTuple, add_tuples
import re
from typing import Tuple, List
from itertools import accumulate
import numpy as np


PATTERN = r"^(U|R|L|D) (\d+) \(#(.+)\)"

MAP_DICT = {"0": "R", "1": "D", "2": "L", "3": "U"}


def generate_vertexes(
    point: CoordTuple,
    instr: Tuple[str, int],
) -> CoordTuple:
    s, n = instr
    if s == "R":
        return add_tuples(point, (0, n))
    elif s == "D":
        return add_tuples(point, (n, 0))
    elif s == "L":
        return add_tuples(point, (0, -n))
    else:
        return add_tuples(point, (-n, 0))


def create_trench(instructions: List[Tuple[str, int, str]]) -> List[CoordTuple]:
    return list(
        accumulate(
            [(x, y) for x, y, _ in instructions], generate_vertexes, initial=(0, 0)
        )
    )


def calculate_area(
    vertexes: List[CoordTuple], instructions: List[Tuple[str, int, str]]
) -> int:
    # Shoelace Formula gives the internal area,
    # given the vertex coordinates, with the start vertex being
    # replicated at the end of the list of coordinates
    array = np.array(vertexes, dtype=int)
    S1 = array[:-1, 0] * array[1:, 1]
    S2 = array[1:, 0] * array[:-1, 1]
    internal_area = np.abs(0.5 * (S1.sum() - S2.sum()))
    # The boundary area
    #  is equal to the sum of:
    #  - the perimeter / 2 (half-area of a block for all the boundary blocks)
    #  - 1 (block-like polygon always have 4 extra-corners giving 1/4 of a block )
    external_area = sum(x for _, x, _ in instructions) / 2 + 1
    return int(internal_area + external_area)


def main(filename: str):
    instructions = [
        (x, int(y), z)
        for row in read_input(filename)
        for (x, y, z) in re.findall(PATTERN, row)
    ]
    trench = create_trench(instructions)
    print(f"Result of part 1: {calculate_area(trench, instructions)}")
    true_instructions_WTF = [
        (MAP_DICT[s[-1]], int(s[:-1], 16), None) for _, _, s in instructions
    ]
    true_trench_WTF = create_trench(true_instructions_WTF)
    print(f"Result of part 2: {calculate_area(true_trench_WTF, true_instructions_WTF)}")


if __name__ == "__main__":
    main("2023/18/input.txt")
