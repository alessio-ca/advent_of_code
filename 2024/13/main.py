from utils import read_input_batch
import re
import numpy as np


def solve_linear_system(machine: list[list[int]], part_1: bool = True) -> int:
    # Create linear system
    X = np.array(machine, dtype=int).T
    if not part_1:
        X[:, -1] += 10000000000000
    # Solve and round results to ints
    a, b = np.linalg.solve(X[:, :-1], X[:, -1])
    a = a.round().astype(int)
    b = b.round().astype(int)
    # Check if integer solution exists
    if np.all(
        np.matmul(X[:, :-1], np.array([[a], [b]], dtype=int)).ravel() == (X[:, -1])
    ):
        return 3 * a + b
    else:
        return 0


def main(filename: str):
    machines = [
        [list(map(int, re.findall(r"\d+", line))) for line in machine]
        for machine in read_input_batch(filename, line_split=False)
    ]
    print(
        f"Result of part 1: {sum(solve_linear_system(machine) for machine in machines)}"
    )
    print(
        "Result of part 2: "
        f"{sum(solve_linear_system(machine, False) for machine in machines)}"
    )


if __name__ == "__main__":
    main("2024/13/input.txt")
