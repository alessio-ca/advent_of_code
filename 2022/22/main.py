import itertools
import math
import re
from collections import deque
from typing import Callable, TypeVar

from utils import read_input

import cube_funs as cb

T = TypeVar("T", bound=int)
CubeTuple = tuple[T, T, T]

DIR_MAP = {(0, 1): "right", (1, 0): "down", (0, -1): "left", (-1, 0): "up"}
FACING_MAP = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}


def find_match(c, line):
    try:
        return line.index(c)
    except ValueError:
        return math.inf


def generate_instructions(input_file: list[str]) -> list[str | int]:
    steps = list(map(int, re.findall(r"\d+", input_file[-1].strip())))
    rot = re.findall(r"[A-Z]", input_file[-1].strip())
    return [
        x for x in itertools.chain(*itertools.zip_longest(steps, rot)) if x is not None
    ]


class Node:
    def __init__(self, c, v, id=-1):
        self.x, self.y = c
        self.v = v
        self.id = id
        self.up = None
        self.down = None
        self.left = None
        self.right = None


def create_node_system(input_file: list[str]) -> dict[CubeTuple, Node]:
    # Create flat node system
    dict_nodes = {}
    for i, line in enumerate(input_file[:-2]):
        offset = min(find_match(".", line), find_match("#", line))
        line = line.strip()
        # For flat map, face_id is not important - set it to -1
        for j, v in enumerate(line):
            coords = (i, j + offset)
            dict_nodes[(i, j + offset, -1)] = Node(coords, v)
    # Populate nn for each node
    # idx corresponds to the axis:
    # 0 sweeps the y axis
    # 1 sweeps the x axis
    for idx in [0, 1]:
        gen = [coord[idx] for coord in dict_nodes.keys()]
        min_c, max_c = min(gen), max(gen)
        # Generate sweep line
        for i in range(min_c, max_c + 1):
            array = [key for key in dict_nodes.keys() if key[idx] == i]
            array.sort(key=lambda x: x[0])
            for low, high in zip(array, array[1:] + array[:1]):
                # When sweeping on the y axis, set right and left
                if idx == 0:
                    setattr(dict_nodes[low], "right", high)
                    setattr(dict_nodes[high], "left", low)
                # When sweeping on the x axis, set down and up
                else:
                    setattr(dict_nodes[low], "down", high)
                    setattr(dict_nodes[high], "up", low)

    return dict_nodes


def initialise_cube_coords(input_file: list[str], size: int) -> list[Node]:
    # For the cube case, add the face_id when parsing the input
    nodes = []
    idx = -1
    counter = 0
    for i, line in enumerate(input_file[:-2]):
        offset = min(find_match(".", line), find_match("#", line))
        line = line.strip()

        chunks = [line[x : x + size] for x in range(0, len(line), size)]
        for block, chunk in enumerate(chunks):
            for j, v in enumerate(chunk):
                coords = (i, block * size + j + offset)
                nodes.append(Node(coords, v, idx + 1 + block))

        counter += 1
        if (counter % size) == 0:
            counter = 0
            idx += 1 * (len(line) // size)

    return nodes


def create_cube_system(
    nodes: list[Node],
    size: int,
    remap_edges_fun: Callable,
) -> tuple[dict[CubeTuple, Node], dict[CubeTuple, CubeTuple]]:
    dict_nodes = {}
    remap_nodes = {}

    max_id = max(node.id for node in nodes) + 1
    # Normalise coords to the (0, size) range for each face
    for face_id in range(max_id):
        face_nodes = [node for node in nodes if node.id == face_id]
        min_x, min_y = (
            min(node.x for node in face_nodes),
            min(node.y for node in face_nodes),
        )
        # Before normalising, store the original position
        # (we need it for the final result)
        for node in face_nodes:
            remap_nodes[(node.x - min_x, node.y - min_y, face_id)] = (
                node.x,
                node.y,
                face_id,
            )
            node.x -= min_x
            node.y -= min_y
    # Initialise nodes, ignore edges for now
    for node in nodes:
        key = (node.x, node.y, node.id)
        dict_nodes[key] = node
        setattr(dict_nodes[key], "down", (node.x + 1, node.y, node.id))
        setattr(dict_nodes[key], "up", (node.x - 1, node.y, node.id))
        setattr(dict_nodes[key], "right", (node.x, node.y + 1, node.id))
        setattr(dict_nodes[key], "left", (node.x, node.y - 1, node.id))

    # Remap edges accordingly
    remap_edges_fun(dict_nodes, size)

    return dict_nodes, remap_nodes


def walk_cube(
    start_pos: CubeTuple,
    dict_cube: dict[CubeTuple, Node],
    instructions: list[int | str],
    turn_direction_fun: Callable,
) -> tuple[CubeTuple, tuple[int, int]]:
    pos = start_pos
    # Initialise direction as a deque, which can rotate
    # to deal with direction changes
    directions = deque([(0, 1), (1, 0), (0, -1), (-1, 0)])
    for move in instructions:
        if isinstance(move, int):
            # Attempt move
            for _ in range(move):
                new_pos = getattr(dict_cube[pos], DIR_MAP[directions[0]])
                if dict_cube[new_pos].v == ".":
                    # Deal with direction changes if needed
                    turn_direction_fun(pos, new_pos, directions)
                    pos = new_pos
                else:
                    break
        else:
            # Rotate
            if move == "R":
                directions.rotate(-1)
            else:
                directions.rotate(1)
    return pos, directions[0]


def main(filename: str):
    input_file = read_input(filename, line_strip=False)
    turn_direction_fun = (
        cb.turn_direction_example if "example" in filename else cb.turn_direction_input
    )
    remap_edges_fun = (
        cb.remap_edges_example if "example" in filename else cb.remap_edges_input
    )
    size_cube = 4 if "example" in filename else 50

    dict_nodes = create_node_system(input_file)
    start_pos = (min(x for x, y, _ in dict_nodes.keys() if y == 0), 0, -1)
    pos, facing = walk_cube(
        start_pos, dict_nodes, generate_instructions(input_file), turn_direction_fun
    )
    res = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + FACING_MAP[facing]
    print(f"Result of part 1: {res}")

    dict_cube, remap_cube = create_cube_system(
        initialise_cube_coords(input_file, size_cube), size_cube, remap_edges_fun
    )
    start_pos = (0, 0, 0)
    pos, facing = walk_cube(
        start_pos, dict_cube, generate_instructions(input_file), turn_direction_fun
    )
    pos = remap_cube[pos]
    res = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + FACING_MAP[facing]
    print(f"Result of part 2: {res}")


if __name__ == "__main__":
    main("2022/22/input.txt")
