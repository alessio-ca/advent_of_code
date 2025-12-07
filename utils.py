import cProfile
import functools
import io
import pstats
import time
from functools import cache
from collections import defaultdict
from typing import Callable, Generator

import numpy as np

CoordTuple = tuple[int, int]
CoordGenerator = Generator[CoordTuple, None, None]
ConstraintFunArgs = tuple[int, int, int, int, np.ndarray]
ConstraintFun = Callable[[ConstraintFunArgs], bool]
DijkstraDistances = defaultdict[CoordTuple, float]


def add_tuples(p1: CoordTuple, p2: CoordTuple) -> CoordTuple:
    return p1[0] + p2[0], p1[1] + p2[1]


@cache
def cached_add_tuples(p1: CoordTuple, p2: CoordTuple) -> CoordTuple:
    return add_tuples(p1, p2)


def diff_tuple(p1: CoordTuple, p2: CoordTuple) -> CoordTuple:
    return p1[0] - p2[0], p1[1] - p2[1]


def no_constraints(_: ConstraintFunArgs) -> bool:
    return True


def get_neighbors(
    node: CoordTuple,
    grid: np.ndarray,
    constraint: ConstraintFun = no_constraints,
) -> Generator[CoordTuple, None, None]:
    """Simple function to obtain the neighbors coordinates of a point on a grid.
    The grid bounds are considered. Obstacles/constraints are considered"""
    x, y = node
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        xx, yy = (x + dx, y + dy)
        # Check if out of bounds
        if 0 <= xx < grid.shape[0] and 0 <= yy < grid.shape[1]:
            # Check constraint
            if constraint((xx, yy, x, y, grid)):
                yield xx, yy


def read_input(input_file: str, line_strip: bool = True) -> list[str]:
    with open(input_file, "r") as file:
        input_list = []
        for line in file:
            if line_strip:
                input_list.append(line.strip())
            else:
                input_list.append(line.rstrip("\n"))

    return input_list


def read_integer_lists(input_file: str) -> list[list[int]]:
    return list(map(lambda x: list(map(int, x.split(" "))), read_input(input_file)))


def read_single_line(input_file: str) -> str:
    return read_input(input_file)[0]


def read_input_batch(input_file: str, line_split: bool = True) -> list[list[str]]:
    with open(input_file, "r") as file:
        input_list = []
        batch: list[str] = []
        for line in file:
            if line == "\n":
                input_list.append(batch)
                batch = []
            else:
                if line_split:
                    for element in line.strip().split(" "):
                        batch.append(element)
                else:
                    batch.append(line.strip())

        # Append last batch
        if batch:
            input_list.append(batch)

    return input_list


def timefunc(func):
    """timefunc's doc"""

    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        """time_wrapper's doc string"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure


def profilefunc(func):
    """profilefunc's doc"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE  # 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return wrapper
