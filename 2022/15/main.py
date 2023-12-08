from utils import read_input
import re
import numpy as np
import itertools
from collections import deque


def manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


def create_vertex_array(c, d):
    xc, yc = c
    # Create vertex array
    offset = d + 0j
    v = []
    for _ in range(4):
        dx = int(offset.real)
        dy = int(offset.imag)
        v.append((xc + dx, yc + dy))
        offset *= 1j
    return v


def create_edges(v):
    edges = []
    it = deque(v)
    for _ in range(len(v)):
        edges.append((it[0], it[1]))
        it.rotate(-1)

    return edges


def create_intersections(e1, e2):
    segm = []
    it1 = deque(e1)
    it2 = deque(e2)

    it2.rotate(-1)
    for pair in zip(it1, it2):
        segm.append(pair)

    it2.rotate(1)
    it1.rotate(-1)
    for pair in zip(it1, it2):
        segm.append(pair)

    return segm


def get_intersect(e1, e2):
    a1, a2 = e1
    b1, b2 = e2
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return (float("inf"), float("inf"))
    return (x / z, y / z)


def is_in_sensor(pt, sensors, distances):
    return any([manhattan(pt, sensor) <= d for (sensor, d) in zip(sensors, distances)])


def check_bounds(pt, bounds):
    for i in pt:
        if (i < bounds[0]) | (i > bounds[1]):
            return False

    return True


def find_distress_beacon(sensors, distances, bounds):
    sensors_pairs = itertools.combinations(sensors, 2)
    distance_pairs = itertools.combinations(distances, 2)
    for (c1, c2), (d1, d2) in zip(sensors_pairs, distance_pairs):
        # Check if they overlap
        if manhattan(c1, c2) < sum((d1, d2)):
            # Create vertex array
            v1 = create_vertex_array(c1, d1)
            v2 = create_vertex_array(c2, d2)
            # Generate edge pairs
            e1 = create_edges(v1)
            e2 = create_edges(v2)
            # Generate intersection pairs
            ss = create_intersections(e1, e2)
            # Test intersections
            for s in ss:
                # Intersect
                ix = tuple(get_intersect(*s))
                # Test that intersection pt is integer
                #  (otherwise, there are no valid neighbors)
                if ix[0].is_integer():
                    # Iterate over 4 close neighbors of intersection pt
                    for pt in create_vertex_array(ix, 1):
                        if (not is_in_sensor(pt, sensors, distances)) & check_bounds(
                            pt, bounds
                        ):
                            return pt


def main():
    raw_input = [
        list(map(int, re.findall(r"-?\d+", line)))
        for line in read_input("2022/15/input.txt", line_strip=True)
    ]

    # Mark sensor and Manhattan distance
    sensors = []
    beacons = []
    distances = []
    for input_line in raw_input:
        x_s, y_s, x_b, y_b = input_line
        coord_s = (x_s, y_s)
        coord_b = (x_b, y_b)
        sensors.append(coord_s)
        beacons.append(coord_b)
        distances.append(manhattan(coord_s, coord_b))

    # Calculate sensor overlaps with row of interest
    overlaps = set()
    y_line = 2000000
    for ((x_s, y_s), dist_s) in zip(sensors, distances):
        dist_x = dist_s - abs(y_line - y_s)
        if dist_x >= 0:
            overlaps.update(range(x_s - dist_x, x_s + dist_x + 1))
    # Remove already existing beacons
    overlaps = overlaps.difference([x_b for (x_b, y_b) in beacons if y_b == y_line])

    print(f"Result of part 1: {len(overlaps)}")

    # Calculate overlapping pairs
    bounds = [0, 4000000]
    pt = find_distress_beacon(sensors, distances, bounds)
    print(f"Result of part 2: {int(pt[0] * 4000000 + pt[1])}")


if __name__ == "__main__":
    main()
