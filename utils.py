from typing import List
import time
import functools


def read_input(input_file: str, line_strip: bool = True) -> List[str]:
    with open(input_file, "r") as input_file:
        input_list = []
        for line in input_file:
            if line_strip:
                input_list.append(line.strip())
            else:
                input_list.append(line.rstrip("\n"))

    return input_list


def read_input_batch(input_file: str, line_split: bool = True) -> List[str]:
    with open(input_file, "r") as input_file:
        input_list = []
        batch = []
        for line in input_file:
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
