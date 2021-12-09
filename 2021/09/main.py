"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small
 hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it
 and be that much safer. The submarine generates a heightmap of the floor of the nearby
  caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the
 following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678
Each number corresponds to the height of a particular location, where 9 is the highest
 and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of
 its adjacent locations. Most locations have four adjacent locations (up, down, left,
  and right); locations on the edge or corner of the map have three or two adjacent
   locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first
 row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a
  5). All other locations on the heightmap have some lower adjacent location, and so
   are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk
 levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low
  points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all
 low points on your heightmap?

--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to
 avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore,
 every low point has a basin, although some basins are very small. Locations of height
  9 do not count as being in any basin, and all other locations will always be part of
   exactly one basin.

The size of a basin is the number of locations within the basin, including the low
 point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example,
 this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""
from utils import read_input
import numpy as np
import itertools


def calculate_basin(i: int, j: int, X: np.ndarray) -> int:
    """Recursive function to calculate the basin size"""
    # If location has height 9 or has been already visited (height -1), return 0
    if X[i, j] == 9 or X[i, j] == -1:
        return 0

    # Mark current height location as -1 (visited)
    X[i, j] = -1

    # Generate possible neighbors
    neighbors = list(itertools.product([i - 1, i + 1], [j])) + list(
        itertools.product([i], [j - 1, j + 1])
    )
    # Contrain neighbors bounds
    neighbors = [
        pair
        for pair in neighbors
        if (pair[0] >= 0)
        & (pair[0] < X.shape[0])
        & (pair[1] >= 0)
        & (pair[1] < X.shape[1])
    ]
    # Recursive call
    return 1 + sum(calculate_basin(ii, jj, X) for ii, jj in neighbors)


def main():
    input_file = read_input("2021/09/input.txt")
    X = np.array([[int(x) for x in line] for line in input_file], dtype=int)
    # Initialize mask of ones
    mask = np.ones(X.shape, dtype=int)

    # Construct mask. Visiting each position, the mask is converted to 0 if any of the
    #  neighbors is lower than the current position. Implemented in a vectorized manner.
    # Loop over rows
    for i in range(1, X.shape[0]):
        # Top
        mask[i, :] = (X[i - 1, :] > X[i, :]) * mask[i, :]
        # Bottom
        mask[i - 1, :] = (X[i, :] > X[i - 1, :]) * mask[i - 1, :]
    # Loop over columns
    for i in range(1, X.shape[1]):
        # Left
        mask[:, i] = (X[:, i - 1] > X[:, i]) * mask[:, i]
        # Right
        mask[:, i - 1] = (X[:, i] > X[:, i - 1]) * mask[:, i - 1]

    print(f"Result of part 1: {((X + 1) * mask).sum()}")

    # Get indices of non null elements in mask
    low_idx = np.argwhere(mask == 1)

    # Calculate basin sizes
    sizes = []
    for i, j in low_idx:
        X_temp = X.copy()
        sizes.append(calculate_basin(i, j, X_temp))
    print(f"Result of part 2: {np.prod(sorted(sizes)[-3:])}")


if __name__ == "__main__":
    main()
