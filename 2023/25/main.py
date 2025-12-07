from collections import defaultdict
from typing import List, Tuple

import numpy as np
import regex as re

from utils import read_input


def build_graph_matrices(connections: List[List[str]]) -> Tuple[np.ndarray, np.ndarray]:
    # Create graph dict tree (node -> edges)
    adj_dict: defaultdict[str, set[str]] = defaultdict(set)
    for line in connections:
        adj_dict[line[0]] |= set(line[1:])
        for comp in line[1:]:
            adj_dict[comp].add(line[0])
    # Build adjacency matrix
    adj_map = {key: i for i, key in enumerate(adj_dict.keys())}
    adj_matrix = np.zeros(shape=(len(adj_dict), len(adj_dict)), dtype=int)
    for key, value in adj_dict.items():
        row_index = adj_map[key]
        column_indexes = [adj_map[node] for node in value]
        adj_matrix[row_index, column_indexes] = 1
    # Build degree matrix
    deg_matrix = np.diag(adj_matrix.sum(axis=0))
    return adj_matrix, deg_matrix


def spectral_min_cut(adj: np.ndarray, deg: np.ndarray) -> int:
    # Find eigenvectors of the Laplacian matrix of the graph
    # Since the Laplacian is symmetric, SVD can be used
    # for eigen decomposition - V's rows are the eigenvectors
    _, _, V = np.linalg.svd(deg - adj)
    # The Fielder vector is the eigenvector of the smallest non-trivial eigenvalue
    fielder_v = V[-2]
    # Negative and positive components of the Fielder vector are the nodes in the
    #  two different partitions. We only need to count one of the 2.
    return (fielder_v > 0).sum()


def main(filename):
    connections = [re.findall(r"[a-z]{3}", line) for line in read_input(filename)]
    adj_matrix, deg_matrix = build_graph_matrices(connections)
    min_cut_size = spectral_min_cut(adj_matrix, deg_matrix)
    print(f"Result of part 1: {min_cut_size * (adj_matrix.shape[0] - min_cut_size)}")


if __name__ == "__main__":
    main("2023/25/input.txt")
