import math
from typing import Dict

from utils import read_input


def calculate_orbits(planet: str, dict_orbits: Dict[str, str]):
    """Convenience function to calculate the number of orbits for a planet"""
    if planet not in dict_orbits.keys():
        # Planet is not orbiting anything, so 0
        return 0
    else:
        # Planet has 1 direct orbit + recursive indirect orbits
        return 1 + calculate_orbits(dict_orbits[planet], dict_orbits)


class Path:
    def __init__(self):
        self.dist = {}
        self.path = {}


def shortest_path(dict_nn, source):
    """Implementation of Dijkstra algorithm for shortest path"""
    # Create double dictionary keeping track of distances between nodes
    result = Path()
    for key in dict_nn.keys():
        result.dist[key] = math.inf
        result.path[key] = None

    # Initialize result for source
    result.dist[source] = 0
    result.path[source] = [source]

    # Initialize queue of nodes and empty visited set
    queue = set(dict_nn.keys())
    visited = set()

    while len(queue) > 0:
        # Get non-visited node with the smallest distance from source
        min_dist = math.inf
        min_node = None
        for node in queue:
            if (result.dist[node] < min_dist) and (node not in visited):
                min_dist = result.dist[node]
                min_node = node
        # Add node to seen, remove from queue
        queue.remove(min_node)
        visited.add(min_node)

        # For each destination, update path and distance from source
        for node in dict_nn[min_node]:
            tot_dist = 1 + min_dist
            if tot_dist < result.dist[node]:
                result.dist[node] = tot_dist
                result.path[node] = result.path[min_node] + [node]
    return result


def main():
    input_file = read_input("2019/06/input.txt")
    input_list = [line.split(")") for line in input_file]
    # Create unique set of planets
    set_planets = set(item for sublist in input_list for item in sublist)

    # Create orbiting dictionary
    dict_orbits = {orbiter: center for center, orbiter in input_list}

    # Obtain count orbits
    dict_count = {
        planet: calculate_orbits(planet, dict_orbits) for planet in set_planets
    }
    print(f"Result of part 1: {sum(dict_count.values())}")

    # Create neighbour dictionary
    dict_nn = {planet: set() for planet in set_planets}
    for center, orbiter in input_list:
        dict_nn[center].add(orbiter)
        dict_nn[orbiter].add(center)

    result = shortest_path(dict_nn, "YOU")
    print(f"Result of part 2: {result.dist['SAN'] - 2}")


if __name__ == "__main__":
    main()
