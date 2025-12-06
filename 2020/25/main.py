import numpy as np
from numba import njit  # type: ignore

REMAINDER = 20201227
SUBJECT_NO_PUBLIC = 7


@njit
def find_loop_size(subject_num: int, value_to_match: int):
    x = 1
    loop_size = 0
    while x != value_to_match:
        x = (x * subject_num) % REMAINDER
        loop_size += 1

    return loop_size


@njit
def transform_subject(subject_num: int, loop_size: int):
    x = 1
    for _ in range(loop_size):
        x = (x * subject_num) % REMAINDER

    return x


def main():
    input_keys = np.loadtxt("2020/25/input.txt", dtype="int")

    loop_size = find_loop_size(SUBJECT_NO_PUBLIC, input_keys[0])
    encryption_key = transform_subject(input_keys[1], loop_size)

    print(f"Result of part 1: {encryption_key}")


if __name__ == "__main__":
    main()
