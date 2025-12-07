from itertools import chain, combinations

import numpy as np

from utils import read_input


def create_adjacency_matrix(
    computers_dict: dict[str, int], connections: list[tuple[str, str]]
) -> np.ndarray:
    # Create adjacency matrix
    adj_matrix = np.zeros(shape=(len(computers_dict), len(computers_dict)), dtype=bool)
    for i, j in connections:
        ic = computers_dict[i]
        jc = computers_dict[j]
        adj_matrix[ic][jc] = True
        adj_matrix[jc][ic] = True
    return adj_matrix


def part_1(adj_matrix: np.ndarray, set_ts: set[int]) -> int:
    # Obtain the non-null graph edges
    # Use upper triangular since the matrix is symmetric
    links = np.argwhere(np.triu(adj_matrix))
    connected = set()
    # Iterate over all vertexes with at least one edge
    for i in np.unique(links[:, 0]):
        # Iterate over the combinations of the other adjacent vertexes
        # in pairs
        for combo in combinations(links[links[:, 0] == i][:, 1], 2):
            # if the pair is connected, the vertex + pair form a clique of size 3
            if adj_matrix[combo]:
                connected.add(frozenset((i,) + combo))

    return sum(1 for party in connected if party.intersection(set_ts))


def find_maximal_clique(adj_matrix: np.ndarray) -> tuple[int]:
    # Obtain the non-null graph edges
    # Use upper triangular since the matrix is symmetric
    links = np.argwhere(np.triu(adj_matrix))
    # Obtain max possible size of a clique
    size = max(links[links[:, 0] == i][:, 1].size for i in np.unique(links[:, 0]))
    # Iterate from max_size until a match is found
    while size > 0:
        # Iterate over all combinations of size 'size' for each vertex
        for i, combos in enumerate(
            combinations(links[links[:, 0] == i][:, 1], size)
            for i in range(len(adj_matrix))
        ):
            for combo in combos:
                # If the combo leads to a full matrix (minus the diagonal), it's a
                # valid clique
                if adj_matrix[list(combo)][:, list(combo)].sum() == size * (size - 1):
                    return (i,) + combo
        size -= 1
    return (0,)


def part_2(adj_matrix: np.ndarray, computers_dict: dict[str, int]) -> str:
    max_clique = find_maximal_clique(adj_matrix)
    computers = [key for key, value in computers_dict.items() if value in max_clique]
    computers.sort()
    return ",".join(computers)


def main(filename: str):
    connections: list[tuple[str, str]] = list(
        map(lambda x: tuple(x.split("-")), read_input(filename))  # type: ignore
    )
    computers_dict = {
        computer: i for i, computer in enumerate(set(chain.from_iterable(connections)))
    }
    adj_matrix = create_adjacency_matrix(computers_dict, connections)

    set_ts = set(value for key, value in computers_dict.items() if key[0] == "t")

    print(f"Result of part 1: {part_1(adj_matrix, set_ts)}")
    print(f"Result of part 2: {part_2(adj_matrix, computers_dict)}")


if __name__ == "__main__":
    main("2024/23/input.txt")
