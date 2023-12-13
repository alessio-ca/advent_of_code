"""
--- Day 17: Conway Cubes ---

As your flight slowly drifts through the sky, the Elves at the Mythical Information
 Bureau at the North Pole contact you. They'd like some help debugging a malfunctioning
  experimental energy source aboard one of their super-secret imaging satellites.

The experimental energy source is based on cutting-edge technology: a set of Conway
 Cubes contained in a pocket dimension! When you hear it's having problems, you can't
  help but agree to take a look.

The pocket dimension contains an infinite 3-dimensional grid. At every integer
 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or
  inactive.

In the initial state of the pocket dimension, almost all cubes start inactive.
 The only exception to this is a small flat region of cubes (your puzzle input);
  the cubes in this region start in the specified active (#) or inactive (.) state.

The energy source then proceeds to boot up by executing six cycles.

Each cube only ever considers its neighbors: any of the 26 other cubes where any of
 their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3, its
  neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.

During a cycle, all cubes simultaneously change their state according to the following
 rules:

If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube
 remains active. Otherwise, the cube becomes inactive.
If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes
 active. Otherwise, the cube remains inactive.
The engineers responsible for this experimental energy source would like you to
 simulate the pocket dimension and determine what the configuration of cubes should be
  at the end of the six-cycle boot process.

For example, consider the following initial state:

.#.
..#
###
Even though the pocket dimension is 3-dimensional, this initial state represents a
 small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1
  region of the 3-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations,
 where the result of each cycle is shown layer-by-layer at each given z coordinate (and
  the frame of view follows the active cells in each cycle):

Before any cycles:

z=0
.#.
..#
###


After 1 cycle:

z=-1
#..
..#
.#.

z=0
#.#
.##
.#.

z=1
#..
..#
.#.


After 2 cycles:

z=-2
.....
.....
..#..
.....
.....

z=-1
..#..
.#..#
....#
.#...
.....

z=0
##...
##...
#....
....#
.###.

z=1
..#..
.#..#
....#
.#...
.....

z=2
.....
.....
..#..
.....
.....


After 3 cycles:

z=-2
.......
.......
..##...
..###..
.......
.......
.......

z=-1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=0
...#...
.......
#......
.......
.....##
.##.#..
...#...

z=1
..#....
...#...
#......
.....##
.#...#.
..#.#..
...#...

z=2
.......
.......
..##...
..###..
.......
.......
.......
After the full six-cycle boot process completes, 112 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles. How many cubes are
 left in the active state after the sixth cycle?

--- Part Two ---

For some reason, your simulated results don't match what the experimental energy source
 engineers expected. Apparently, the pocket dimension actually has four spatial
  dimensions, not three.

The pocket dimension contains an infinite 4-dimensional grid. At every integer
 4-dimensional coordinate (x,y,z,w), there exists a single cube (really, a hypercube)
  which is still either active or inactive.

Each cube only ever considers its neighbors: any of the 80 other cubes where any of
 their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3,w=4,
  its neighbors include the cube at x=2,y=2,z=3,w=3, the cube at x=0,y=2,z=3,w=4, and
   so on.

The initial state of the pocket dimension still consists of a small flat region of
 cubes. Furthermore, the same rules for cycle updating still apply: during each cycle,
  consider the number of active neighbors of each cube.

For example, consider the same initial state as in the example above. Even though the
 pocket dimension is 4-dimensional, this initial state represents a small 2-dimensional
  slice of it. (In particular, this initial state defines a 3x3x1x1 region of the
   4-dimensional space.)

Simulating a few cycles from this initial state produces the following configurations,
 where the result of each cycle is shown layer-by-layer at each given z and w
  coordinate:

Before any cycles:

z=0, w=0
.#.
..#
###


After 1 cycle:

z=-1, w=-1
#..
..#
.#.

z=0, w=-1
#..
..#
.#.

z=1, w=-1
#..
..#
.#.

z=-1, w=0
#..
..#
.#.

z=0, w=0
#.#
.##
.#.

z=1, w=0
#..
..#
.#.

z=-1, w=1
#..
..#
.#.

z=0, w=1
#..
..#
.#.

z=1, w=1
#..
..#
.#.


After 2 cycles:

z=-2, w=-2
.....
.....
..#..
.....
.....

z=-1, w=-2
.....
.....
.....
.....
.....

z=0, w=-2
###..
##.##
#...#
.#..#
.###.

z=1, w=-2
.....
.....
.....
.....
.....

z=2, w=-2
.....
.....
..#..
.....
.....

z=-2, w=-1
.....
.....
.....
.....
.....

z=-1, w=-1
.....
.....
.....
.....
.....

z=0, w=-1
.....
.....
.....
.....
.....

z=1, w=-1
.....
.....
.....
.....
.....

z=2, w=-1
.....
.....
.....
.....
.....

z=-2, w=0
###..
##.##
#...#
.#..#
.###.

z=-1, w=0
.....
.....
.....
.....
.....

z=0, w=0
.....
.....
.....
.....
.....

z=1, w=0
.....
.....
.....
.....
.....

z=2, w=0
###..
##.##
#...#
.#..#
.###.

z=-2, w=1
.....
.....
.....
.....
.....

z=-1, w=1
.....
.....
.....
.....
.....

z=0, w=1
.....
.....
.....
.....
.....

z=1, w=1
.....
.....
.....
.....
.....

z=2, w=1
.....
.....
.....
.....
.....

z=-2, w=2
.....
.....
..#..
.....
.....

z=-1, w=2
.....
.....
.....
.....
.....

z=0, w=2
###..
##.##
#...#
.#..#
.###.

z=1, w=2
.....
.....
.....
.....
.....

z=2, w=2
.....
.....
..#..
.....
.....
After the full six-cycle boot process completes, 848 cubes are left in the active state.

Starting with your given initial configuration, simulate six cycles in a 4-dimensional
 space. How many cubes are left in the active state after the sixth cycle?
"""
import numpy as np
from scipy.ndimage import convolve
from utils import read_input

EMPTY_CHAR = "."
FULL_CHAR = "#"


class CellularAutomataSystem:
    def __init__(self, X: np.array, dimension: int = 3):
        self.initial_flat_slice = X
        self.dimension = dimension
        self.reset()

    def reset(self):
        self.idx = 0
        # Define multidimensional grid
        self.grid = np.zeros(
            shape=tuple(
                max(self.initial_flat_slice.shape) for i in range(self.dimension)
            ),
            dtype="int",
        )
        # Perform initialization slice
        initial_slice = [slice(None)] * self.initial_flat_slice.ndim + [0] * (
            self.dimension - self.initial_flat_slice.ndim
        )
        self.grid[tuple(initial_slice)] = self.initial_flat_slice
        # Define conv filter
        self.conv_filter = np.ones(
            shape=tuple(3 for i in range(self.dimension)), dtype="int"
        )
        self.conv_filter[tuple([1] * self.conv_filter.ndim)] = 0

    def augment(self):
        """Function to augment grid in all dimensions"""
        # Define new shape
        shape = self.grid.shape[0] + 2
        # Initialize new grid
        Y = np.zeros(shape=tuple(shape for i in range(self.dimension)))
        # Assign old values (shifted by 1)
        old_slice = tuple([slice(1, -1)] * self.conv_filter.ndim)
        Y[old_slice] = self.grid
        # Reassign grid
        self.grid = Y

    # Function for occupancy - NNeighbour
    def count_occupancy_nn(self):
        """Count occupancy in nearest places to a position"""

        # Create copy of grid
        Y = self.grid.copy()
        # Perform convolution with a NNEIGH filter.
        #  This effectively correspond to counting the number of occupied seats
        #  next to a particular seat
        Y = convolve(Y, self.conv_filter, mode="constant")
        return Y

    # Function to generate system status
    def generate_status(self):
        """Generate occupancy status for the grid"""
        self.augment()
        Y = self.count_occupancy_nn()

        # Create two masks corresponding to the rules:
        # 1. Occupied tile within tolerance
        # 2. Empty tile with no neighbours
        occupied_mask = ((Y == 2) | (Y == 3)) & (self.grid == 1)
        empty_mask = (Y == 3) & (self.grid == 0)

        # The new status is occupied when empty or occupied mask are valid,
        #  else is inactive
        X_new = np.where(occupied_mask | empty_mask, 1, 0)

        self.idx += 1
        self.grid = X_new


def main():
    input_file = read_input("2020/17/input.txt")
    # Statuses are mapped to 0 or 1
    input_list = [
        list(map(lambda x: 0 if x is EMPTY_CHAR else 1, row)) for row in input_file
    ]

    # Create numpy array of the initial grid and initialize system
    X = np.array(input_list)
    system = CellularAutomataSystem(X, dimension=3)

    # First part
    while system.idx < 6:
        system.generate_status()
    print(f"Result of part 1: {system.grid[system.grid == 1].sum()}")
    # Second part
    system.dimension = 4
    system.reset()
    while system.idx < 6:
        system.generate_status()
    print(f"Result of part 2: {system.grid[system.grid == 1].sum()}")


if __name__ == "__main__":
    main()
