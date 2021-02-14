"""
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare. The final leg of your journey
 is a ferry that goes directly to the tropical island where you can finally
  start your vacation. As you reach the waiting area to board the ferry, you
   realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the
 waiting area, you're pretty sure you can predict the best place to sit. You
  make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an
 empty seat (L), or an occupied seat (#). For example, the initial seat layout
  might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly.
 Fortunately, people are entirely predictable and always follow a simple set
  of rules. All decisions are based on the number of occupied seats adjacent
   to a given seat (one of the eight positions immediately up, down, left,
    right, or diagonal from the seat). The following rules are applied to
     every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the
 seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also
 occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes
 occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats
 become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further
 applications of these rules cause no seats to change state! Once people stop
  moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no
 seats change state. How many seats end up occupied?

--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just
 care about adjacent seats - they care about the first seat they can see in
  each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats,
 consider the first seat in each of those eight directions. For example, the
  empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see
 any of the occupied ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or
 more visible occupied seats for an occupied seat to become empty (rather than
  four or more from the previous rules). The other rules still apply: empty
   seats that see no occupied seats become occupied, seats matching no rule
    don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating
 area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches
 equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats
 becoming empty, once equilibrium is reached, how many seats end up occupied?
"""
import numpy as np
from scipy.signal import convolve2d
from scipy.sparse import csr_matrix
from utils import read_input

EMPTY_SEAT_CHAR = "L"
FLOOR_CHAR = "."
MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
CONV_FILTER = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


class CellularAutomataSystem:
    def __init__(self, X: np.array, tolerance: str = 4, style="nn"):
        self.initial_grid = X
        self.grid = self.initial_grid.copy()
        self.kernels = self.kernel_stack()
        self.tolerance = tolerance
        if style not in ["nn", "los"]:
            # fmt: off
            raise Exception(
                "Nearest Neighbour counting style"
                f" {style} is not defined"
            )
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
        Y = convolve2d(Y, CONV_FILTER, mode="same", boundary="fill", fillvalue=0)  # noqa: E501
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
        if self.style == 'los':
            Y = self.count_occupancy_los()
        elif self.style == 'nn':
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
    while not system.equilibrium:
        system.generate_status()
    print(f"First answer: {system.grid[system.grid == 1].sum()}")

    # Second part
    system.reset()
    system.style = 'los'
    system.tolerance = 5
    while not system.equilibrium:
        system.generate_status()
    print(f"Second answer: {system.grid[system.grid == 1].sum()}")


if __name__ == "__main__":
    main()
