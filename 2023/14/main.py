import numpy as np
from numba import int64  # type: ignore
from numba.experimental import jitclass  # type: ignore

from utils import read_input, timefunc

DICT_ROCKS = {".": 0, "O": 1, "#": 2}


@jitclass([("orig_platform", int64[:, :]), ("platform", int64[:, :])])
class Platform:
    def __init__(self, platform) -> None:
        self.orig_platform = platform
        self.platform = platform.copy()

    def reset(self):
        self.platform = self.orig_platform

    def transform(self, tilt, platform):
        if tilt == 0:
            return platform
        elif tilt == 1:
            return platform.T
        elif tilt == 2:
            return platform[::-1, ...]
        elif tilt == 3:
            return platform.T[::-1, ...]

    def inverse(self, tilt, platform):
        if tilt == 0:
            return platform
        elif tilt == 1:
            return platform.T
        elif tilt == 2:
            return platform[::-1, ...]
        elif tilt == 3:
            return platform[::-1, ...].T

    def tilt_platform(self, tilt):
        i = 1
        platform = self.transform(tilt, self.platform)

        while i < platform.shape[0]:
            # Test if previous row has space
            zeros = platform[i - 1] == 0
            change = platform[i] == 1
            if zeros.any() > 0:
                change = (platform[i] == 1) * zeros
                if change.any() > 0:
                    # Test if current row has round rocks
                    platform[i - 1] += change
                    platform[i] -= change
                    i -= 1
                else:
                    i += 1
            else:
                i += 1

            if i < 1:
                i = 1
        self.platform = self.inverse(tilt, platform)

    def spin_platform(self):
        dict_maps = {0: self.platform.copy()}
        cycle = 0
        while True:
            cycle += 1
            for tilt in [i for i in range(4)]:
                self.tilt_platform(tilt)

            for i, config in dict_maps.items():
                if np.array_equal(self.platform, config):
                    break
            else:
                dict_maps[cycle] = self.platform.copy()
            if i != cycle - 1:
                break

        start_cycle = [
            k for k, v in dict_maps.items() if np.array_equal(self.platform, v)
        ][0]
        end_platform = dict_maps[
            start_cycle + (1000000000 - start_cycle) % (cycle - start_cycle)
        ]
        self.platform = end_platform


def calculate_load(platform):
    return (platform == 1).sum(axis=1).dot(1 + np.flip(np.arange(platform.shape[0])))


@timefunc
def main(filename: str):
    platform = Platform(
        np.array(
            [[DICT_ROCKS[rock] for rock in line] for line in read_input(filename)],
            dtype=int,
        )
    )
    platform.tilt_platform(0)
    print(f"Result of part 1: {calculate_load(platform.platform)}")
    platform.reset()
    platform.spin_platform()
    print(f"Result of part 2: {calculate_load(platform.platform)}")


if __name__ == "__main__":
    main("2023/14/input.txt")
