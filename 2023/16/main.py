from collections import deque

from utils import read_input, timefunc


def encounter(x, y, hx, hy, grid):
    element = grid[x][y]
    if element == "\\":
        return [(hy, hx)]
    elif element == "/":
        return [(-hy, -hx)]
    elif element == "|" and (hx == 0):
        return [(1, 0), (-1, 0)]
    elif element == "-" and (hy == 0):
        return [(0, 1), (0, -1)]
    else:
        return [(hx, hy)]


def check_bounds(x, y, xg, yg):
    return x >= 0 and x < xg and y >= 0 and y < yg


def laser_walk(grid, start, head):
    xg, yg = len(grid), len(grid[0])
    queue = deque([start + head])
    visited = {start + head}

    while queue:
        x, y, hx, hy = queue.pop()
        new_heads = encounter(x, y, hx, hy, grid)
        for hnx, hny in new_heads:
            xn = x + hnx
            yn = y + hny
            if (xn, yn, hnx, hny) not in visited and check_bounds(xn, yn, xg, yg):
                queue.append((xn, yn, hnx, hny))
                visited.add((xn, yn, hnx, hny))

    return len(set([(x, y) for x, y, _, _ in visited]))


def generate_starts(grid):
    shape = len(grid), len(grid[0])
    for i in range(shape[0]):
        yield ((i, 0), (0, 1))
        yield ((i, shape[1] - 1), (0, -1))
    for i in range(shape[1]):
        yield ((0, i), (1, 0))
        yield ((shape[0] - 1, i), (-1, 0))


@timefunc
def main(filename: str):
    grid = read_input(filename)
    print(f"Result of part 1: {laser_walk(grid, start=(0, 0), head=(0, 1))}")
    configs = []
    for start, head in generate_starts(grid):
        configs.append(laser_walk(grid, start, head))
    print(f"Result of part2: {max(configs)}")


if __name__ == "__main__":
    main("2023/16/input.txt")
