from collections import deque

from utils import CoordTuple, cached_add_tuples, read_input_batch


def warehouse(filename: str) -> tuple[list[list[str]], str]:
    map_raw, moves_raw = read_input_batch(filename)
    map = [list(line) for line in map_raw]
    moves = "".join(move for move in moves_raw)
    return map, moves


def big_warehouse(filename: str) -> tuple[list[list[str]], str]:
    map, moves = warehouse(filename)
    xg = len(map)
    yg = len(map[0])
    big_map = [2 * yg * [""] for _ in range(xg)]
    for i in range(len(map)):
        for j in range(len(map[0])):
            sym = map[i][j]
            if sym == "O":
                big_map[i][2 * j] = "["
                big_map[i][2 * j + 1] = "]"
            elif sym == "@":
                big_map[i][2 * j] = sym
                big_map[i][2 * j + 1] = "."
            else:
                big_map[i][2 * j] = sym
                big_map[i][2 * j + 1] = sym
    return big_map, moves


def initialize_robot(grid: list[list[str]]) -> CoordTuple:
    for i, line in enumerate(grid):
        for j, c in enumerate(line):
            if c == "@":
                return (i, j)
    return -1, -1


class RobotWalker:
    VECTORS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

    def __init__(self, filename: str, init_fun) -> None:
        self.grid, self.moves = init_fun(filename)
        self.robot = initialize_robot(self.grid)
        self.xg = len(self.grid)
        self.yg = len(self.grid[0])

    def move(self, moves: dict[CoordTuple, str], move: CoordTuple) -> None:
        # Reset grid positions
        for x, y in moves:
            self.grid[x][y] = "."
        # Assign new positions
        for pos, grid_value in moves.items():
            xn, yn = cached_add_tuples(pos, move)
            self.grid[xn][yn] = grid_value

    def attempt_move(
        self, pos: CoordTuple, move: CoordTuple
    ) -> dict[CoordTuple, str] | None:
        queue = deque([pos])
        moves: dict[CoordTuple, str] = dict()
        while queue:
            # Pop a position to check
            x, y = queue.pop()
            if (x, y) not in moves:
                # If there is an obstacle/robot, add to moves
                if (grid_value := self.grid[x][y]) != ".":
                    moves[(x, y)] = grid_value
                    if (grid_value == "O") | (grid_value == "@"):
                        # There is a box or robot at xn, yn
                        queue.append(cached_add_tuples((x, y), move))
                    elif grid_value == "[":
                        # There is a bigbox at xn, [yn, yn + 1]
                        # Check neighbor and rest of box
                        queue.append(cached_add_tuples((x, y), move))
                        queue.append((x, y + 1))
                    elif grid_value == "]":
                        # There is a bigbox at xn, [yn, yn - 1]
                        # Check neighbor and rest of box
                        queue.append(cached_add_tuples((x, y), move))
                        queue.append((x, y - 1))
                    elif grid_value == "#":
                        # There is a wall - we can't perform this move
                        return None

        # Once all possible moves have been checked,
        #  return the dict of moves to perform
        return moves

    def walk(self) -> None:
        for _, move in enumerate(self.moves):
            if moves := self.attempt_move(self.robot, self.VECTORS[move]):
                self.move(moves, self.VECTORS[move])
                self.robot = cached_add_tuples(self.robot, self.VECTORS[move])

    def return_gps(self, pos: CoordTuple) -> int:
        return 100 * pos[0] + pos[1]

    def calculate_gps_map(self) -> int:
        sum = 0
        for x in range(self.xg):
            for y in range(self.yg):
                if (self.grid[x][y] == "O") | (self.grid[x][y] == "["):
                    sum += self.return_gps((x, y))
        return sum


def main(filename: str):
    walker = RobotWalker(filename, warehouse)
    walker.walk()
    print(f"Result of part 1: {walker.calculate_gps_map()}")
    walker = RobotWalker(filename, big_warehouse)
    walker.walk()
    print(f"Result of part 2: {walker.calculate_gps_map()}")


if __name__ == "__main__":
    main("2024/15/input.txt")
