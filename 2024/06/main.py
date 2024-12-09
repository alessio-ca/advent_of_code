from utils import read_input, timefunc
from utils import CoordTuple
from typing import Optional

DirTuple = tuple[CoordTuple, CoordTuple]


def initialize_guard(grid: list[list[str]]) -> CoordTuple:
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c == "^":
                return (i, j)


class GridWalker:
    VECTORS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    SIZE_V = len(VECTORS)

    def __init__(
        self,
        start: CoordTuple,
        grid: list[list[str]],
    ) -> None:
        self.grid = grid
        self.guard = start
        self.xg = len(grid)
        self.yg = len(grid[0])

    def next_vector(self) -> CoordTuple:
        # Return next direction
        return self.VECTORS[self.i % self.SIZE_V]

    def encounter(self, move: DirTuple) -> Optional[DirTuple]:
        # Unpack move & check if result is in bounds
        x, y, hx, hy = move
        xn = x + hx
        yn = y + hy
        if not self.check_bounds(xn, yn):
            return None

        # If the result is an obstacle, increase obstacle counter
        # and change direction. Keep existing position
        if self.grid[xn][yn] == "#":
            self.i += 1
            return (x, y) + self.next_vector()
        # Otherwise, return the result and existing direction
        else:
            return (xn, yn, hx, hy)

    def check_bounds(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.xg and y >= 0 and y < self.yg

    def grid_walk(self):
        # Initialize
        self.i = 0
        self.visited = set()
        move = self.guard + self.next_vector()
        self.visited.add(move)
        loop = False
        # Loop over moves
        while move := self.encounter(move):
            # If the move was already performed,
            # it's a loop
            if move in self.visited:
                loop = True
                break
            self.visited.add(move)
        # Return whether it's a loop
        return loop

    def obtain_positions(self):
        return len(set((x, y) for x, y, _, _ in self.visited))

    def explore_grid(self) -> int:
        # Obtain candidates by excluding the initial position
        candidates = set(
            (x, y) for (x, y, _, _) in self.visited if (x, y) != self.guard
        )
        loops = 0
        # Loop over candidates
        for x, y in candidates:
            self.grid[x][y] = "#"
            # If the modified grid creates a loop,
            # increase counter
            if self.grid_walk():
                loops += 1
            self.grid[x][y] = "."
        return loops


@timefunc
def main(filename: str):
    grid = [list(line) for line in read_input(filename)]
    walker = GridWalker(
        initialize_guard(grid),
        grid,
    )
    walker.grid_walk()
    print(f"Result of part 1: {walker.obtain_positions()}")
    print(f"Result of part 2: {walker.explore_grid()}")


if __name__ == "__main__":
    main("2024/06/input.txt")
