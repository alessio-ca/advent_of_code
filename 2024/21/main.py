from utils import read_input
from collections import defaultdict
import re
import math
import heapq
from functools import cache

Pad = dict[str, dict[str, str]]
Dist = int | float
ShortestPrevs = dict[str, set[tuple[str, str]]]
ShortestPaths = dict[str, dict[str, list[str]]]

NUMERIC_PAD: Pad = {
    "A": {"^": "3", "<": "0"},
    "0": {"^": "2", ">": "A"},
    "1": {"^": "4", ">": "2"},
    "2": {"^": "5", ">": "3", "v": "0", "<": "1"},
    "3": {"^": "6", "v": "A", "<": "2"},
    "4": {"^": "7", ">": "5", "v": "1"},
    "5": {"^": "8", ">": "6", "v": "2", "<": "4"},
    "6": {"^": "9", "v": "3", "<": "5"},
    "7": {">": "8", "v": "4"},
    "8": {">": "9", "v": "5", "<": "7"},
    "9": {"v": "6", "<": "8"},
}

DIRECTIONAL_PAD: Pad = {
    "A": {"v": ">", "<": "^"},
    "^": {">": "A", "v": "v"},
    ">": {"^": "A", "<": "v"},
    "v": {"^": "^", ">": ">", "<": "<"},
    "<": {">": "v"},
}


def create_graph_subset(node: str, pad: Pad) -> ShortestPrevs:
    """Create graph subset; the subset has the property that each path from `node` to any node
    is a shortest path between `node` and the target."""
    q: list[tuple[Dist, str]] = [(0, node)]

    # Lengths is the default dist dictionary
    lengths: defaultdict[str, Dist] = defaultdict(lambda: math.inf, {node: 0})
    # Prev is a subset of Pad where each path from node to any node in Prev
    # is a shortest path
    prev: defaultdict[str, set[tuple[str, str]]] = defaultdict(lambda: set())

    # Create the Prev subset graph
    while q:
        cost, node = heapq.heappop(q)
        for edge, neigh in pad[node].items():
            candidate = cost + 1
            if candidate <= lengths[neigh]:
                # Accepts candidates with same length (multiple shortest paths)
                lengths[neigh] = candidate
                prev[neigh].add((node, edge))
                heapq.heappush(q, (candidate, neigh))

    return prev


def find_shortest_paths(pad: Pad) -> ShortestPaths:
    """Shortest paths between all pair of nodes of a Pad.
    All equal-length shortest paths are returned."""
    all_paths: dict[str, dict[str, list[str]]] = dict()

    for source in pad:
        prev = create_graph_subset(source, pad)
        paths: dict[str, list[str]] = defaultdict(list)
        for target in prev:
            # Walk path from target to source
            q = [(0, target, "")]
            lengths: defaultdict[str, Dist] = defaultdict(lambda: math.inf, {target: 0})
            while q:
                # Pop item from stack
                cost, node, path = heapq.heappop(q)
                if node == source:
                    # Add path to target
                    if cost <= lengths[source]:
                        paths[target].append(path)
                    continue

                # Explore neighbors of node in Prev
                for neigh, edge in prev[node]:
                    # Favour moves where the edge is unchanged (i.e. we move in the same direction)
                    if (not path) or (edge != path[0]):
                        candidate = cost + 1
                    else:
                        candidate = cost
                    if candidate <= lengths[neigh]:
                        # Accepts candidates with same length (multiple shortest paths)
                        lengths[neigh] = candidate
                        heapq.heappush(q, (candidate, neigh, edge + path))

        all_paths[source] = paths

    return all_paths


# Create overall Paths for both Pads
NUMERIC_PATHS = find_shortest_paths(NUMERIC_PAD)
PATHS = NUMERIC_PATHS | find_shortest_paths(DIRECTIONAL_PAD)
PATHS["A"] |= NUMERIC_PATHS["A"]  # The A key appears in both numeric and directional


@cache
def obtain_shortest_sequence(moves: str, level: int, max_level: int) -> int:
    """Recursive function to obtain the shortest sequence"""
    head = "A"
    total = 0
    for target in moves:
        # Obtain sequence of moves to go from `head` to `target`
        if PATHS[head][target]:
            new_moves = [move + "A" for move in PATHS[head][target]]
        else:
            new_moves = ["A"]

        # If max recursion is reached, augment total
        #  using an arbitrary move in `new_moves` (they're all the same length)
        if level == max_level:
            total += len(new_moves[0])
        # Otherwise, augment total with the recursive call (taking the minimum
        #   across all new_moves)
        else:
            total += min(
                obtain_shortest_sequence(new_move, level + 1, max_level)
                for new_move in new_moves
            )
        head = target
    return total


def calculate_complexity(code: str, n: int) -> int:
    total = obtain_shortest_sequence(code, 0, n)
    digits = re.findall(r"\d+", code)[0]
    return total * int(digits)


def main(filename: str):
    codes = read_input(filename)
    print(f"Result of part 1: {sum(calculate_complexity(code, 2) for code in codes)}")
    print(f"Result of part 2: {sum(calculate_complexity(code, 25) for code in codes)}")


if __name__ == "__main__":
    main("2024/21/input.txt")
