from utils import read_input
import regex as re
from functools import reduce
from operator import mul
from typing import Pattern, Iterable


def get_product(s: str, pattern: Pattern) -> Iterable[int]:
    return map(
        lambda x: reduce(mul, map(int, re.findall(r"\d+", x))),
        re.findall(pattern, s),
    )


def main(filename: str):
    memory = "".join(read_input(filename))

    pattern = re.compile(r"mul\(\d+,\d+\)")
    print(f"Result of part 1: {sum(get_product(memory, pattern))}")

    valid_memory = ""
    for el in memory.split("do()"):
        valid_memory += el.split("don't()")[0]

    print(f"Result of part 2: {sum(get_product(valid_memory, pattern))}")


if __name__ == "__main__":
    main("2024/03/input.txt")
