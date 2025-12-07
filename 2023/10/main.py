import heapq
from typing import List, Set, Tuple

import numpy as np

from utils import CoordTuple, read_input

N = (-1, 0)
S = (1, 0)
W = (0, -1)
E = (0, 1)

DICT_PIPES = {
    "|": {N, S},
    "-": {W, E},
    "L": {N, E},
    "J": {N, W},
    "7": {S, W},
    "F": {S, E},
}

ROT_CLOCK = np.array([(0, -1), (1, 0)], dtype="int")
ROT_ANTI = np.array([(0, 1), (-1, 0)], dtype="int")


def calculate_angle(
    direction: CoordTuple, new_direction: CoordTuple, clock_nn: CoordTuple
) -> int:
    """Calculate angle between directions.
    Uses the clockwise nn of "new_direction" for comparison"""
    x_0, y_0 = direction
    x_1, y_1 = new_direction

    if x_0 * x_1 + y_0 * y_1 == 0:
        # Vectors are perpendicular
        if direction == clock_nn:
            return -1  # If clockwise rotation of the new direction brings
            # back the original direction, angle is anticlock
        else:
            return 1  # Otherwise, angle is clockwise
    return 0


def rotate(dir: CoordTuple) -> Tuple[CoordTuple, CoordTuple]:
    return tuple(ROT_CLOCK.dot(dir)), tuple(ROT_ANTI.dot(dir))


def dir_inverse(direction: CoordTuple) -> CoordTuple:
    x, y = direction
    return (-x, -y)


def add_tuples(point: CoordTuple, direction: CoordTuple) -> CoordTuple:
    x, y = point
    i, j = direction
    return (x + i, y + j)


def generate_nn_dirs(point: CoordTuple, grid_shape: CoordTuple) -> List[CoordTuple]:
    """Generate plausible nn in 4 directions.
    Returns a list marking the possible directions (N,S,W,E)"""
    x, y = point
    x_max, y_max = grid_shape
    return [
        (i, j)
        for i, j in [N, S, W, E]
        if (x + i) >= 0 and (x + i) < x_max and (y + j) >= 0 and (y + j) < y_max
    ]


def generate_all_nn(point: CoordTuple) -> List[CoordTuple]:
    """Generate all nn in all 8 directions.
    Returns a list marking all directions (can be out of bound)"""
    x, y = point
    return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2) if i != j]


class Network:
    def __init__(self, grid) -> None:
        # Initialise network
        self.grid = grid
        self.full_grid = set(
            [(x, y) for x in range(0, grid.shape[0]) for y in range(0, grid.shape[1])]
        )
        x, y = np.where(grid == "S")
        self.start = (x[0], y[0])
        self.linked_pipe, self.linked_dir = self.start_network()

        # Initialise loop
        self.network = set()
        self.network.add(self.start)
        self.clock_set: set[CoordTuple] = set()
        self.anti_set: set[CoordTuple] = set()
        self.total_angle = 0
        self.network_loop: set[CoordTuple] = set()

    def start_network(self) -> Tuple[CoordTuple, CoordTuple]:
        """Start the network. Find first connected pipe to start.
        Returns the connected pipe and direction taken from start to reach it"""
        nn_dirs = generate_nn_dirs(self.start, self.grid.shape)
        for direction in nn_dirs:
            pipe = self.grid[add_tuples(self.start, direction)]
            try:
                if dir_inverse(direction) in DICT_PIPES[pipe]:
                    return add_tuples(self.start, direction), direction
            except KeyError:
                continue
        else:
            raise Exception("This should not happen!")

    def update_sets(
        self, orig: CoordTuple, dest: CoordTuple, dir: CoordTuple
    ) -> CoordTuple:
        """Update sets of clock / anticlockwise neighbors to the network.
        Generates a pair of clock/anti clock rotations of "dir"
        Adds a segment between orig and dest, on both sides"""
        clock, anti = rotate(dir)
        # Clockwise segment
        self.clock_set.add(add_tuples(orig, clock))
        self.clock_set.add(add_tuples(dest, clock))
        # Anticlockwise segment
        self.anti_set.add(add_tuples(orig, anti))
        self.anti_set.add(add_tuples(dest, anti))
        return clock

    def construct_network(self):
        """Constructs the network"""
        # Set up loop
        orig = self.start
        dest = self.linked_pipe
        new_dir = self.linked_dir
        _ = self.update_sets(orig, dest, new_dir)

        while dest != self.start:
            self.network.add(dest)
            # Update parameters
            old_dir = new_dir
            new_dir = (
                DICT_PIPES[self.grid[dest]].difference({dir_inverse(old_dir)}).pop()
            )
            orig = dest
            dest = add_tuples(orig, new_dir)
            # Update clock/anticlock sets & total angle
            clock = self.update_sets(orig, dest, new_dir)
            self.total_angle += calculate_angle(old_dir, new_dir, clock)

        # Remove network nodes from clock/anticlock sets
        self.clock_set = self.clock_set.intersection(self.full_grid).difference(
            self.network
        )
        self.anti_set = self.anti_set.intersection(self.full_grid).difference(
            self.network
        )
        pass

    def _fill_flood(self, init_seeds: Set[CoordTuple]) -> Set[CoordTuple]:
        """Fill flood algorithm to fill area given a set of seeds."""
        # Initialize the full map minus the network.
        # Initialize queue and visited set
        full_map = self.full_grid.difference(self.network)
        queue = list(init_seeds)
        visited = set(queue)

        heapq.heapify(queue)
        while queue:
            # Pop from queue
            point = heapq.heappop(queue)
            # Test neighbors
            nns = generate_all_nn(point)
            for nn in nns:
                # If neighbor satisfies conditions, add to queue and visited
                if nn in full_map and nn not in visited:
                    heapq.heappush(queue, nn)
                    visited.add(nn)
        return visited.union(init_seeds)

    def construct_loop(self):
        """Construct full loop & calculate area"""
        if self.total_angle > 0:
            # Take clock set as the seeds
            self.network_loop = self._fill_flood(self.clock_set)
        else:
            # Take anti clock set as the seeds
            self.network_loop = self._fill_flood(self.anti_set)


def main(filename: str):
    grid = np.array([list(line) for line in read_input(filename)], dtype=str)
    network = Network(grid)
    network.construct_network()
    print(f"Result of part 1: {int((len(network.network) + 1) / 2)}")
    network.construct_loop()
    print(f"Result of part 2: {len(network.network_loop)}")


if __name__ == "__main__":
    main("2023/10/input.txt")
