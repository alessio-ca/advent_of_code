"""
--- Day 10: Monitoring Station ---

You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here
 have an emergency: they're having trouble tracking all of the asteroids and can't be
  sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of space; they
 hand you a map of all of the asteroids in that region (your puzzle input).

The map indicates whether each position is empty (.) or contains an asteroid (#). The
 asteroids are much smaller than they appear on the map, and every asteroid is exactly
  in the center of its marked position. The asteroids can be described with X,Y
   coordinates where X is the distance from the left edge and Y is the distance from
    the top edge (so the top-left corner is 0,0 and the position immediately to its
     right is 1,0).

Your job is to figure out which asteroid would be the best place to build a new
 monitoring station. A monitoring station can detect any asteroid to which it has
  direct line of sight - that is, there cannot be another asteroid exactly between them.
   This line of sight can be at any angle, not just lines aligned to the grid or
    diagonally. The best location is the asteroid that can detect the largest number of
     other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##
The best location for a new monitoring station on this map is the highlighted asteroid
 at 3,4 because it can detect 8 asteroids, more than any other location. (The only
  asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by
   the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or
    fewer other asteroids. Here is the number of other asteroids a monitoring station
     on each asteroid could detect:

.7..7
.....
67775
....7
...87
Here is an asteroid (#) and some examples of the ways its line of sight might be
 blocked. If there were another asteroid at the location of a capital letter, the
  locations marked with the corresponding lowercase letter would be blocked and could
   not be detected:

#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c
Here are some larger examples:

Best is 5,8 with 33 other asteroids detected:

......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
Best is 1,2 with 35 other asteroids detected:

#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
Best is 6,3 with 41 other asteroids detected:

.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
Best is 11,13 with 210 other asteroids detected:

.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
Find the best location for a new monitoring station. How many other asteroids can be
 detected from that location?
"""
from utils import read_input
import numpy as np
from typing import List, Tuple


class Map:
    def __init__(self, X: np.array):
        self.initial_grid = X
        self.grid = self.initial_grid.copy()

    def reset(self):
        self.grid = self.initial_grid.copy()

    def count_asteroids(self, x: int, y: int, asteroids: List[Tuple[int]]):
        set_moves = set()
        for x_v, y_v in asteroids:
            if (x_v, y_v) != (x, y):
                x_v -= x
                y_v -= y
                gcd = np.gcd(x_v, y_v)
                set_moves.add((x_v // gcd, y_v // gcd))
        return set_moves

    # Function to count the number of asteroids
    def find_best_asteroid(self):
        """Count the number of asteroids seen by a position"""

        X_asteroids = self.grid.nonzero()
        # Perform crawling over each x,y position of the grid
        # Record the coordinates nearest valid asteroid in each direction
        #  in row_list and col_list
        asteroid_count = np.zeros(shape=self.grid.shape, dtype=np.int64)
        for x_s, y_s in zip(*X_asteroids):
            set_moves = self.count_asteroids(x_s, y_s, zip(*X_asteroids))
            asteroid_count[x_s, y_s] = len(set_moves)

        return asteroid_count

    def vaporize_asteroid(self, x: int, y: int, target: int):
        """Vaporize until a certain asteroid"""
        destroyed = 0
        while destroyed < target:
            # Count asteroids to destory in one round and update destroyed num
            X_asteroids = self.grid.nonzero()
            asteroids = self.count_asteroids(x, y, zip(*X_asteroids))
            destroyed += len(asteroids)
            # Obtain asteroid positions
            pos_asteroids = []
            for idx, idy in asteroids:
                i = 1
                while self.grid[x + i * idx, y + i * idy] != 1:
                    i += 1

                pos_asteroids.append((x + i * idx, y + i * idy))
            idx, idy = np.transpose(pos_asteroids)
            # Update grid
            self.grid[idx, idy] = 0

        # Revert last round (since we hit target)
        destroyed -= len(asteroids)
        self.grid[idx, idy] = 1
        # Get asteroids destroyed in the last round into an array
        X_asteroids = np.array(list(asteroids), dtype=np.int64)
        # Since we are already indexing row-by-column, results are already rotated by 90
        # (so that the first point to be vaporized will be [-1,0])
        # Simply sort clockwise (using arctan to sort from [-1,0] descending)
        idx_sort = np.flip(np.argsort(np.arctan2(X_asteroids[:, 1], X_asteroids[:, 0])))
        # Find ID of the `target` asteroid
        res = X_asteroids[idx_sort[(target - destroyed) - 1]]
        i = 1
        while self.grid[x + i * res[0], y + i * res[1]] != 1:
            i += 1
        return i * res + np.array([x, y])


def main():
    input_file = read_input("2019/10/input.txt")
    # Statuses are mapped to 0 if empty, 1 if asteroid
    input_list = [list(map(lambda x: 0 if x == "." else 1, row)) for row in input_file]
    # Create numpy array of the initial grid and initialize system
    X = np.array(input_list)
    mapmap = Map(X)
    # Get the number of asteroids detected per location
    detected_asteroids = mapmap.find_best_asteroid()
    print(f"Result of part 1: {np.max(detected_asteroids)}")

    # Find best position
    x_best, y_best = np.unravel_index(
        np.argmax(detected_asteroids), detected_asteroids.shape
    )
    target = mapmap.vaporize_asteroid(x_best, y_best, 200)
    print(f"Result of part 2: {target[1] * 100 + target[0]}")


if __name__ == "__main__":
    main()
