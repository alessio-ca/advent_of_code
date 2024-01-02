from utils import read_input
import re
import heapq
import math
from collections import defaultdict


class Node:
    def __init__(self, name, rate, neighbors):
        self.name = name
        self.rate = rate
        self.neighs = neighbors


def parse_input(line):
    # Split line on colon
    parts = line.split("; ")
    # Fetch valve and flowrate
    valve, rate = re.fullmatch(
        r"^Valve ([A-Z]{2}) has flow rate=(\d*)$", parts[0]
    ).groups()
    # Fetch tunnels
    tunnels = re.search(r"(([A-Z]{2})(, [A-Z]{2})*)$", parts[1]).group()

    return Node(valve, int(rate), tunnels.split(", "))


def compute_paths(node, nodes):
    # Compute all shortest paths from a node to any node in `nodes`
    q = [(0, node.name)]
    lengths = defaultdict(lambda: math.inf, {node.name: 0})

    while q:
        cost, c_node = heapq.heappop(q)
        for neigh in nodes[c_node].neighs:
            candidate = cost + 1
            if candidate < lengths[neigh]:
                # Only consider neigh if has non-zero rate
                lengths[neigh] = candidate
                heapq.heappush(q, (candidate, neigh))

    return lengths


def compute_all_paths(start_node, nodes):
    # Compute costs (lengths) for all paths between all nodes
    # Only compute it for the start node or nodes with non-zero rate
    costs = {
        name: compute_paths(node, nodes)
        for name, node in nodes.items()
        if name == start_node or node.rate > 0
    }
    # Eliminate nodes with zero flow rate from computed costs
    for name, costs_d in costs.items():
        costs[name] = {d: l for d, l in costs_d.items() if nodes[d].rate > 0}
    return costs


def compute_all_scenarios(dists, start_node, candidate_nodes, visited_nodes, t):
    # Recursively compute all possible paths from start_node
    #  to any node with a valve to open
    for node in candidate_nodes:
        # The +1 is for opening the valve
        length = dists[start_node][node] + 1
        # If we make it in time, recurse
        if length < t:
            yield from compute_all_scenarios(
                dists,
                node,
                candidate_nodes - {node},
                visited_nodes + [node],
                t - length,
            )
    # Return the sequence of visited nodes (the path)
    yield visited_nodes


def pressure_release(lengths, nodes, start_node, trajectory, t):
    # Compute the pressure release for a certain trajectory
    current = start_node
    pressure = 0
    for node in trajectory:
        # The +1 is for opening the valve
        length = lengths[current][node] + 1
        t -= length
        pressure += t * nodes[node].rate
        current = node
    return pressure


def main(filename: str):
    raw_input = [parse_input(line) for line in read_input(filename, line_strip=True)]
    nodes = {node.name: node for node in raw_input}
    dists = compute_all_paths("AA", nodes)

    candidate_nodes = set(dists.keys()) - {"AA"}
    scenarios = compute_all_scenarios(dists, "AA", candidate_nodes, [], 30)
    optimised_release = max(
        pressure_release(dists, nodes, "AA", scenario, 30) for scenario in scenarios
    )
    print(f"Result of part 1: {optimised_release}")

    scenarios = compute_all_scenarios(dists, "AA", candidate_nodes, [], 26)
    # Calculate all possible release scenarios, sorting them (highest first)
    releases = sorted(
        [
            (pressure_release(dists, nodes, "AA", scenario, 26), set(scenario))
            for scenario in scenarios
        ]
    )[::-1]

    # Check pairs
    max_score = 0
    for i, (p1, path_1) in enumerate(releases):
        # Stopping criterion
        if p1 * 2 < max_score:
            break
        for p2, path_2 in releases[i + 1 :]:
            # Check if paths overlap
            if len(path_1 & path_2) == 0:
                pair_release = p1 + p2
                max_score = max(max_score, pair_release)
    print(f"Result of part 2: {max_score}")


if __name__ == "__main__":
    main("2022/16/input.txt")
