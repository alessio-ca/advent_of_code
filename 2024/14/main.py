import re
from collections import Counter, defaultdict
from functools import reduce
from operator import mul

import numpy as np

from utils import CoordTuple, read_input


def predict_position(robot, shape: CoordTuple, steps: int = 100) -> CoordTuple:
    y, x, vy, vx = robot
    xg, yg = shape
    return (x + vx * steps) % xg, (y + vy * steps) % yg


def map_to_quadrant(occupancy: Counter[CoordTuple], shape: CoordTuple) -> int:
    xg, yg = shape
    qx, qy = xg // 2, yg // 2
    quadrants: defaultdict[int, int] = defaultdict(int)
    for pos, count in occupancy.items():
        x, y = pos
        if (x < qx) & (y < qy):
            quadrants[0] += count
        elif (x > qx) & (y < qy):
            quadrants[1] += count
        elif (x < qx) & (y > qy):
            quadrants[2] += count
        elif (x > qx) & (y > qy):
            quadrants[3] += count

    return reduce(mul, (value for _, value in quadrants.items()), 1)


def main(filename: str):
    input_str = filename.split("/")[-1]
    if "example" in input_str:
        shape = (7, 11)
    else:
        shape = (103, 101)

    robots = [
        list(map(int, re.findall(r"-?\d+", line))) for line in read_input(filename)
    ]

    occupancy = Counter(predict_position(robot, shape) for robot in robots)
    print(f"Result of part 1: {map_to_quadrant(occupancy, shape)}")

    # Dump the map!
    with open("2024/14/grid.txt", "w+") as f:
        grid = np.empty(shape=shape, dtype=str)
        # One map cycle is shape[0]*shape[1]
        for i in range(0, shape[0] * shape[1]):
            f.write(f"{str(i)}\n")
            grid[:] = "."
            for pos in Counter(predict_position(robot, shape, i) for robot in robots):
                grid[pos] = "#"
            f.write("\n".join("".join(str(cell) for cell in row) for row in grid))
            f.write("\n")

    # Go manually inspect the grid - search for the substring '########``
    print(f"Result of part 2: {7338}")


if __name__ == "__main__":
    main("2024/14/input.txt")
