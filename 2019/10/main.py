from typing import List, Tuple

import numpy as np

from utils import read_input


class Map:
    def __init__(self, X: np.ndarray):
        self.initial_grid = X
        self.grid = self.initial_grid.copy()

    def reset(self):
        self.grid = self.initial_grid.copy()

    def count_asteroids(self, x: int, y: int, asteroids: List[Tuple[int, int]]):
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
            asteroids = self.count_asteroids(x, y, list(zip(*X_asteroids)))
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
        asteroids_array = np.array(list(asteroids), dtype=np.int64)
        # Since we are already indexing row-by-column, results are already rotated by 90
        # (so that the first point to be vaporized will be [-1,0])
        # Simply sort clockwise (using arctan to sort from [-1,0] descending)
        idx_sort = np.flip(
            np.argsort(np.arctan2(asteroids_array[:, 1], asteroids_array[:, 0]))
        )
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
