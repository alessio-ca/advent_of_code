from __future__ import annotations

import math
from functools import cached_property

import numpy as np
import regex as re

from utils import read_input


class Snowflake:
    def __init__(self, config: list[tuple[int, int, int]]) -> None:
        x, y, z = config[0]
        vx, vy, vz = config[1]
        self.x0 = x
        self.y0 = y
        self.z0 = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    @cached_property
    def x1(self):
        return self.x0 + self.vx

    @cached_property
    def y1(self):
        return self.y0 + self.vy

    @cached_property
    def z1(self):
        return self.z0 + self.vz

    def path_intersection(self, other: Snowflake):
        # Geometric intersection of two lines given two points on each line
        denominator = (self.x0 - self.x1) * (other.y0 - other.y1) - (
            self.y0 - self.y1
        ) * (other.x0 - other.x1)
        det_0 = self.x0 * self.y1 - self.y0 * self.x1
        det_1 = other.x0 * other.y1 - other.y0 * other.x1
        num_x = det_0 * (other.x0 - other.x1) - det_1 * (self.x0 - self.x1)
        num_y = det_0 * (other.y0 - other.y1) - det_1 * (self.y0 - self.y1)
        try:
            return (num_x / denominator, num_y / denominator)
        except ZeroDivisionError:
            return (math.inf, math.inf)

    def time_to_intersection(self, x_t: int):
        return (x_t - self.x0) / self.vx


def intersect(snowflakes: list[Snowflake], area_bounds: tuple[int, int]) -> int:
    bound_min, bound_max = area_bounds
    counter = 0
    for i, snow_1 in enumerate(snowflakes):
        for snow_2 in snowflakes[(i + 1) :]:
            x_t, y_t = snow_1.path_intersection(snow_2)
            if bound_min <= x_t <= bound_max and bound_min <= y_t <= bound_max:
                if (
                    snow_1.time_to_intersection(x_t) >= 0
                    and snow_2.time_to_intersection(x_t) >= 0
                ):
                    counter += 1
    return counter


def create_coefficient_matrices(
    snowflakes: list[Snowflake],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create coefficient matrices that represents three linear systems of equations.
    We need three linear systems XY, XZ and YZ to completely solve the problem.
    See PDF for a theoretical derivation.
    """
    XY = np.zeros(shape=(len(snowflakes), 4), dtype=int)
    bxy = np.zeros(shape=(len(snowflakes),), dtype=int)
    XZ = np.zeros(shape=(len(snowflakes), 4), dtype=int)
    bxz = np.zeros(shape=(len(snowflakes),), dtype=int)
    YZ = np.zeros(shape=(len(snowflakes), 4), dtype=int)
    byz = np.zeros(shape=(len(snowflakes),), dtype=int)

    for i, el in enumerate(snowflakes):
        XY[i, 0] = -el.vy
        XY[i, 1] = el.vx
        XY[i, 2] = el.y0
        XY[i, 3] = -el.x0
        bxy[i] = -el.x0 * el.vy + el.y0 * el.vx

        XZ[i, 0] = -el.vz
        XZ[i, 1] = el.vx
        XZ[i, 2] = el.z0
        XZ[i, 3] = -el.x0
        bxz[i] = -el.x0 * el.vz + el.z0 * el.vx

        YZ[i, 0] = -el.vz
        YZ[i, 1] = el.vy
        YZ[i, 2] = el.z0
        YZ[i, 3] = -el.y0
        byz[i] = -el.y0 * el.vz + el.z0 * el.vy

    return (
        np.diff(XY, axis=0),
        np.diff(bxy),
        np.diff(XZ, axis=0),
        np.diff(bxz),
        np.diff(YZ, axis=0),
        np.diff(byz),
    )


def solve_systems(
    X1: np.ndarray,
    b1: np.ndarray,
    X2: np.ndarray,
    b2: np.ndarray,
    X3: np.ndarray,
    b3: np.ndarray,
) -> int:
    # The systems have 4 unknown and potentially N equations with N > 6.
    # We batch solve the system to improve accuracy and eliminate floating point errors

    n_batches = int(X1.shape[0] / 4)
    batch_X1 = np.split(X1[: n_batches * 4], n_batches)
    batch_b1 = np.split(b1[: n_batches * 4], n_batches)
    batch_X2 = np.split(X2[: n_batches * 4], n_batches)
    batch_b2 = np.split(b2[: n_batches * 4], n_batches)
    batch_X3 = np.split(X3[: n_batches * 4], n_batches)
    batch_b3 = np.split(b3[: n_batches * 4], n_batches)

    result = []
    for XX1, XX2, XX3, bb1, bb2, bb3 in zip(
        batch_X1, batch_X2, batch_X3, batch_b1, batch_b2, batch_b3
    ):
        x1, y1, _, _ = np.linalg.solve(XX1, bb1)
        x2, z1, _, _ = np.linalg.solve(XX2, bb2)
        y2, z2, _, _ = np.linalg.solve(XX3, bb3)
        result.append(x1 + x2 + y1 + y2 + z1 + z2)
    test = np.array(result)
    print(test.mean() / 2, test.std() / 2)
    return int(np.array(result).mean() / 2)


def main(filename: str):
    if "example" in filename:
        bound_min = 7
        bound_max = 27
    else:
        bound_min = 200000000000000
        bound_max = 400000000000000

    snowflakes = [
        Snowflake(
            [
                tuple(map(int, tup.split(",")))  # type: ignore
                for tup in re.findall(r"-?\d+,\s+-?\d+,\s+-?\d+", line)
            ]
        )
        for line in read_input(filename)
    ]

    print(f"Result of part 1: {intersect(snowflakes, (bound_min, bound_max))}")

    res = solve_systems(*create_coefficient_matrices(snowflakes))
    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main("2023/24/input.txt")
