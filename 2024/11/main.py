from utils import read_integer_lists
from collections import deque
from functools import cache


@cache
def memosequence(stone: str, n: int):
    if n == 0:
        return 1
    else:
        # Apply rules
        if stone == "0":
            return memosequence("1", n - 1)
        elif not (len(stone) % 2):
            first_half = stone[len(stone) // 2 :].lstrip("0")
            first_half = first_half if first_half else "0"
            return memosequence(first_half, n - 1) + memosequence(
                stone[: len(stone) // 2], n - 1
            )
        else:
            return memosequence(str(2024 * int(stone)), n - 1)


def main(filename: str):

    stones = deque(map(lambda d: str(d), read_integer_lists(filename)[0]))
    print(f"Result of part 1: {sum(memosequence(stone, 25) for stone in stones)}")
    print(f"Result of part 2: {sum(memosequence(stone, 75) for stone in stones)}")


if __name__ == "__main__":
    main("2024/11/input.txt")
