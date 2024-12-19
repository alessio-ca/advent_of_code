from utils import read_input_batch
from functools import cache


@cache
def count_ways(design: str, patterns: tuple[str]) -> int:
    if design == "":
        return 1
    count = 0
    for pattern in patterns:
        if design.startswith(pattern):
            count += count_ways(design.removeprefix(pattern), patterns)
    return count


def main(filename: str):
    patterns, designs = read_input_batch(filename, line_split=False)
    patterns = tuple(patterns[0].split(", "))
    n_ways = [count_ways(design, patterns) for design in designs]

    print(f"Result of part 1: {sum(n > 0 for n in n_ways)}")
    print(f"Result of part 2: {sum(n_ways)}")


if __name__ == "__main__":
    main("2024/19/input.txt")
