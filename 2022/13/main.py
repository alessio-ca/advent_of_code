import ast
from functools import cmp_to_key
from math import prod

import numpy as np

from utils import read_input_batch

from typing import Any


def compare_packets(A: Any, B: Any) -> int:
    a_type = isinstance(A, list)
    b_type = isinstance(B, list)

    if a_type and b_type:
        # List to list
        for i, a in enumerate(A):
            # Iterate over list A
            try:
                check = compare_packets(a, B[i])
                if abs(check) == 1:
                    return check
            # Right list ran out first
            except IndexError:
                return -1
        # If we get out of the loop, left list finished
        return int(len(A) < len(B))

    elif (not a_type) and (not b_type):
        # Integer to integer
        if A < B:
            return 1
        elif A == B:
            return 0
        else:
            return -1

    else:
        # Mixed type
        if a_type:
            B = [B]
        else:
            A = [A]
        return compare_packets(A, B)


def main(filename: str):
    raw_packets = read_input_batch(filename, line_split=True)
    packets = [
        [ast.literal_eval(subpacket) for subpacket in packet] for packet in raw_packets
    ]
    res = [compare_packets(*pair) for pair in packets]
    idx = np.where(np.array(res, dtype=np.int64) == 1)[0]
    print(f"Result of part 1: {sum(idx + 1)}")

    flattened_packets = [subpacket for packet in packets for subpacket in packet]
    divider = [[[2]], [[6]]]
    ordered_packets = sorted(
        flattened_packets + divider, key=cmp_to_key(compare_packets)
    )[::-1]

    divider_idx = [ordered_packets.index(el) + 1 for el in divider]
    print(f"Result of part 2: {prod(divider_idx)}")


if __name__ == "__main__":
    main("2022/13/input.txt")
