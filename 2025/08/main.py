from utils import read_input
import numpy as np
from scipy.spatial.distance import pdist

def create_circuits(connections: np.ndarray, n_junctions: int, n_shortest: int | None) -> tuple[set[frozenset[int]], tuple[int, int]]:
    if n_shortest is None:
        n_shortest = len(connections)

    last_junctions = (-1, -1)
    # Initialise circuits
    circuits: dict[int, set] = dict()
    for i in range(n_junctions):
        circuits[i] = set([i])
    
    for conn in connections[:n_shortest]:
        c1, c2 = conn
        # If they are already in the same circuit, skip
        if circuits[c1] is circuits[c2]:
            continue
        # Merge circuits
        new_circuit = circuits[c1].union(circuits[c2])

        for node in new_circuit:
            circuits[node] = new_circuit
        
        if len(new_circuit) == n_junctions:
            last_junctions = c1, c2
            break

    return set(map(frozenset, circuits.values())), last_junctions


def main(filename: str):
    data = np.array([list(map(int, line.split(','))) for line in read_input(filename)], dtype=np.int64)
    distances = pdist(data, metric='euclidean')
    c_idx_x, c_idx_y = np.triu_indices(len(data), k=1)
    c_idx = np.array(list(zip(c_idx_x, c_idx_y)), dtype=int)
    assert len(distances) == len(c_idx)
    if 'example' in filename:
        n = 10
    else:
        n = 1000
    sorted_connections = c_idx[np.argsort(distances)]
    
    circuits, _ = create_circuits(sorted_connections, len(data), n)
    circuit_sizes = [len(circuit) for circuit in circuits]
    print(f"Result of part 1: {np.prod(sorted(circuit_sizes)[-3:])}")

    _, last_junctions = create_circuits(sorted_connections, len(data), None)
    print(f"Result of part 2: {np.prod(data[last_junctions, 0])}")

if __name__ == "__main__":
    main("2025/08/input.txt")
