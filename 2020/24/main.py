import re
from typing import List, Tuple

import numpy as np
from scipy.ndimage import convolve

from utils import read_input

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
