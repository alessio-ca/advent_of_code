from utils import read_input
import re
import heapq
from collections.abc import Sequence, Callable, Iterable
from typing import TypeVar

Q = TypeVar("Q", bound=Sequence[tuple[int, int]])


def push_part_1(queue: Q, residual: int, numbers: list[int], i: int) -> None:
    # If residual is divisible by number, add division to queue
    if residual % numbers[i] == 0:
        heapq.heappush(queue, (residual / numbers[i], i + 1))
    # Add substraction to queue
    heapq.heappush(queue, (residual - numbers[i], i + 1))


def push_part_2(queue: Q, residual: int, numbers: list[int], i: int) -> None:
    push_part_1(queue, residual, numbers, i)
    # Obtain candidate in string form & digit size
    candidate = repr(int(residual))
    number_digits = len(repr(numbers[i]))
    candidate_digits = len(candidate) - number_digits
    # If the residual can be split into two sides with the right one matching number,
    # add residual without the number
    if (int(candidate[-number_digits:]) == numbers[i]) & (candidate_digits > 0):
        heapq.heappush(queue, (int(candidate[:candidate_digits]), i + 1))


def calibration(
    equations: Iterable[list[int]], push_fun: Callable[[Q, int, list[int], int], None]
) -> int:
    sum = 0
    for equation in equations:
        # Obtain result and numbers (reversed, to walk backward)
        result, numbers = equation[0], equation[1:]
        numbers.reverse()
        # Use priority queue, minimises residual
        queue = [(result, 0)]
        heapq.heapify(queue)
        while queue:
            residual, i = heapq.heappop(queue)
            # If residual goes below 0 or numbers are exausted,
            # return the result is the residual is exactly 0
            # & exit the loop
            if (residual < 0) | (i == len(numbers)):
                if residual == 0:
                    sum += result
                    break
            # Otherwise, push the candidates to the queue
            else:
                push_fun(queue, residual, numbers, i)

    return sum


def main(filename: str):
    equations = list(
        map(lambda x: list(map(int, re.findall(r"\d+", x))), read_input(filename))
    )

    print(f"Result of part 1: {calibration(equations, push_part_1)}")
    print(f"Result of part 2: {calibration(equations, push_part_2)}")


if __name__ == "__main__":
    main("2024/07/input.txt")
