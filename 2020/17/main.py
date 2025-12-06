import numpy as np
from scipy.ndimage import convolve

from utils import read_input

EMPTY_CHAR = "."
FULL_CHAR = "#"


class CellularAutomataSystem:
    def __init__(self, X: np.ndarray, dimension: int = 3):
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
