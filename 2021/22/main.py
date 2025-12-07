import re
from typing import Optional

from utils import read_input, timefunc


class CubeSystem:
    def __init__(self, cubes, bounded=True):
        self.cubes = cubes.copy()
        self.bounded = bounded
        self.recount_cubes = []
        self.filter()

    def filter(self):
        # Filter out the -50 to 50 region
        if self.bounded:
            valid_cubes = []
            while len(self.cubes) > 0:
                cube = self.cubes.pop()
                edges = map(
                    abs,
                    [coord for edge in [cube.x, cube.y, cube.z] for coord in edge],
                )

                if not any(coord > 50 for coord in edges):
                    valid_cubes.append(cube)

            valid_cubes.reverse()
            self.cubes = valid_cubes
        return self

    def execute(self):
        # recount_cubes starts as an empty list and will initialize itself with the
        #  first cube with ON.
        # From there, each new cube in self.cubes will check the past (recount) element.
        #  When an overlap is found, the next element in self.cubes will check the
        #  overlap cube first, then the original element again if it was ON.
        # Similar to recursion.
        for i, cube in enumerate(self.cubes):
            temp_cubes = []
            for past_cube in self.recount_cubes:
                new_cube = cube.overlap(past_cube)
                if new_cube:
                    #  If there is overlap, append to the list of temporary new cubes
                    temp_cubes.append(new_cube)

            # If the current switch is ON, add it to the recount list first as it needs
            #  to be reprocessed to balance the count
            if cube.switch:
                self.recount_cubes.append(cube)
            #  Then, add all the overlaps
            self.recount_cubes += temp_cubes

        # recount_cubes now contains all cubes for counting
        total = 0
        for cube in self.recount_cubes:
            total += cube.n_points() * (-1 + 2 * cube.switch)

        return total


class Cube:
    def __init__(self, x, y, z, switch):
        self.x = x
        self.y = y
        self.z = z
        self.switch = switch

    def overlap(self, next_cube: "Cube") -> Optional["Cube"]:
        # Check if overlap
        if next_cube.x[0] > self.x[1] or self.x[0] > next_cube.x[1]:
            return None
        if next_cube.y[0] > self.y[1] or self.y[0] > next_cube.y[1]:
            return None
        if next_cube.z[0] > self.z[1] or self.z[0] > next_cube.z[1]:
            return None

        # Get the new interval
        x_new = (max(self.x[0], next_cube.x[0]), min(self.x[1], next_cube.x[1]))
        y_new = (max(self.y[0], next_cube.y[0]), min(self.y[1], next_cube.y[1]))
        z_new = (max(self.z[0], next_cube.z[0]), min(self.z[1], next_cube.z[1]))

        # The overlap is needed to balance the counts, using its status.
        # Swap the switch to normalize the count: if both cubes are ON, it will be
        #  marked as OFF and viceversa
        # Two OFF cubes also are double-counting (same as two ON cubes) because you
        #  can't substract the count twice
        if self.switch == next_cube.switch:
            switch_new = not self.switch

        # If the two switches are different, then follow the rule: we need to balance
        #  the count.
        #  So swap according to what the new one in line is gonna be
        else:
            # If the next cube is ON, then it's an OFF and viceversa
            switch_new = not next_cube.switch

        new_cube = Cube(x_new, y_new, z_new, switch_new)

        return new_cube

    def n_points(self):
        # Calculate the cube's number of points
        n_points = (
            (self.x[1] - self.x[0] + 1)
            * (self.y[1] - self.y[0] + 1)
            * (self.z[1] - self.z[0] + 1)
        )
        return n_points


@timefunc
def main():
    input_file = read_input("2021/22/input.txt")
    switches = []
    x_edges = []
    y_edges = []
    z_edges = []
    for switch, coords in [line.split(" ") for line in input_file]:
        switches.append(0 if switch == "off" else 1)
        x_min, x_max, y_min, y_max, z_min, z_max = tuple(
            map(int, re.findall("-?[0-9]+", coords))
        )
        x_edges.append((x_min, x_max))
        y_edges.append((y_min, y_max))
        z_edges.append((z_min, z_max))

    cubes = [
        Cube(x, y, z, switch)
        for x, y, z, switch in zip(x_edges, y_edges, z_edges, switches)
    ]

    system = CubeSystem(cubes)
    res = system.execute()
    print(f"Result of part 1: {res}")

    system = CubeSystem(cubes, bounded=False)
    res = system.execute()
    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main()
