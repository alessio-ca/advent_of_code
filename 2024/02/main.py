from itertools import pairwise, combinations
from utils import read_input


def is_safe(report: list[int]) -> bool:
    steps = [y - x for (x, y) in pairwise(report)]
    return (all(step > 0 for step in steps) | all(step < 0 for step in steps)) & all(
        (abs(step) >= 1) & (abs(step) <= 3) for step in steps
    )


def main(filename: str):
    reports = list(map(lambda x: list(map(int, x.split(" "))), read_input(filename)))

    mask_steps = map(is_safe, reports)
    print(f"Result of part 1: {sum(mask_steps)}")

    dampened_reports = (combinations(report, len(report) - 1) for report in reports)
    mask_steps = (
        any(is_safe(report) for report in reports) for reports in dampened_reports
    )
    print(f"Result of part 2: {sum(mask_steps)}")


if __name__ == "__main__":
    main("2024/02/input.txt")
