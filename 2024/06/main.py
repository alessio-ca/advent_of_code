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

    def grid_walk(self, move: DirTuple, path: set[CoordTuple]) -> bool:
        loop = False
        while move := self.encounter(move):
            # If the move was already performed,
            # it's a loop
            if move in path:
                loop = True
                break
            path.add(move)
        return loop

    def obtain_positions(self, path: set[DirTuple]) -> int:
        return len(set((x, y) for x, y, _, _ in path))

    def simulate(self, move: DirTuple, new_move: DirTuple, path: set[DirTuple]) -> bool:
        # Keep original i & change grid
        old_i = self.i
        xn, yn, _, _ = new_move
        self.grid[xn][yn] = "#"
        # Simulate if loop, then restore
        loop = self.grid_walk(move, path | set())
        self.i = old_i
        self.grid[xn][yn] = "."
        return loop

    def explore_grid(self) -> tuple[int, int]:
        # Initialize
        self.i = 0
        path = set()
        move = self.guard + self.next_vector()
        checked = set([self.guard])
        loops = 0
        # Loop over moves
        new_move = self.encounter(move)
        while new_move:
            # Check if the new_move position has been checked
            x, y, _, _ = new_move
            if (x, y) not in checked:
                # Change grid and simulate if there is a loop
                loops += 1 if self.simulate(move, new_move, path) else 0
                checked.add((x, y))
            # Otherwise, add move to path and proceed
            path.add(move)
            move = new_move
            new_move = self.encounter(move)
        # Add last move to path
        path.add(move)
        return self.obtain_positions(path), loops


@timefunc
def main(filename: str):
    grid = [list(line) for line in read_input(filename)]
    walker = GridWalker(
        initialize_guard(grid),
        grid,
    )
    positions, loops = walker.explore_grid()
    print(f"Result of part 1: {positions}")
    print(f"Result of part 2: {loops}")


if __name__ == "__main__":
    main("2024/06/input.txt")
