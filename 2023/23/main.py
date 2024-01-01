from utils import read_input, timefunc
import numpy as np
from typing import Tuple, Dict, List, Iterator
import math
import itertools
from typing import TypeVar
from collections import defaultdict

T = TypeVar("T", bound=int)
Coord = Tuple[T, T]

DICT_DIRECTIONS = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def longest_path_dfs(
    start: int,
    end: int,
    dict_nn: Dict[int, List[int]],
) -> int:
    """DFS algo for longest path calculation between a start node and
        and end node
    Returns the length of the longest path

    `dict_node` contains the list of neighbors for each node
    """
    # Initialise queue & max length
    stack = [(0, {start}, start)]
    max_length = -math.inf
    while stack:
        # Pop from the stack
        dist, current_path, head = stack.pop()
        # Check if end node
        if head == end:
            max_length = max(max_length, dist)
            continue
        # One step more
        dist += 1
        for neighbor in dict_nn[head]:
            # If neighbor is not already in path, add to the stack
            if neighbor not in current_path:
                stack.append((dist, current_path | {neighbor}, neighbor))

    return max_length


def longest_path_dfs_compressed(
    start: int,
    end: int,
    graph_edges: Dict[int, List[Tuple[int, int]]],
) -> int:
    """DFS algo for longest path calculation between a start node and
        and end node, on a compressed graph
    Returns the length of the longest path

    `graph_edges` contains the list of neighbors for each node
    """
    # Initialise queue & max length
    stack = [(0, {start}, start)]
    max_length = -math.inf

    while stack:
        dist, path, node = stack.pop()
        # Add current path to visited
        # Find neighbors
        for dest, new_dist in graph_edges[node]:
            # If we reached the end, update dist
            if dest == end:
                max_length = max(max_length, dist + new_dist)
                continue
            # Push adjacents to stack if they don't intersect
            if dest not in path:
                stack.append((dist + new_dist, path | {dest}, dest))

    return max_length


def compress_graph(
    start: int,
    end: int,
    dict_nn: Dict[int, List[int]],
) -> Dict[Tuple[int, int], int]:
    """Compress a graph between start and end node.
    Calculate edges between grid junctions and transform grid
    into a graph of junctions.
    """
    # Consider a grah made of junction nodes.
    # Each path from a junction to another is an edge

    # Initialise queue and visited set
    graph = defaultdict(list)
    stack = [(0, [start], start)]
    visited = set()

    while stack:
        # Pop the last junction
        dist, junction_path, junction = stack.pop()
        # Process junction if not visited
        if junction not in visited:
            visited.add(junction)
            for branch in dict_nn[junction]:
                # Examine each branch if not visited before
                if branch not in junction_path:
                    path = junction_path + [branch]
                    dist = 1
                    adj = [
                        neighbor for neighbor in dict_nn[branch] if neighbor not in path
                    ]
                    # Keep going until next junction
                    while len(adj) == 1:
                        dist += 1
                        path.append(adj[0])
                        adj = [
                            neighbor
                            for neighbor in dict_nn[path[-1]]
                            if neighbor not in path
                        ]

                    # If we reached a dead end and it's not the end, prune
                    if len(adj) == 0 and path[-1] != end:
                        continue
                    else:
                        # Add node to junction stack
                        stack.append((dist, path, path[-1]))
                        # Update graph dictionary
                        graph[junction].append((path[-1], dist))
                        graph[path[-1]].append((junction, dist))

    return graph


def conv_func(coord: Coord, grid: np.ndarray) -> int:
    """Convert a coord tuple into a single int"""
    return grid.shape[1] * coord[0] + coord[1]


def convert_coords_to_int(
    dict_nn: Dict[Coord, List[Coord]], grid: np.ndarray
) -> Dict[int, List[int]]:
    """Convert a dictionary of nn as Coord into single int"""
    return {
        conv_func(key, grid): [conv_func(el, grid) for el in value]
        for key, value in dict_nn.items()
    }


def _get_neighbors(node: Coord, grid: np.ndarray) -> Iterator:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered. Obstacles/constraints are considered"""
    x, y = node
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = (x + dx, y + dy)
        # Check if out of bounds
        if 0 <= xx < grid.shape[0] and 0 <= yy < grid.shape[1]:
            # Check if not a a wall or direction if compatible with slope
            if not (
                grid[xx, yy] == "#"
                or (
                    grid[xx, yy] in DICT_DIRECTIONS
                    and DICT_DIRECTIONS[grid[xx, yy]] != (dx, dy)
                )
            ):
                yield (xx, yy)


def create_neighbors_dict(
    grid: np.ndarray,
) -> Dict[Coord, List[Coord]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn = {
        node: []
        for node in list(itertools.product(range(grid.shape[0]), range(grid.shape[1])))
    }
    for node in dict_nn.keys():
        dict_nn[node] = _get_neighbors(node, grid)

    return dict_nn


@timefunc
def main(filename: str):
    grid = np.array([[c for c in row] for row in read_input(filename)])
    # Create neighbour dictionary
    dict_nn = convert_coords_to_int(create_neighbors_dict(grid), grid)

    # Perform shortest path search
    start = conv_func((0, 1), grid)
    end = conv_func((grid.shape[0] - 1, grid.shape[1] - 2), grid)
    print(f"Result of part 1: {longest_path_dfs(start, end, dict_nn)}")
    for slope in DICT_DIRECTIONS.keys():
        grid[grid == slope] = "."
    dict_nn = convert_coords_to_int(create_neighbors_dict(grid), grid)
    graph = compress_graph(start, end, dict_nn)
    # We can further limit the search to the last junction before end
    new_end, dist_end = graph[end][0]
    max_dist = longest_path_dfs_compressed(start, new_end, graph)
    print(f"Result of part 2: {dist_end + max_dist}")


if __name__ == "__main__":
    main("2023/23/input.txt")
