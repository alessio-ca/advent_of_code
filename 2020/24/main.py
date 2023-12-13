"""
--- Day 24: Lobby Layout ---

Your raft makes it to the tropical island; it turns out that the small crab was an
 excellent navigator. You make your way to the resort.

As you enter the lobby, you discover a small problem: the floor is being renovated. You
 can't even reach the check-in desk until they've finished installing the new tile
  floor.

The tiles are all hexagonal; they need to be arranged in a hex grid with a very
 specific color pattern. Not in the mood to wait, you offer to help figure out the
  pattern.

The tiles are all white on one side and black on the other. They start with the white
 side facing up. The lobby is large enough to fit whatever pattern might need to appear
  there.

A member of the renovation crew gives you a list of the tiles that need to be flipped
 over (your puzzle input). Each line in the list identifies a single tile that needs to
  be flipped by giving a series of steps starting from a reference tile in the very
   center of the room. (Every line starts from the same reference tile.)

Because the tiles are hexagonal, every tile has six neighbors: east, southeast,
 southwest, west, northwest, and northeast. These directions are given in your list,
  respectively, as e, se, sw, w, nw, and ne. A tile is identified by a series of these
   directions with no delimiters; for example, esenee identifies the tile you land on
    if you start at the reference tile and then move one tile east, one tile southeast,
     one tile northeast, and one tile east.

Each time a tile is identified, it flips from white to black or from black to white.
 Tiles might be flipped more than once. For example, a line like esew flips a tile
  immediately adjacent to the reference tile, and a line like nwwswee flips the
   reference tile itself.

Here is a larger example:

sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
In the above example, 10 tiles are flipped once (to black), and 5 more are flipped
 twice (to black, then back to white). After all of these instructions have been
  followed, a total of 10 tiles are black.

Go through the renovation crew's list and determine which tiles they need to flip.
 After all of the instructions have been followed, how many tiles are left with the
  black side up?

--- Part Two ---

The tile floor in the lobby is meant to be a living art exhibit. Every day, the tiles
 are all flipped according to the following rules:

Any black tile with zero or more than 2 black tiles immediately adjacent to it is
 flipped to white.
Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to
 black.
Here, tiles immediately adjacent means the six tiles directly touching the tile in
 question.

The rules are applied simultaneously to every tile; put another way, it is first
 determined which tiles need to be flipped, then they are all flipped at the same time.

In the above example, the number of black tiles that are facing up after the given
 number of days has passed is as follows:

Day 1: 15
Day 2: 12
Day 3: 25
Day 4: 14
Day 5: 23
Day 6: 28
Day 7: 41
Day 8: 37
Day 9: 49
Day 10: 37

Day 20: 132
Day 30: 259
Day 40: 406
Day 50: 566
Day 60: 788
Day 70: 1106
Day 80: 1373
Day 90: 1844
Day 100: 2208
After executing this process a total of 100 times, there would be 2208 black tiles
 facing up.

How many tiles will be black after 100 days?
"""
from utils import read_input
import re
from typing import List, Tuple
import numpy as np
from scipy.ndimage import convolve

# Dictionary of directions in an HEX cartesian system
DICT_DIRECTIONS = {
    "e": (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
}


class Grid:
    def __init__(self, instructions: List[Tuple[int]]):
        self.grid_size = max(len(line) for line in instructions)
        # Construct array of instructions
        array_instr = [np.array(line) for line in instructions]
        # Pad
        for i, array in enumerate(array_instr):
            array_instr[i] = np.pad(
                array, ((0, self.grid_size - array.shape[0]), (0, 0))
            )
        # Define instructions as a 3D array
        self.instructions = np.stack(array_instr)

        # Initialise grid
        self.grid = np.ones(shape=(2 * self.grid_size + 1, 2 * self.grid_size + 1))
        # Define starting tile
        self.start = [self.grid_size, self.grid_size]
        # Flip tiles -- start flip
        self.start_flip()
        # Define NN conv filter in HEX cartesian system
        self.conv_filter = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype="int")

        # Define counter
        self.idx = 0

    def start_flip(self):
        """Function to flip tiles according to instructions"""
        # Sum the instructions
        instructions = self.instructions.sum(axis=1)
        # For each instruction, perform flip
        for instruction in instructions:
            current_value = self.grid[tuple(self.start + instruction)]
            self.grid[tuple(self.start + instruction)] = 1 if not current_value else 0

    def augment(self):
        """Function to augment grid in all dimensions"""
        # Define new shape
        self.grid_size = self.grid_size + 1
        # Initialize new grid
        Y = np.ones(shape=(2 * self.grid_size + 1, 2 * self.grid_size + 1))
        # Assign old values (shifted by 1)
        old_slice = tuple([slice(1, -1)] * self.conv_filter.ndim)
        Y[old_slice] = self.grid
        # Reassign grid
        self.grid = Y

    def count_occupancy_nn(self):
        """Count occupancy in nearest places to a position"""

        # Create copy of grid
        Y = self.grid.copy()
        # Perform convolution with a NNEIGH filter.
        #  This effectively correspond to counting the number of occupied seats
        #  next to a particular seat
        Y = convolve(Y, self.conv_filter, mode="constant", cval=1)
        return Y

    # Function to generate system status
    def generate_status(self):
        """Generate occupancy status for the grid"""
        self.augment()
        Y = self.count_occupancy_nn()

        # Create two masks corresponding to the rules:
        # 1. Zero tiles with neighbours
        # 2. Empty tile with no neighbours
        zero_mask = ((Y == 6) | (Y < 4)) & (self.grid == 0)
        ones_mask = (Y == 4) & (self.grid == 1)

        # The new status is one when zero or occupied mask are valid,
        #  else is inactive
        X_new = np.where(zero_mask, 1, self.grid)
        X_new = np.where(ones_mask, 0, X_new)

        self.idx += 1
        self.grid = X_new


def main():
    input_file = read_input("2020/24/input.txt")
    # Parse instructions
    instructions = [
        list(map(DICT_DIRECTIONS.get, re.findall(r"(e|se|sw|w|nw|ne)", line)))
        for line in input_file
    ]
    # Define Grid
    gridgrid = Grid(instructions)
    print(f"Result of part 1: {np.nansum(gridgrid.grid == 0)}")

    while gridgrid.idx < 100:
        gridgrid.generate_status()
    print(f"Result of part 2: {np.nansum(gridgrid.grid == 0)}")


if __name__ == "__main__":
    main()
