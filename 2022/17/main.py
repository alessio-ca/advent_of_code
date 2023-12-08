from utils import read_input, timefunc
import itertools
from dataclasses import dataclass
from collections import defaultdict
from typing import List

SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


@dataclass
class Rock:
    # Define a rock as a list of integers
    # Each integer represents a row of the rock, in binary
    # Rocks are created already shifted by 2 to the right (as they would appear)
    rows: List[int]

    def create_rock(shape, width):
        # Get boundaries
        x_b, y_b = max(x for (x, _) in shape), max(y for (_, y) in shape)
        # Iterate over all possible coordinates
        matrix = [[(i, j) in shape for i in range(x_b + 1)] for j in range(y_b + 1)]
        # Convert to bit format
        rows = []
        for row in matrix:
            x = 0
            for i, v in enumerate(row):
                x += v << ((width - 1) - 2 - i)
            rows.append(x)
        return Rock(rows)

    def jet_move_rock(self, direction, width):
        if direction > 0:
            # Check move is possible (right shift)
            if any(row & 1 for row in self.rows):
                return self
            else:
                return Rock([row >> 1 for row in self.rows])

        else:
            # Check move is possible (left shift)
            if any(row & (1 << (width - 1)) for row in self.rows):
                return self
            else:
                return Rock([row << 1 for row in self.rows])


class RockSystem:
    def __init__(self, jet_streams, shapes):
        # Initialize params
        self.width = 7
        self.max_h = 0
        self.period_h = 0

        # Create rocks
        rocks = [Rock.create_rock(shape, self.width) for shape in shapes]

        # Create cyclic arrays
        self.streams = itertools.cycle(jet_streams)
        self.shapes = itertools.cycle(rocks)
        self.len_streams = len(jet_streams)
        self.len_shapes = len(shapes)

        # Create grid
        self.grid = defaultdict(int)
        self.grid[-1] = 2**self.width - 1

        # Create cache
        self.cache = {}
        self._last_jet = jet_streams[-1]

    def check_intersect(self, shape, h):
        # Check if intersects grid
        return any(row & self.grid[h + i] for i, row in enumerate(shape.rows))

    def update_grid(self, shape, h):
        for i, row in enumerate(shape.rows):
            self.grid[h + i + 1] |= row
        return self

    def push_or_fall(self, shape):
        # Define vertical "floor" of shape
        h = 3 + self.max_h
        # Do push and fall
        while not self.check_intersect(shape, h):
            jet = next(self.streams)
            jetted_shape = shape.jet_move_rock(jet, self.width)
            if not self.check_intersect(jetted_shape, h):
                shape = jetted_shape
            h -= 1
        self.update_grid(shape, h)
        self.max_h = max(self.max_h, h + len(shape.rows) + 1)

        self._last_jet = jet

        return self

    def create_periodic(self, idx_c, maxh_c, i, num):
        dh = self.max_h - maxh_c
        dt = i - idx_c

        n = (num - i) // dt
        self.period_h += dh * n
        i += dt * n

        return i

    def simulate(self, num):
        i = 0
        while i < num:
            shape = next(self.shapes)
            self.push_or_fall(shape)

            status = tuple(self.grid[self.max_h - i] for i in range(0, 21))
            pattern = (i % self.len_shapes, self._last_jet, status)
            if pattern in self.cache:
                idx_c, maxh_c = self.cache[pattern]
                i = self.create_periodic(idx_c, maxh_c, i, num)
            self.cache[pattern] = (i, self.max_h)

            i += 1


@timefunc
def main():
    map_jet = {">": 1, "<": -1}
    jet_streams = [
        *map(map_jet.get, read_input("2022/17/input.txt", line_strip=True)[0])
    ]

    rock_system = RockSystem(jet_streams, SHAPES)
    rock_system.simulate(2022)
    print(f"Result of part 1: {rock_system.period_h + rock_system.max_h}")

    rock_system = RockSystem(jet_streams, SHAPES)
    rock_system.simulate(1000000000000)
    print(f"Result of part 2: {rock_system.period_h + rock_system.max_h}")


if __name__ == "__main__":
    main()
