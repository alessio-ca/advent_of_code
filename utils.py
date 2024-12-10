import time
import functools
import cProfile
import io
import pstats
from typing import TypeVar

T = TypeVar("T", bound=int)
CoordTuple = tuple[T, T]


def add_tuples(p1: CoordTuple, p2: CoordTuple) -> CoordTuple:
    return p1[0] + p2[0], p1[1] + p2[1]


def diff_tuple(p1: CoordTuple, p2: CoordTuple) -> CoordTuple:
    return p1[0] - p2[0], p1[1] - p2[1]


def read_input(input_file: str, line_strip: bool = True) -> list[str]:
    with open(input_file, "r") as file:
        input_list = []
        for line in file:
            if line_strip:
                input_list.append(line.strip())
            else:
                input_list.append(line.rstrip("\n"))

    return input_list


def read_integer_lists(input_file: str) -> list[int]:
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
