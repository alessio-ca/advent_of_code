from collections import defaultdict, deque
from itertools import product

import numpy as np
from scipy.signal import convolve2d

from utils import ConstraintFunArgs, CoordTuple, get_neighbors, read_input


def equal_constraint(fun_args: ConstraintFunArgs) -> bool:
    xx, yy, x, y, grid = fun_args
    return grid[xx, yy] == grid[x, y]


def create_neighbors_dict(
    grid: np.ndarray,
) -> dict[CoordTuple, list[CoordTuple]]:
    """Create dictionary of neighbors for a grid"""
    dict_nn = dict()
    for node in product(range(grid.shape[0]), range(grid.shape[1])):
        dict_nn[node] = list(get_neighbors(node, grid, equal_constraint))

    return dict_nn


def extract_connected_components(adj_list: dict[CoordTuple, list[CoordTuple]]):
    # Store components as a dict:
    # d[node] = component
    components: dict[CoordTuple, int] = dict()

    visited = set()
    id_component = 0
    for start in adj_list:
        # Only process fresh starts if not already visited
        if start not in visited:
            # For new starts, span a DFS
            stack = deque([start])
            while stack:
                head = stack.pop()
                if head not in visited:
                    visited.add(head)
                    for nn in adj_list[head]:
                        stack.append(nn)
                    # Assign new component
                    components[head] = id_component

            # After exahusting the walk for a new start, augment
            # component_id
            id_component += 1

    # Invert the component dictionary: give a set of nodes per component
    comp_set: defaultdict[int, set[CoordTuple]] = defaultdict(set)
    for node, id in components.items():
        comp_set[id].add(node)
    return comp_set


def main(filename: str):
    garden = np.array(list(map(list, read_input(filename))), dtype="str")
    # Create adjaceny list
    adj_list = create_neighbors_dict(garden)
    components = extract_connected_components(adj_list)
    res_1 = sum(
        sum(4 - len(adj_list[node]) for node in nodes) * (len(nodes))
        for nodes in components.values()
    )
    print(f"Result of part 1: {res_1}")

    garden_int = np.zeros(shape=garden.shape, dtype=int)
    for id, nodes in components.items():
        for node in nodes:
            garden_int[node] = id + 1

    res_2 = sum(
        abs(
            convolve2d(
                garden_int == id + 1,
                np.array([[-1, 1], [1, -1]], dtype=int),
                boundary="fill",
                fillvalue=0,
            )
        ).sum()
        * (garden_int == id + 1).sum()
        for id in components.keys()
    )
    print(f"Result of part 2: {res_2}")


if __name__ == "__main__":
    main("2024/12/input.txt")
