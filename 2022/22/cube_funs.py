from .main import CubeTuple, Node
from typing import Dict, Deque
from utils import CoordTuple


def remap_edges_example(dict_nodes: Dict[CubeTuple, Node], size: int):
    max_idx = size - 1
    for i in range(size):
        # 0 --> 1
        setattr(dict_nodes[(0, i, 0)], "up", (0, max_idx - i, 1))
        setattr(dict_nodes[(0, max_idx - i, 1)], "up", (0, i, 0))
        # 0 --> 2
        setattr(dict_nodes[(i, 0, 0)], "left", (0, i, 2))
        setattr(dict_nodes[(0, i, 2)], "up", (i, 0, 0))
        # 0 --> 3
        setattr(dict_nodes[(max_idx, i, 0)], "down", (0, i, 3))
        setattr(dict_nodes[(0, i, 3)], "up", (max_idx, i, 0))
        # 0 --> 5
        setattr(dict_nodes[(i, max_idx, 0)], "right", (max_idx - i, 0, 5))
        setattr(dict_nodes[(max_idx - i, 0, 5)], "right", (i, max_idx, 0))
        # 1 --> 2
        setattr(dict_nodes[(i, max_idx, 1)], "right", (i, 0, 2))
        setattr(dict_nodes[(i, 0, 2)], "left", (i, max_idx, 1))
        # 1 --> 4
        setattr(dict_nodes[(max_idx, i, 1)], "down", (max_idx, max_idx - i, 4))
        setattr(dict_nodes[(max_idx, max_idx - i, 4)], "down", (max_idx, i, 1))
        # 1 --> 5
        setattr(dict_nodes[(i, 0, 1)], "left", (max_idx, max_idx - i, 5))
        setattr(dict_nodes[(max_idx, max_idx - i, 5)], "down", (i, 0, 1))
        # 2 --> 3
        setattr(dict_nodes[(i, max_idx, 2)], "right", (i, 0, 3))
        setattr(dict_nodes[(i, 0, 3)], "left", (i, max_idx, 2))
        # 2 --> 4
        setattr(dict_nodes[(max_idx, i, 2)], "down", (max_idx - i, 0, 4))
        setattr(dict_nodes[(max_idx - i, 0, 4)], "left", (max_idx, i, 2))
        # 3 --> 4
        setattr(dict_nodes[(max_idx, i, 3)], "down", (0, i, 4))
        setattr(dict_nodes[(0, i, 4)], "up", (max_idx, i, 3))
        # 3 --> 5
        setattr(dict_nodes[(i, max_idx, 3)], "right", (0, max_idx - i, 5))
        setattr(dict_nodes[(0, max_idx - i, 5)], "top", (i, max_idx, 3))
        # 4 --> 5
        setattr(dict_nodes[(i, max_idx, 4)], "right", (i, 0, 5))
        setattr(dict_nodes[(i, 0, 5)], "left", (i, max_idx, 4))


def turn_direction_example(
    pos: CubeTuple,
    new_pos: CubeTuple,
    directions: Deque[CoordTuple],
):
    # Change direction if moving to another face of the cube
    id_1, id_2 = pos[2], new_pos[2]
    if id_1 != id_2:
        if (
            (id_1, id_2) == (0, 1)
            or (id_1, id_2) == (1, 0)
            or (id_1, id_2) == (0, 5)
            or (id_1, id_2) == (5, 0)
            or (id_1, id_2) == (1, 4)
            or (id_1, id_2) == (4, 1)
        ):
            directions.rotate(2)
        elif (
            (id_1, id_2) == (0, 2)
            or (id_1, id_2) == (2, 4)
            or (id_1, id_2) == (5, 1)
            or (id_1, id_2) == (5, 3)
        ):
            directions.rotate(1)
        elif (
            (id_1, id_2) == (2, 0)
            or (id_1, id_2) == (4, 2)
            or (id_1, id_2) == (1, 5)
            or (id_1, id_2) == (3, 5)
        ):
            directions.rotate(-1)


def remap_edges_input(dict_nodes: Dict[CubeTuple, Node], size: int):
    max_idx = size - 1
    for i in range(size):
        # 0 --> 1
        setattr(dict_nodes[(i, max_idx, 0)], "right", (i, 0, 1))
        setattr(dict_nodes[(i, 0, 1)], "left", (i, max_idx, 0))
        # 0 --> 2
        setattr(dict_nodes[(max_idx, i, 0)], "down", (0, i, 2))
        setattr(dict_nodes[(0, i, 2)], "up", (max_idx, i, 0))
        # 0 --> 3
        setattr(dict_nodes[(i, 0, 0)], "left", (max_idx - i, 0, 3))
        setattr(dict_nodes[(max_idx - i, 0, 3)], "left", (i, 0, 0))
        # 0 --> 5
        setattr(dict_nodes[(0, i, 0)], "up", (i, 0, 5))
        setattr(dict_nodes[(i, 0, 5)], "left", (0, i, 0))
        # 1 --> 2
        setattr(dict_nodes[(max_idx, i, 1)], "down", (i, max_idx, 2))
        setattr(dict_nodes[(i, max_idx, 2)], "right", (max_idx, i, 1))
        # 1 --> 4
        setattr(dict_nodes[(i, max_idx, 1)], "right", (max_idx - i, max_idx, 4))
        setattr(dict_nodes[(max_idx - i, max_idx, 4)], "right", (i, max_idx, 1))
        # 1 --> 5
        setattr(dict_nodes[(0, i, 1)], "up", (max_idx, i, 5))
        setattr(dict_nodes[(max_idx, i, 5)], "down", (0, i, 1))
        # 2 --> 3
        setattr(dict_nodes[(i, 0, 2)], "left", (0, i, 3))
        setattr(dict_nodes[(0, i, 3)], "up", (i, 0, 2))
        # 2 --> 4
        setattr(dict_nodes[(max_idx, i, 2)], "down", (0, i, 4))
        setattr(dict_nodes[(0, i, 4)], "up", (max_idx, i, 2))
        # 3 --> 4
        setattr(dict_nodes[(i, max_idx, 3)], "right", (i, 0, 4))
        setattr(dict_nodes[(i, 0, 4)], "left", (i, max_idx, 3))
        # 3 --> 5
        setattr(dict_nodes[(max_idx, i, 3)], "down", (0, i, 5))
        setattr(dict_nodes[(0, i, 5)], "up", (max_idx, i, 3))
        # 4 --> 5
        setattr(dict_nodes[(max_idx, i, 4)], "down", (i, max_idx, 5))
        setattr(dict_nodes[(i, max_idx, 5)], "right", (max_idx, i, 4))


def turn_direction_input(
    pos: CubeTuple,
    new_pos: CubeTuple,
    directions: Deque[CoordTuple],
):
    # Change direction if moving to another face of the cube
    id_1, id_2 = pos[2], new_pos[2]
    if id_1 != id_2:
        if (
            (id_1, id_2) == (0, 3)
            or (id_1, id_2) == (3, 0)
            or (id_1, id_2) == (1, 4)
            or (id_1, id_2) == (4, 1)
        ):
            directions.rotate(2)
        elif (
            (id_1, id_2) == (2, 3)
            or (id_1, id_2) == (5, 0)
            or (id_1, id_2) == (2, 1)
            or (id_1, id_2) == (5, 4)
        ):
            directions.rotate(1)
        elif (
            (id_1, id_2) == (3, 2)
            or (id_1, id_2) == (0, 5)
            or (id_1, id_2) == (1, 2)
            or (id_1, id_2) == (4, 5)
        ):
            directions.rotate(-1)
