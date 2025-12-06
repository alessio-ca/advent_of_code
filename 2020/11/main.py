import numpy as np
from scipy.signal import convolve2d
from scipy.sparse import csr_matrix

from utils import read_input

EMPTY_SEAT_CHAR = "L"
FLOOR_CHAR = "."
MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
CONV_FILTER = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


class CellularAutomataSystem:
    def __init__(self, X: np.ndarray, tolerance: int = 4, style="nn"):
        self.initial_grid = X
        self.grid = self.initial_grid.copy()
        self.kernels = self.kernel_stack()
        self.tolerance = tolerance
        if style not in ["nn", "los"]:
            raise Exception(f"Nearest Neighbour counting style {style} is not defined")
        self.style = style
        self.equilibrium = 0

    def reset(self):
        self.grid = self.initial_grid.copy()
        self.equilibrium = 0

    # Function to create a kernel stack as a sparse matrix
    def kernel_stack(self):
        """Construct a stack of kernels, one for each position in the grid.
        Elements are 1 if they correspond to the closest VALID (i.e. non-floor)
        seat to a particular position, 0 otherwise

        The stack is saved as a sparse matrix.
        """
        height, width = self.initial_grid.shape
        # Unroll the grid to a 1D array
        X_unroll = self.initial_grid.ravel()

        # Redefine as boolean mask for valid seats
        #  (i.e. empty or occupied, not floor)
        X_unroll = X_unroll >= 0

        row_list = []
        col_list = []
        # Perform crawling over each x,y position of the grid
        # Record the coordinates nearest valid seat in each direction
        #  in row_list and col_list
        for y_s in range(height):
            for x_s in range(width):
                # This is the row coordinate in unrolled form
                row_coord = y_s * width + x_s
                # loop over the available moves
                for i, j in MOVES:
                    x = x_s + i
                    y = y_s + j
                    # Check for boundaries
                    while 0 <= x < width and 0 <= y < height:
                        # This is the column coordinate in unrolled form
                        col_coord = y * width + x
                        if X_unroll[col_coord]:
                            # If the seat is valid,
                            #  record the row and col coordinates
                            row_list.append(row_coord)
                            col_list.append(col_coord)
                            break
                        x += i
                        y += j
        # Create sparse matrix from the row and coordinate lists
        # The matrix has shape (height*width, height*width)
        # i.e. it contains an unrolled matrix for each position in the grid
        row_array = np.array(row_list)
        col_array = np.array(col_list)
        data = np.ones(shape=row_array.shape)
        kernel_matrix = csr_matrix(
            (data, (row_array, col_array)),
            shape=(
                height * width,
                height * width,
            ),
        )
        return kernel_matrix

    # Function for occupancy - NNeighbour
    def count_occupancy_nn(self):
        """Count occupancy in nearest tiles to a seat"""

        # Create copy of grid
        Y = self.grid.copy()
        # To count occupancy, floor tiles are the same as empty.
        # Convert them to 0
        Y[self.grid == -1] = 0
        # Perform convolution with a NNEIGH filter.
        #  This effectively correspond to counting the number of occupied seats
        #  next to a particular seat
        Y = convolve2d(Y, CONV_FILTER, mode="same", boundary="fill", fillvalue=0)
        return Y

    # Function for occupancy - Line Of Sight
    def count_occupancy_los(self):
        """Count occupancy in line-of-sight tiles to a seat"""

        # Create copy of grid
        Y = self.grid.copy()
        # To count occupancy, floor tiles are the same as empty.
        # Convert them to 0
        Y[self.grid == -1] = 0

        # Unroll the grid
        Y = Y.ravel()

        # Perform the cross product of the unrolled grid with the kernels
        #  containing the line-of-sight closest seats to each grid position
        #  This effectively correspond to counting the number of occupied seats
        #  in line of sight to a particular seat
        return self.kernels.dot(Y).reshape(self.grid.shape)

    # Function to generate system status
    def generate_status(self):
        """Generate occupancy status for the grid"""

        # Compute the occupancy number
        if self.style == "los":
            Y = self.count_occupancy_los()
        elif self.style == "nn":
            Y = self.count_occupancy_nn()

        # Create two masks corresponding to the rules:
        # 1. Occupied tile within tolerance
        # 2. Empty tile with no neighbours
        occupied_mask = (Y >= self.tolerance) & (self.grid == 1)
        empty_mask = (Y == 0) & (self.grid == 0)

        # The new status is occupied if empty_mask is valid
        #  and empty if occupied_mask is valid.
        #  Else, it remains unchanged
        X_new = np.where(empty_mask, 1, self.grid)
        X_new = np.where(occupied_mask, 0, X_new)

        self.equilibrium = np.array_equal(self.grid, X_new)
        self.grid = X_new


def main():
    input_file = read_input("2020/11/input.txt")
    # Statuses are mapped to -1 if floor, 0 if empty seat
    input_list = [
        list(map(lambda x: 0 if x is EMPTY_SEAT_CHAR else -1, row))
        for row in input_file
    ]

    # Create numpy array of the initial grid and initialize system
    X = np.array(input_list)
    system = CellularAutomataSystem(X)

    # First part
    system.style = "nn"
    system.tolerance = 4
    while not system.equilibrium:
        system.generate_status()
    print(f"Result of part 1: {system.grid[system.grid == 1].sum()}")

    # Second part
    system.reset()
    system.style = "los"
    system.tolerance = 5
    while not system.equilibrium:
        system.generate_status()
    print(f"Result of part 2: {system.grid[system.grid == 1].sum()}")


if __name__ == "__main__":
    main()
