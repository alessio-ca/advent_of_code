"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents constantly
 produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of
 vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1
 are the coordinates of one end the line segment and x2,y2 are the coordinates of the
  other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either
 x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following
 diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
 Each position is shown as the number of lines which cover that point or . if no line
  covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the
   very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at
 least two lines overlap. In the above example, this is anywhere in the diagram with a
  2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines
 overlap?


--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you the full
 picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list
 will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees.
  In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap.
 In the above example, this is still anywhere in the diagram with a 2 or larger - now a
  total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""
from utils import read_input
import numpy as np


def populate_matrix(
    p1: np.ndarray, p2: np.ndarray, diagonal: bool = False
) -> np.ndarray:
    # Create empty matrix
    X = np.zeros(
        shape=(
            max(p1[:, 1].max() + 1, p2[:, 1].max() + 1),
            max(p1[:, 0].max() + 1, p2[:, 0].max() + 1),
        )
    )
    # Loop over points
    for pp1, pp2 in zip(p1, p2):
        min_x, max_x = min(pp1[1], pp2[1]), max(pp1[1], pp2[1])
        min_y, max_y = min(pp1[0], pp2[0]), max(pp1[0], pp2[0])

        # If horiz or vertical line, simply add one to all points on the line
        if (min_x == max_x) | (min_y == max_y):
            X[min_x : max_x + 1, min_y : max_y + 1] += 1

        # If diagonal, generate points on the diagonal line
        else:
            if diagonal:
                # Create view of the area where the diagonal lives
                X_temp = X[min_x : max_x + 1, min_y : max_y + 1]
                # Create a identity matrix mask
                mask = np.eye(len(X_temp), dtype=bool)
                # Flip the mask depending on the points arrangement
                if (pp2[0] < pp1[0]) != (pp2[1] < pp1[1]):
                    mask = np.fliplr(mask)
                # Add oone to the points on the line
                X_temp[mask] += 1
            else:
                pass
    return X


def main():
    input_file = read_input("2021/05/input.txt")
    p1 = []
    p2 = []
    for line in input_file:
        p1.append(list(map(int, line.split(" ")[0].split(","))))
        p2.append(list(map(int, line.split(" ")[2].split(","))))

    p1 = np.array(p1)
    p2 = np.array(p2)

    # For part 1, diagonals are disabled by default
    X = populate_matrix(p1, p2)
    print(f"Result of part 1: {(X>1).sum()}")

    # For part 2, diagonals are enabled
    X = populate_matrix(p1, p2, diagonal=True)
    print(f"Result of part 2: {(X>1).sum()}")


if __name__ == "__main__":
    main()
