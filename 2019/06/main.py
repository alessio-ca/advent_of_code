"""
--- Day 6: Universal Orbit Map ---

You've landed at the Universal Orbit Map facility on Mercury. Because navigation in
 space often involves transferring between orbits, the orbit maps here are useful for
  finding efficient routes between, for example, you and Santa. You download a map of
   the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around
 exactly one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /
In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around
 AAA (drawn with lines) is only partly shown. In the map data, this orbital
  relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't
 corrupted during the download. To verify maps, the Universal Orbit Map facility uses
  orbit count checksums - the total number of direct orbits (like the one shown above)
   and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any
 number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly
  orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
In this visual representation, when two objects are connected by a line, the one on the
 right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

--- Part Two ---

Now, you just need to figure out how many orbital transfers you (YOU) need to take to
 get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is
 orbiting. An orbital transfer lets you move from any object to an object orbiting or
  orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from
 K to I, a minimum of 4 orbital transfers are required:

K to J
J to E
E to D
D to I
Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU
What is the minimum number of orbital transfers required to move from the object YOU
 are orbiting to the object SAN is orbiting? (Between the objects they are orbiting -
  not between YOU and SAN.)
"""

from utils import read_input
from typing import Dict
import math


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
