from __future__ import annotations

"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus refuelling
 station. During the rush back on Earth, the fuel management system wasn't completely
  installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are
 connected to a central port and extend outward on a grid. You trace the path each wire
  takes as it leaves the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the
 circuit, you need to find the intersection point closest to the central port. Because
  the wires are on a grid, use the Manhattan distance for this measurement. While the
   wires do technically cross right at the central port where they both start, this
    point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central
 port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........
Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left
 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
These wires cross at two locations (marked X), but the lower-left one is closer to the
 central port: its distance is 3 + 3 = 6.

Here are a few more examples:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
What is the Manhattan distance from the central port to the closest intersection?

--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to minimize
 the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection;
 choose the intersection where the sum of both wires' steps is lowest. If a wire visits
  a position on the grid multiple times, use the steps value from the first time it
   visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has
 entered to get to that location, including the intersection being considered. Again
  consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........
In the above example, the intersection closest to the central port is reached after
 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a
  total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and
 the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
What is the fewest combined steps the wires must take to reach an intersection?
"""
from utils import read_input
from typing import List, Tuple
from itertools import product

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

    def find_steps(self, point: Tuple[int]):
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
