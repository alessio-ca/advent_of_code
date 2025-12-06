from __future__ import annotations
from itertools import product
from typing import List, Tuple
from utils import read_input

DICT_MOVES = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}


class Wire:
    def __init__(self, path: List[Tuple[str, int]]):
        self.path = path
        self.compute_locations()
        self.compute_points()

    def compute_locations(self):
        # For each location in the path, transform the path in a dictionary of the form
        #  {idx: (x, y)}
        self.dict_locations = {0: (0, 0)}
        for i in range(1, len(self.path) + 1):
            prev_x, prev_y = self.dict_locations[i - 1]
            move = DICT_MOVES[self.path[i - 1][0]]
            value = self.path[i - 1][1]
            self.dict_locations[i] = (
                prev_x + value * move[0],
                prev_y + value * move[1],
            )

    def compute_points(self):
        # For each location in the path, compute the set of points in the segment
        #  leading to this location
        self.dict_points = {}
        for i in range(0, len(self.path)):
            # Fetch current and next location
            current_x, current_y = self.dict_locations[i]
            next_x, next_y = self.dict_locations[i + 1]
            # Compute min and max of the x and y values
            min_x, max_x = min(current_x, next_x), max(current_x, next_x)
            min_y, max_y = min(current_y, next_y), max(current_y, next_y)
            # Generate a list of all the points visited on the x and y axes
            points_x = list(range(min_x, max_x + 1))
            points_y = list(range(min_y, max_y + 1))
            # Assign it to the dictionary
            self.dict_points[i] = set(product(points_x, points_y))

    def intersection(self, wire: Wire):
        # Compute the overall set of points visited during the path
        # for the two wires
        points_1 = set.union(*self.dict_points.values())
        points_2 = set.union(*wire.dict_points.values())
        # Compute intersection -- remove the origin point
        return set.intersection(points_1, points_2) - set({(0, 0)})

    def find_steps(self, point: Tuple[int, int]):
        steps = 0
        # Loop through the dictionary of points
        for i, points in self.dict_points.items():
            # If point is in here,
            if point in points:
                x, y = point
                prev_x, prev_y = self.dict_locations[i]
                # Steps is the sum of the previous steps and the number of steps to get
                #  to `point` from the previous location
                return steps + max(abs(x - prev_x), abs(y - prev_y))
            else:
                # Update steps with the number of points (-1 for the start-point)
                steps += len(points) - 1

        return -1


def main():
    input_file = read_input("2019/03/input.txt")
    paths = [
        [(move[0], int(move[1:])) for move in line.split(",")] for line in input_file
    ]
    # Declare wires
    wire_1 = Wire(paths[0])
    wire_2 = Wire(paths[1])
    # Compute minimum distance
    intersection_set = wire_1.intersection(wire_2)
    min_dist = min(map(sum, [(abs(x), abs(y)) for x, y in intersection_set]))
    print(f"Result of part 1: {min_dist}")

    # Obtain steps
    wire_1_steps = [wire_1.find_steps(point) for point in intersection_set]
    wire_2_steps = [wire_2.find_steps(point) for point in intersection_set]
    min_steps = min(map(sum, zip(wire_1_steps, wire_2_steps)))
    print(f"Result of part 2: {min_steps}")


if __name__ == "__main__":
    main()
